# apps.products/forms.py
from django import forms
from apps.products.models import Product
from apps.products.validators import FORBIDDEN_WORDS

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Введите название продукта',
            'description': 'Описание...',
            'price': '0.00',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]
            if field_name == 'image':
                field.widget.attrs['class'] = 'form-control-file'

    def clean_name(self):
        name = self.cleaned_data['name']
        if self.contains_forbidden_word(name):
            raise forms.ValidationError("Название содержит запрещённые слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if self.contains_forbidden_word(description):
            raise forms.ValidationError("Описание содержит запрещённые слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if hasattr(image, 'content_type'):
                if image.content_type not in ['image/jpeg', 'image/png']:
                    raise forms.ValidationError("Только изображения в формате JPEG или PNG.")
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Размер изображения не должен превышать 5 МБ.")
        return image

    def contains_forbidden_word(self, text):
        text_lower = text.lower()
        return any(word in text_lower for word in FORBIDDEN_WORDS)
