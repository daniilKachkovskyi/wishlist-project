from django.db import models
from django.contrib.auth.models import User

class Wish(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True)
    reason = models.TextField(blank=True, verbose_name="Чому це тобі потрібно?")
    photo_url = models.URLField(blank=True, null=True, verbose_name="Посилання на фото (URL)")
    is_received = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.title