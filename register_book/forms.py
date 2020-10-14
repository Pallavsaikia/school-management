from django import forms


class RegisterBookForm(forms.Form):

    course = forms.IntegerField()
    semester = forms.IntegerField()
    subject = forms.IntegerField()
    year = forms.IntegerField()