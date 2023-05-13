from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ExifTags


class Sfide(models.Model):
    sfida = models.TextField(blank=True, null=True)
    punti = models.IntegerField(default='0')

    def __str__(self):
        return self.sfida

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    foto = models.ImageField(default='default.jpg', upload_to='profile_images')
    sfide = models.ManyToManyField(Sfide, blank=True)
    puntitotali = models.IntegerField(default='0', null=True)

    def __str__(self):
        return "Profilo di: {}".format(self.user.username)
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        
        img = Image.open(self.foto.path)

        # ruota immagine se è contenuto nei metadati
        try:

            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':
                    break
            
            exif=dict(img._getexif().items())

            if exif[orientation] == 3:
                img=img.rotate(180, expand=True)
            elif exif[orientation] == 6:
                img=img.rotate(270, expand=True)
            elif exif[orientation] == 8:
                img=img.rotate(90, expand=True)

            img.save(self.foto.path)
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        # riduce la dimensione dell immagine
        if img.height > 300 or img.width > 300:
                output_size = (480,480)
                img.thumbnail(output_size)
                img.save(self.foto.path)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        