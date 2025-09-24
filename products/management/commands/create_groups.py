from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from products.models import Product
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = "Создаёт группы и назначает права"

    def handle(self, *args, **kwargs):
        product_ct = ContentType.objects.get_for_model(Product)

        # создаём группу "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name="Модератор продуктов")

        # права: удалять продукт + unpublish
        delete_permission = Permission.objects.get(
            codename="delete_product",
            content_type=product_ct
        )
        unpublish_permission = Permission.objects.get(
            codename="can_unpublish_product",
            content_type=product_ct
        )

        moderator_group.permissions.add(delete_permission, unpublish_permission)

        self.stdout.write(self.style.SUCCESS("Группа 'Модератор продуктов' создана"))
