from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    average_rating = models.FloatField()
    description = models.TextField()
    price = models.FloatField()
    def __str__(self):
         return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    small_url = models.JSONField(default=list, help_text="List of URLs for small-size images")
    medium_url = models.JSONField(default=list, help_text="List of URLs for medium-size images")
    large_url = models.JSONField(default=list, help_text="List of URLs for large-size images")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
       return (
           f"Image for {self.product.name} | "
           f"small={self.small_url}, medium={self.medium_url}, large={self.large_url}"
       )
    

class User(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    def __str__(self):
         return self.username

class Review(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    timestamp = models.BigIntegerField()
    def __str__(self):
       return self.title