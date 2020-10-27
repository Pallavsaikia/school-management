from rest_framework import serializers
from helper.validation_error_response import error_response
from django.contrib.auth.models import User
from teacher.models import UserAbstract
from student.models import Student
from helper.exception import CustomValidation
from helper.errors import Error
from helper.quick_errors import raise_field_error, raise_missing_field_error


class RegisterSerializers(serializers.Serializer):
    year = serializers.IntegerField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def save(self):
        password = self.validated_data['password']
        if password != "":

            exist, string, user_abs = UserAbstract.objects.get_student_by_email_for_registration(
                email=self.validated_data['email'])
            if exist:
                username = self.validated_data['username']
                year = self.validated_data['year']
                user = User.objects.filter(username=username)
                if user.count() == 0:
                    # saving user in main user table
                    user = User(
                        username=self.validated_data['username']
                    )
                    user.set_password(password)
                    user.save()
                    # updating user in user abstract table
                    user_abs.registered = True
                    user_abs.user = user
                    new_user = user_abs.save()
                    # adding student to Student Table
                    Student(student=user_abs, year=year).save()
                else:
                    raise_field_error(key='username', details='username already exist')
            else:
                raise_field_error(key='email', details=string)
        else:
            raise_missing_field_error(key='password', details='Password cannot be empty')
