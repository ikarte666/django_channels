from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

signup = CreateView.as_view(
    form_class=UserCreationForm,
    template_name="partials/form.html",
    extra_context={"form_name": "Sign up", "submit_label": "Sign up"},
    success_url=reverse_lazy("accounts:login"),
)

login = LoginView.as_view(
    template_name="partials/form.html",
    extra_context={"form_name": "로그인", "submit_label": "로그인"},
)

logout = LogoutView.as_view(next_page="accounts:login")


@login_required
def profile(request):
    user = request.user
    return render(
        request,
        "accounts/profile.html",
        {
            "user": user,
        },
    )
