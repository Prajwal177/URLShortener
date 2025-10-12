from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import RegisterForm, ShortURLForm
from .models import ShortURL

# Registration
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            messages.success(request, "Account created and logged in.")
            return redirect("shortener:dashboard")
    else:
        form = RegisterForm()
    return render(request, "shortener/register.html", {"form": form})

# Login
from django.contrib.auth.forms import AuthenticationForm
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("shortener:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "shortener/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("shortener:login")

# Dashboard
@login_required
def dashboard(request):
    form = ShortURLForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        short = form.save(commit=False)
        short.owner = request.user
        short.save()
        messages.success(request, f"Short URL created: {request.build_absolute_uri('/')[:-1]}/{short.short_code}")
        return redirect("shortener:dashboard")
    urls = ShortURL.objects.filter(owner=request.user).order_by("-created_at")
    base_url = request.build_absolute_uri('/')[:-1]
    return render(request, "shortener/dashboard.html", {"form": form, "urls": urls, "base_url": base_url})

# Delete URL (owner only)
@login_required
def delete_url(request, pk):
    obj = get_object_or_404(ShortURL, pk=pk, owner=request.user)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Short URL deleted.")
        return redirect("shortener:dashboard")
    return render(request, "shortener/confirm_delete.html", {"object": obj})

# Redirect endpoint
def redirect_view(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    short_url.click_count += 1
    short_url.save()
    return HttpResponseRedirect(short_url.original_url)
