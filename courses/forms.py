from django import forms


class CourseForm(forms.Form):
    course_name = forms.CharField()
    abbreviation = forms.CharField()
    num_div = forms.IntegerField()
