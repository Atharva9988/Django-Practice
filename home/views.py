from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render

from vege.seed import *


def home(request):

    seed_db(100)

    players = [
        {'name' : 'Abhishek Sharma', 'age' : 23, 'totalruns': 1630},
        {'name' : 'Shubhman Gill', 'age' : 25, 'totalruns': 7291},
        {'name' : 'Virat Kohli', 'age' : 37, 'totalruns': 28359},
        {'name' : 'Rohit Sharma', 'age' : 39, 'totalruns': 20427},
    ]

    return render(request, "home/index.html", context={'page': 'Django Practice', 'players': players})


def about(request):
    context = {'page': 'About'}
    return render(request, "home/about.html", context)


def contact(request):
    context = {'page': 'Contact'}
    return render(request, "home/contact.html", context)


def livingroom(request):
    print("*" * 10)
    return HttpResponse("<h2> I am the son of home page, I say, 'I am back daddy'</h2>")


@login_required
def send_email_view(request):
    context = {'page': 'Send Email'}
    if request.method == "POST":
        to_email = request.POST.get("to_email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        try:
            validate_email(to_email)
            if not subject or not message:
                raise ValidationError("Subject and message are required.")
            send_mail(subject, message, None, [to_email])
            context["success"] = f"Email sent to {to_email}."
        except ValidationError as e:
            context["error"] = " ".join(e.messages)
        except OSError as e:
            context["error"] = f"Sending failed: {e}"
    return render(request, "home/send_email.html", context)