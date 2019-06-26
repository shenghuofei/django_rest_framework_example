# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

# Create your views here.

from django import forms
from django.shortcuts import render

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
