from django.db import models

class Wish(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True)
    is_received = models.BooleanField(default=False)

    def __str__(self):
        return self.title