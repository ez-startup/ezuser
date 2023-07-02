from django.shortcuts import render
from django.utils.translation import gettext as _

# Create your views here.
def index(request):
    text = "Welcome to User Manager!"
    return render(request, "base.html",{'text':text})