from django import forms
from django.http import HttpResponse
from django.conf import settings


class CommentForm(forms.Form):
    txt = forms.CharField(widget=forms.Textarea)
    #txt = forms.CharField(widget=forms.Textarea)
