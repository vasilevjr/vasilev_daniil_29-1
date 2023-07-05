from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100)
    # image = models.ImageField(null=True, blank=True)

class Product(models.Model):
    image = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=245, default=0)
    description = models.TextField()
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    """ M2M """
    categories = models.ManyToManyField(Category)
    
    @property
    def categories_list(self) -> list:
        return self.categories.all()










