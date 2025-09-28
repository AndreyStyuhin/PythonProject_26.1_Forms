from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'image', 'status']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user  # назначаем владельца
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'image', 'status']
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # только владелец или модератор с правом can_unpublish_product может редактировать
        if obj.owner != request.user and not request.user.has_perm("products.can_unpublish_product"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Дополнительная проверка для изменения статуса опубликованного продукта
        if (self.object.status == 'published' and
            form.cleaned_data['status'] == 'draft' and
            self.object.owner != self.request.user and
            not self.request.user.has_perm("products.can_unpublish_product")):
            raise PermissionDenied("Недостаточно прав для снятия с публикации")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # владелец или модератор с правом "delete_product"
        if obj.owner != request.user and not request.user.has_perm("products.delete_product"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
