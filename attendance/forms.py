from django import forms
from school_management.settings import DATE_INPUT_FORMATS


class AttendanceForm(forms.Form):
    book_id = forms.IntegerField()
    half = forms.IntegerField()
    attendance_date = forms.DateField(input_formats=['%d / %b / %Y',])
