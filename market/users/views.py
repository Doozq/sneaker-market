from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from users.forms import ProfileForm, RegisterForm, UserForm
from users.models import Person

__all__ = ["signup"]


def signup(request):
    template = "users/signup.html"
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        reg_url = f"http://127.0.0.1:8000/auth/activate/{username}"
        send_mail(
            f"Привет {username}",
            f"Для активации ползователя перейдите по ссылке:\n{reg_url}",
            settings.FEEDBACK_SENDER,
            [form.cleaned_data["email"]],
            fail_silently=False,
        )
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()
        return redirect("users:login")
    context = {"form": form}
    return render(request, template, context)


def activate(request, username):
    user = User.objects.get(username=username)
    now = timezone.now()
    reg_datetime = user.date_joined
    print(reg_datetime)
    time = now - reg_datetime
    if 12 * 60 * 60 > time.total_seconds():
        user.is_active = True
        user.save()
        text = f"Вы активировали аккаунт {username}"
    else:
        text = "Истек срок активации (12 часов)"

    template = "users/activate.html"
    context = {"text": text}
    return render(request, template, context)


def user_list(request):
    template = "users/user_list.html"
    users = Person.objects.active_users_list()
    context = {"users": users}
    return render(request, template, context)


def user_detail(request, pk):
    template = "users/user_detail.html"
    queryset = Person.objects.queryset_for_user_detail()
    user = get_object_or_404(queryset, pk=pk)
    context = {"user": user}
    return render(request, template, context)


def profile(request):
    user = request.user
    template = "users/profile.html"
    initial_user = {
        "email": user.email,
        "first_name": user.first_name,
    }
    form_user = UserForm(request.POST or initial_user)
    form_profile = ProfileForm(request.POST, request.FILES)
    if (
        request.method == "POST"
        and form_user.is_valid()
        and form_profile.is_valid()
    ):
        user.email = form_user.cleaned_data["email"]
        user.first_name = form_user.cleaned_data["first_name"]
        user.profile.birthday = form_profile.cleaned_data["birthday"]
        user.profile.image = form_profile.cleaned_data["image"]
        user.save()
        user.profile.save()
        return redirect("users:profile")

    initial_profile = {
        "birthday": user.profile.birthday,
        "image": user.profile.image.url,
    }
    form_profile = ProfileForm(initial_profile)
    context = {"form_user": form_user, "form_profile": form_profile}
    return render(request, template, context)
