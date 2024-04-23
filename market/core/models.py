import django.db.models

__all__ = ["AbstractModel"]


class AbstractModel(django.db.models.Model):
    is_published = django.db.models.BooleanField("опубликовано", default=True)
    name = django.db.models.CharField(
        "название",
        unique=True,
        max_length=150,
        help_text="max 150 символов",
    )

    class Meta:
        abstract = True
