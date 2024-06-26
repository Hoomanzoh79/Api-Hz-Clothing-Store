from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator


class Cloth(models.Model):
    SEASON_CHOICES = [
        ("winter", "winter"),
        ("summer", "summer"),
        ("fall", "fall"),
    ]
    GENDER_CHOICES = [
        ("male", "male"),
        ("female", "female"),
    ]

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(50000)],default=0,verbose_name=_("price"))
    active = models.BooleanField(default=True)
    season = models.CharField(max_length=6, choices=SEASON_CHOICES)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    # cover = models.ImageField(upload_to='cloth/cloth_covers', blank=True)

    datetime_created = models.DateTimeField(default=timezone.now)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def api_get_absolute_url(self):
        return reverse("cloths:api-v1:cloth-detail", kwargs={"pk": self.pk})
