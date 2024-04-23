from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

__all__ = ["Profile", "PersonManager", "Person"]


class PersonManager(models.Manager):
    def active_users_list(self):
        return self.filter(
            is_active=True,
        ).only(
            "username",
        )

    def queryset_for_user_detail(self):
        return self.only("email", "first_name", "last_name").select_related(
            User.profile.related.name,
        )


class Person(User):
    objects = PersonManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="users/", null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
