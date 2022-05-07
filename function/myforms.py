from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

class RegiForm(forms.Form):
    name=forms.CharField(min_length=4,widget=widgets.TextInput(attrs={"class":"form-control"}))
    pwd=forms.CharField(min_length=8,widget=widgets.PasswordInput(attrs={"class":"form-control"}))
    repwd=forms.CharField(min_length=8,widget=widgets.PasswordInput(attrs={"class":"form-control"}))
    email=forms.EmailField(widget=widgets.EmailInput(attrs={"class":"form-control"}))
    phone=forms.IntegerField(widget=widgets.TextInput(attrs={"class":"form-control"}))

    def clean(self):
        if self.cleaned_data.get("pwd") != self.cleaned_data.get("repwd"):
            raise ValidationError("两次密码输入不一致")
        else:
            return self.cleaned_data