import io
import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from products.forms import ProductForm


@pytest.fixture
def valid_data():
    return {
        'name': 'Хороший продукт',
        'description': 'Описание без запрещённых слов',
        'price': '100.00'
    }


def generate_image_file(format='JPEG', size=(100, 100), name='test.jpg'):
    file = io.BytesIO()
    image = Image.new('RGB', size)
    image.save(file, format=format)
    file.name = name
    file.seek(0)
    return file


@pytest.mark.django_db
def test_valid_data(valid_data):
    form = ProductForm(data=valid_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_forbidden_word_in_name(valid_data):
    data = valid_data.copy()
    data['name'] = 'Лучшее казино онлайн'
    form = ProductForm(data=data)
    assert not form.is_valid()
    assert 'name' in form.errors
    assert 'Название содержит запрещённые слова.' in form.errors['name']


@pytest.mark.django_db
def test_forbidden_word_in_description(valid_data):
    data = valid_data.copy()
    data['description'] = 'Очень дешево и бесплатно!'
    form = ProductForm(data=data)
    assert not form.is_valid()
    assert 'description' in form.errors
    assert 'Описание содержит запрещённые слова.' in form.errors['description']


@pytest.mark.django_db
def test_case_insensitivity(valid_data):
    data = valid_data.copy()
    data['description'] = 'ОБМАН пользователей'
    form = ProductForm(data=data)
    assert not form.is_valid()
    assert 'description' in form.errors


@pytest.mark.django_db
def test_valid_image(valid_data):
    image_file = generate_image_file()
    image = SimpleUploadedFile('valid.jpg', image_file.read(), content_type='image/jpeg')
    form = ProductForm(data=valid_data, files={'image': image})
    assert form.is_valid()


@pytest.mark.django_db
def test_invalid_format_image(valid_data):
    fake_txt = SimpleUploadedFile('not_image.txt', b'This is not an image.', content_type='text/plain')
    form = ProductForm(data=valid_data, files={'image': fake_txt})
    assert not form.is_valid()
    assert 'image' in form.errors
    assert 'JPEG' in form.errors['image'][0] or 'PNG' in form.errors['image'][0]


@pytest.mark.django_db
def test_too_large_image(valid_data):
    image_file = generate_image_file()
    content = image_file.read()
    content *= (6 * 1024 * 1024) // len(content) + 1  # сделать >5MB

    large_file = SimpleUploadedFile('big.jpg', content, content_type='image/jpeg')
    form = ProductForm(data=valid_data, files={'image': large_file})
    assert not form.is_valid()
    assert 'image' in form.errors
    assert '5 МБ' in form.errors['image'][0]
