from django.db import models
from category.models import Category, Subcategory
from django.core.validators import MinValueValidator, MaxValueValidator


SIZE_CHOICES = (
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("2XL", "2XL")
)

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description  = models.TextField(max_length=800, blank=True)
    price        = models.IntegerField(validators=[MinValueValidator(0)])
    image1 = models.ImageField(upload_to='images/products')
    image2 = models.ImageField(upload_to='images/products')
    image3 = models.ImageField(upload_to='images/products')
    image4 = models.ImageField(upload_to='images/products')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    have_size = models.BooleanField(default=False)
    size = models.CharField(max_length = 10,choices = SIZE_CHOICES,default = 'S')
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category     = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add =True)
    modified_date = models.DateTimeField(auto_now=True)
    discount_price = models.IntegerField(null=True, blank=True ,default= 0)

    def __str__(self):
        return self.name


class Categoryoffer(models.Model):
    category = models.OneToOneField(Category, related_name='category_offer', on_delete=models.CASCADE)
    discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):   
     return self.category.category_name    


class Productoffer(models.Model):
    product= models.OneToOneField(Product, related_name='product_offer', on_delete=models.CASCADE)
    discount= models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],null=True,default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):   
     return self.product.name