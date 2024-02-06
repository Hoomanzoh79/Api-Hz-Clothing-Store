from django.shortcuts import render
from django.views.generic import TemplateView


class HelloPageView(TemplateView):
    template_name = "cloths/hello.html"
