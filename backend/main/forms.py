from django import forms
from django.contrib.auth.models import User

class Registration(forms.ModelForm):
    error_messages = {'password_mismatch': ("Пароли не совпадают.")}
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput())
    password1.widget.attrs.update({'class': 'form-control form-control-sm'})
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput())
    password2.widget.attrs.update({'class': 'form-control form-control-sm'})
    first_name = forms.CharField(label="Имя",
                               widget=forms.TextInput())
    first_name.widget.attrs.update({'class': 'form-control form-control-sm'})
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput())
    username.widget.attrs.update({'class': 'form-control form-control-sm'})
    class Meta:
        model = User
        fields = ('first_name', "username")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch')
        return password2

    def save(self, commit=True):
        user = super(Registration, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user