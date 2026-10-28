from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ReceipeForm
from .models import Receipe

User = get_user_model()


def _flash_errors(request, form):
    for errors in form.errors.values():
        for err in errors:
            messages.error(request, err)


@login_required
def receipes(request):
    if request.method == "POST":
        form = ReceipeForm(request.POST, request.FILES)
        if form.is_valid():
            receipe = form.save(commit=False)
            receipe.user = request.user
            receipe.save()
        else:
            _flash_errors(request, form)
        return redirect("receipes")

    queryset = Receipe.objects.filter(user=request.user)
    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(receipe_name__icontains=search)
    return render(request, "receipes.html", {"receipes": queryset})


@login_required
def update_receipe(request, id):
    receipe = get_object_or_404(Receipe, id=id, user=request.user)
    if request.method == "POST":
        form = ReceipeForm(request.POST, request.FILES, instance=receipe)
        if form.is_valid():
            form.save()
            return redirect("receipes")
        _flash_errors(request, form)
    return render(request, "update_receipe.html", {"receipe": receipe})


@login_required
@require_POST
def delete_receipe(request, id):
    get_object_or_404(Receipe, id=id, user=request.user).delete()
    return redirect("receipes")


def login_page(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user is None:
            messages.error(request, "Invalid phone number or password.")
            return redirect("login_page")
        login(request, user)
        return redirect("receipes")
    return render(request, "login.html")


@require_POST
def logout_page(request):
    logout(request)
    return redirect("login_page")


def register(request):
    if request.method == "POST":
        phone = request.POST.get("phone_number", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        if not phone or not email:
            messages.error(request, "Phone number and email are required.")
            return redirect("register")
        if User.objects.filter(phone_number=phone).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "An account with that phone number or email already exists.")
            return redirect("register")
        try:
            validate_password(password)
        except ValidationError as e:
            messages.error(request, " ".join(e.messages))
            return redirect("register")

        User.objects.create_user(
            phone_number=phone,
            email=email,
            password=password,
            first_name=request.POST.get("first_name", "").strip(),
            last_name=request.POST.get("last_name", "").strip(),
        )
        messages.success(request, "Account created. You can log in now.")
        return redirect("login_page")
    return render(request, "register.html")