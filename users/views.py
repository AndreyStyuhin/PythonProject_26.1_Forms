from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from .forms import RegisterForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from products.models import Product


class RegisterView(View):
    template_name = 'users/register.html'
    form_class = RegisterForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()

            # Отправка приветственного письма
            self.send_welcome_email(user)

            # Автоматический вход после регистрации
            login(request, user)
            return redirect('home')  # Замените 'home' на ваш URL

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


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    # Разрешаем доступ всем (анонимным и авторизованным)
    # Ничего не меняем, так как это общедоступная страница


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'image']
    template_name = 'products/product_form.html'
    success_url = '/'

    # LoginRequiredMixin автоматически перенаправит
    # анонимных пользователей на страницу входа


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'image']
    template_name = 'products/product_form.html'
    success_url = '/'


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = '/'