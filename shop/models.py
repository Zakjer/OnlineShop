from django.db import models
from django.core.validators import MinValueValidator
from .validators import validate_image_size

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(null=True, upload_to='shop/images', validators=[validate_image_size])
