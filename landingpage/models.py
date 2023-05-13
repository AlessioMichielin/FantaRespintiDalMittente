from django.db import models

# Create your models here.

class LandingPage(models.Model):
    sfida = models.TextField()
    punti = models.IntegerField()

    def __str__(self):
        return self.sfida