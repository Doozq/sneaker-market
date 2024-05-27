import django.core.validators
import django.db.models
from django.utils.html import mark_safe
from sorl.thumbnail import get_thumbnail
from django.db import models
from core.models import AbstractModel

from users.models import User

__all__ = ["Category", "GalleryImage", "MainImage", "Item", "Tag"]


class Tag(AbstractModel):
    slug = django.db.models.CharField(
        "Слаг",
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(AbstractModel):
    slug = django.db.models.CharField(
        verbose_name="слаг",
        max_length=200,
        unique=True,
        validators=[django.core.validators.validate_slug],
    )
    weight = django.db.models.IntegerField(
        "Вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class GalleryImage(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="catalog/",
        null=True,
        blank=True,
        verbose_name="изображение",
    )

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51, crop="center")

    item = django.db.models.ForeignKey(
        "Item",
        related_name="gallery_images",
        on_delete=django.db.models.CASCADE,
    )


class MainImage(django.db.models.Model):
    image = django.db.models.ImageField(
        upload_to="catalog/",
        null=True,
        blank=True,
        verbose_name="изображение",
    )

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51, crop="center")

    item = django.db.models.OneToOneField(
        "Item",
        related_name="item_main_image",
        on_delete=django.db.models.CASCADE,
    )


class ItemManager(django.db.models.Manager):
    def on_main(self):
        return (
            self.published()
            .filter(
                is_on_main=True,
            )
            .order_by(
                Item.name.field.name,
            )
        )

    def published(self):
        return (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .order_by(
                f"{Item.category.field.name}__{Category.name.field.name}",
                Item.name.field.name,
            )
            .select_related(
                Item.category.field.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.tags.field.name,
                    queryset=Tag.objects.all().only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .only(
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__{Category.name.field.name}",
                f"{Item.tags.field.name}__{Tag.name.field.name}",
            )
        )

    def queryset_for_item_detail(self):
        return (
            self.published()
            .select_related(
                Item.item_main_image.related.name,
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    Item.gallery_images.field.related_query_name(),
                    queryset=GalleryImage.objects.only(
                        GalleryImage.image.field.name,
                        GalleryImage.item_id.field.name,
                    ),
                ),
            )
        )


class Item(AbstractModel):
    objects = ItemManager()
    price = models.PositiveIntegerField(default=1)
    color = django.db.models.CharField(
        "Цвет",
        max_length=150,
        help_text="Перечислите цвета",
        default="",
    )
    is_on_main = django.db.models.BooleanField(default=False)
    category = django.db.models.ForeignKey(
        "category",
        default=None,
        help_text="Выберите категорию",
        verbose_name="Категория",
        related_name="category_items",
        on_delete=django.db.models.CASCADE,
    )
    tags = django.db.models.ManyToManyField(Tag, verbose_name="теги")
    text = django.db.models.TextField(
        "Текст",
        help_text="Описание товара",
    )

    def main_image_tmb(self):
        if self.item_main_image:
            new_image = self.item_main_image.get_image_300x300()
            return mark_safe(f"<img src='{new_image.url}'>")
        return "Нет изображения"

    main_image_tmb.short_description = "Главное изображение"
    main_image_tmb.allow_tags = True

    def get_gallery_urls(self):
        return [i.get_image_300x300().url for i in self.gallery_images.all()]

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    items = models.TextField()  # Мы будем хранить список товаров как текст
    total_price = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f'Заказ #{self.order_number} от {self.order_date}'    