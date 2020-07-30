from django import forms
from bugreport.models import Ticket

N = "New"
IP = "In-Progress"
D = "Done"
INV = "Invalid"
DEFAULT_CHOICES = [
    (N, "New"),
    (IP, "In-Progress"),
    (D, "Done"),
    (INV, "Invalid")
]


class AddTicket(forms.Form):
    title = forms.CharField(max_length=50)
    body = forms.CharField(widget=forms.Textarea)


class Login_Form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class Change_Status_Form(forms.Form):
    status = forms.ChoiceField(choices=DEFAULT_CHOICES)
