from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from register_book.models import RegisterBook
from courses.models import Courses
from django.contrib import messages
from register_book.forms import RegisterBookForm
from helper.authenticate import authenticate_superuser
import datetime
from .models import Attendance
from .forms import AttendanceForm
from helper.qr import QrCode, QrData
from helper.urlbuilder import build_url


# Create your views here.

class SearchAttendanceBookView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id=None):
        courses = Courses.objects.all()
        now = datetime.datetime.now()
        books = RegisterBook.objects.filter(active=True).filter(year=now.year).order_by('subject__course__abbreviation',
                                                                                        'subject__semester',
                                                                                        'subject__name')
        if id is not None:
            success, str = RegisterBook.objects.toggle_book(id=id)
            if success:
                messages.success(request, str)
            else:
                messages.error(request, str)
            return redirect('/register-book')
        else:
            return render(request, "search_attendance_book.html", {"edit": False, 'courses': courses, 'books': books})

    @method_decorator(authenticate_superuser)
    def post(self, request, id=None):
        form = RegisterBookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            success, str, book = RegisterBook.objects.check_book_exist_by_year_subject_return_book(
                subject_id=data["subject"],
                year=data["year"])
            if success:
                messages.success(request, str)
                return redirect(reverse('attendances:view_book', kwargs={'id': book.id}))
            else:
                messages.error(request, str)
                return redirect('/attendance')
        else:
            messages.error(request, "Fields cannot be empty")
            return redirect('/attendance')


class ViewAttendanceBookView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request, id):

        now = datetime.datetime.now()
        books = RegisterBook.objects.filter(active=True).filter(year=now.year).order_by('subject__course__abbreviation',
                                                                                        'subject__semester',
                                                                                        'subject__name')
        exist, book = RegisterBook.objects.get_or_do_not_exist(id_book=id)
        if exist:
            half = Attendance.objects.get_half(book=book, date_attendance=now.date()) + 1
            return render(request, "start_attendance.html",
                          {"edit": False, 'course': book.subject.course.abbreviation, 'semester': book.subject.semester,
                           'year': book.year,
                           'subject': book.subject.name,
                           'book': book,
                           'half': half,
                           'books': books})
        else:
            messages.error(request, "Book Does not exist")
            redirect('/attendance')


class StartAttendance(View):
    @method_decorator(authenticate_superuser)
    def post(self, request):
        form = AttendanceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            book_id = data["book_id"]
            half = data["half"]
            date = data["attendance_date"]
            success, string = Attendance.objects.bulk_insert(book_id=book_id, half=data["half"],
                                                             date_attendance=data["attendance_date"])
            if success:
                qr_str = QrCode.encode(book_id=book_id, date=date, half=half).decode("utf-8")
                url = build_url('attendances:qr_code_scanner', get={'qr_code': qr_str})
                return redirect(url)
            else:
                messages.error(request, string)
                return redirect(reverse('attendances:view_book', kwargs={'id': book_id}))
        else:
            messages.error(request, "Field error")
            return redirect(reverse('attendances:view_book', kwargs={'id': request.POST["book_id"]}))


class QRcodeView(View):
    @method_decorator(authenticate_superuser)
    def get(self, request):
        qr_code = request.GET["qr_code"]
        success, dict = QrCode.decode(qr_code)
        if success:
            qr_data = QrData(dict)
            exist, book = RegisterBook.objects.get_or_do_not_exist(qr_data.book_id)
            valid, date = qr_data.get_processed_date()
            if exist and valid:

                attendance_exist = Attendance.objects.check_entry_exist_for_date_half_book(book=book,
                                                                                           date_attendance=date,
                                                                                           half=qr_data.half)

                subject = book.subject.name
                course = book.subject.course.abbreviation
                semester = book.subject.semester
                year = book.year
                if attendance_exist:
                    return render(request, "qr_code.html",
                                  {"qr": qr_code, "valid": True,
                                   "subject": subject,
                                   "course": course,
                                   "semester": semester,
                                   "year": year})
                else:
                    return render(request, "qr_code.html",
                                  {"qr": qr_code, "valid": False})
            else:
                return render(request, "qr_code.html",
                              {"qr": qr_code, "valid": False})

        else:
            return render(request, "qr_code.html",
                          {"qr": qr_code, "valid": False})
