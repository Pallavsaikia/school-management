from django import forms


class RegisterForm(forms.Form):
    FORM_FIELD_ERROR = "Fields can not be empty"
    PASSWORD_ERROR = "Password Does not match"
    SUCCESS = "No Error"
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()

    def is_valid(self):

        # run the parent validation first
        valid = super(RegisterForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid, self.FORM_FIELD_ERROR

        if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
            self._errors = 'passwords does not match'
            return False, self.PASSWORD_ERROR

        # all good
        return True, self.SUCCESS
