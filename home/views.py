from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse

from vege.seed import *


def home(request):

    seed_db(100)

    players = [
        {'name' : 'Abhishek Sharma', 'age' : 23, 'totalruns': 1630},
        {'name' : 'Shubhman Gill', 'age' : 25, 'totalruns': 7291},
        {'name' : 'Virat Kohli', 'age' : 37, 'totalruns': 28359},
        {'name' : 'Rohit Sharma', 'age' : 39, 'totalruns': 20427}, 
    ]

    

    return render(request, "home/index.html" , context={'page':'Django Practice','players': players})

def about(request):
    context = {'page' : 'About'}
    return render(request, "home/about.html", context)

def contact(request):
    context = {'page' : 'Contact'}
    return render(request, "home/contact.html", context)

def livingroom(request):
    print("*" * 10)
    return HttpResponse("<h2> I am the son of home page, I say, 'I am back daddy'</h2>")