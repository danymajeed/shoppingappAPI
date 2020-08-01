from django.db import models


def upload_path(instance, filename):
    return '/'.join([str(instance.title), filename])


def default_image():
    return '/default.png'


class Product(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    screen_size = models.DecimalField(
        max_digits=3, decimal_places=1, blank=False)
    ram = models.IntegerField()
    storage = models.IntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False)
    image = models.ImageField(default=default_image, upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
