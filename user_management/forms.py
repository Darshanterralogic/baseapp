import re
from django import forms
from django.core.exceptions import ValidationError

# Custom validator for name fields
def validate_name(value):
    if not re.match(r'^[a-zA-Z]*$', value):
        raise ValidationError('Name should only contain alphabetical characters.')


# Custom validator for Employee ID
def validate_employee_id(value):
    if not re.match(r'^PSI-\d{4}$', value):
        raise ValidationError('Employee ID should be in the format PSI-XXXX.')

# Custom validator for password
def validate_password(value):
    if len(value) < 8 or len(value) > 10:
        raise ValidationError('Password length should be between 8 and 10 characters.')
    if not any(char.isupper() for char in value):
        raise ValidationError('Password should contain at least 1 uppercase character.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password should contain at least 1 digit.')
    if not any(char in "!@#$%^&*()_+{}[]|\<>?/~`" for char in value):
        raise ValidationError('Password should contain at least 1 special character.')

# Common widget attributes for all fields
common_widget_attrs = {
    'class': 'form-control form-control-user',
    'required': True,
}


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        widget=forms.TextInput(attrs={**common_widget_attrs, 'id': 'exampleFirstName','placeholder':'Enter First name'})
    )
    last_name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        widget=forms.TextInput(attrs={**common_widget_attrs,'id': 'exampleLastName','placeholder':'Enter Last name'})
    )
    employee_id = forms.CharField(
        max_length=10,
        validators=[validate_employee_id],
        widget=forms.TextInput(attrs={**common_widget_attrs, 'id': 'empid','placeholder':'Enter EmpId'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={**common_widget_attrs, 'id': 'exampleInputEmail','placeholder':'Enter Email '})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={**common_widget_attrs, 'id': 'exampleInputPassword','placeholder':'Enter Password'}),
        validators=[validate_password]
    )
    re_enter_password = forms.CharField(
        widget=forms.PasswordInput(attrs={**common_widget_attrs, 'id': 'exampleRepeatPassword','placeholder':'Enter Re-Enter Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        re_enter_password = cleaned_data.get("re_enter_password")

        if password and re_enter_password and password != re_enter_password:
            raise forms.ValidationError("Passwords do not match.")



class LoginForm(forms.Form):
    employee_id = forms.CharField(
        max_length=10,
        label="Employee ID",
        widget=forms.TextInput(attrs={**common_widget_attrs, 'placeholder': 'Employee ID'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={**common_widget_attrs, 'placeholder': 'Email Address'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={**common_widget_attrs, 'placeholder': 'Password'})
    )
