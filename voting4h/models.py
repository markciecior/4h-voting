from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


# Create your models here.


class Pet(models.Model):
    name = models.CharField("Pet Name", max_length=200, default="")
    owner = models.CharField("Pet Owner", max_length=200, default="")
    breed = models.CharField("Pet Breed", max_length=200, default="")

    # def vote_unique(self):
    #     return Profile.objects.filter(vote_unique=self).count()

    # def vote_cutest(self):
    #     return Profile.objects.filter(vote_cutest=self).count()

    # def vote_people_choice(self):
    #     return Profile.objects.filter(vote_people_choice=self).count()

    def __str__(self):
        return f"{self.name} ({self.breed}) by {self.owner}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vote_unique = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="unique", blank=True, null=True
    )
    vote_people_choice = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="people_choice",
        blank=True,
        null=True,
    )
    vote_cutest = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="cutest", blank=True, null=True
    )

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
