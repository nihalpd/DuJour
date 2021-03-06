from django.db import models
from django.core.exceptions import ValidationError
import os

def validate_file_extension(value):
    if not (value.name.endswith('.png') or value.name.endswith('.jpg')):
        raise ValidationError(u'Please upload a PNG or JPG file only')

class Restaurant(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    fax = models.CharField(max_length=20, blank=True)
    website = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class DayRestaurant(models.Model):
    class Meta:
        verbose_name = 'Assigned day of week'
        verbose_name_plural = 'Assigned days of week'

    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAY_CHOICES)

class Menu(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='static/menus/', validators=[validate_file_extension])

class MenuItem(models.Model):
    menu = models.ForeignKey('Menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=6, max_digits=9)

class MenuItemType(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)
    is_base_price = models.BooleanField(default=False)
    allow_many = models.BooleanField(default=False)

class MenuItemTypeOption(models.Model):
    menu_item_type = models.ForeignKey('MenuItemType', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=6, max_digits=9, null=True)

class MenuItemRegion(models.Model):
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    menu_item_type = models.ForeignKey('MenuItemType', null=True, on_delete=models.CASCADE)
    sw_lng = models.FloatField()
    sw_lat = models.FloatField()
    ne_lng = models.FloatField()
    ne_lat = models.FloatField()
