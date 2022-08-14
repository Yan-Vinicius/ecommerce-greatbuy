from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    # essa função serve para que todos as classes dos campos do formulário tornem-se form-control
    # deixando o campo de input melhor visualmente
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match."
            )