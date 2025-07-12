from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Show(models.Model):
    name = models.CharField("Show Name", max_length=200, default="")
    date = models.DateField("Show Date", blank=True, null=True)
    location = models.CharField("Show Location", max_length=200, default="")
    active = models.BooleanField("Active Show", default=False)

    def __str__(self):
        return f"{self.name} at {self.location} on {self.date}"


class Pet(models.Model):
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name="pets", blank=True, null=True
    )
    name = models.CharField("Pet Name", max_length=200, default="")
    owner = models.CharField("Pet Owner", max_length=200, default="")
    breed = models.CharField("Pet Breed", max_length=200, default="")

    def __str__(self):
        return f"{self.name} ({self.breed}) by {self.owner}"


class Ballot(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    show = models.ForeignKey(
        Show, on_delete=models.CASCADE, related_name="ballots", blank=True, null=True
    )
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


class ManualBallot(models.Model):
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE,
        related_name="manualballots",
        blank=True,
        null=True,
    )
    vote_people_choice = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.vote_people_choice)


class UserProfile(models.Model):
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_ballot(sender, instance, created, **kwargs):
    if created:
        Ballot.objects.create(
            user=instance,
            show=(
                Show.objects.filter(active=True).last()
                if Show.objects.filter(active=True).exists()
                else None
            ),
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
        )


@receiver(post_save, sender=User)
def save_user_ballot(sender, instance, **kwargs):
    instance.ballot.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
