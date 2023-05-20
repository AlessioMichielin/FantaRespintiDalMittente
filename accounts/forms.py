from typing import Any
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Sfide

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class':'form-control',
            'type':'username',
            'id':'username',
            'required':''
        })
        self.fields["password"].widget.attrs.update({
            'class':'form-control',
            'type':'password',
            'id':'password',
            'required':'',
            'aria-autocomplete':'list'
        })

    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)
            if not user or not user.is_active:
                raise forms.ValidationError("C'è qualcosa di sbagliato. Riprova.")
            return self.cleaned_data


user=get_user_model()


class RegistrationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=40, required=False, help_text="Optional.")
    last_name = forms.CharField(max_length=40, required=False, help_text="Optional.")
    email = forms.CharField(max_length=120, required=False, help_text='Optional.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class':'form-control',
            'type':'username',
            'id':'username',
            'required':''
        })
        self.fields["first_name"].widget.attrs.update({
            'class':'form-control',
            'type':'text',
            'id':'text'
        })
        self.fields["last_name"].widget.attrs.update({
            'class':'form-control',
            'type':'text2',
            'id':'text2'
        })
        self.fields["email"].widget.attrs.update({
            'class':'form-control',
            'type':'email',
            'id':'email'
        })
        self.fields["password1"].widget.attrs.update({
            'class':'form-control',
            'type':'password',
            'id':'password1',
            'required':''
        })
        self.fields["password2"].widget.attrs.update({
            'class':'form-control',
            'type':'password',
            'id':'password2',
            'required':''
        })


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class UserEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'class':'form-control',
            'type':'username',
            'id':'username',
            'required':''
        })
        self.fields["email"].widget.attrs.update({
            'class':'form-control',
            'type':'email',
            'id':'email'
        })

    class Meta:
        model = User
        fields = ('username','email',)


class ProfileEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["foto"].widget.attrs.update({
            'type':'picture',
            'id':'photo',
        })

    class Meta:
        model = Profile
        fields = ('foto',)
        

class SfideForm(forms.ModelForm):
    sfide = forms.ModelMultipleChoiceField(
                        queryset=Sfide.objects.all().order_by('punti'),
                        label="sfide",
                        widget=forms.CheckboxSelectMultiple,
                        required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sfide"].widget.attrs.update({
            'type':'checkbox',
            'class':'listaCheckbox',
        })

# Controllo che non vengano scelte più di 5 sfide
    def clean_sfide(self):
        value = self.cleaned_data['sfide']
        if len(value) > 5:
            raise forms.ValidationError("Hei! Puoi scegliere massimo 5 sfide.")
        if len(value) == 0:
            raise forms.ValidationError("Non è stata scelta alcuna sfida.")
        return value

    class Meta:
      model = Profile
      fields = ('sfide',)