from django.shortcuts import render
from django.views import generic
import socket


# Create your views here.
class IndexView(generic.TemplateView):
    print("hostname = ", socket.getfqdn())
    template_name = 'index.html'
