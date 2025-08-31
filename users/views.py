# users/views.py
from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            self.send_welcome_email(user)
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})

    def send_welcome_email(self, user):
        subject = 'Добро пожаловать на наш сайт!'
        message = render_to_string('users/emails/welcome_email.txt', {'user': user})
        send_mail(
            subject,
            message,
            'noreply@yourdomain.com',
            [user.email],
            fail_silently=False,
        )


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
