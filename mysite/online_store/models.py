from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):

    age = models.PositiveSmallIntegerField(default =0, null=True,blank=True)
    country = models.CharField(max_length=32,null=True,blank=True)
    phono_number = models.IntegerField(null=True,blank=True)
    date_registered = models.DateField(auto_now= True ,null=True,blank=True)
    STATUS_CHOICES = (
        ('gold','Gold'),
        ('silver','Silver') ,
        ('bronze','Bronze'),
        ('simple','Simple'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='simple')


    def __str__(self):
        return f'{self.first_name} - {self.last_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


class Pattern(models.Model):
    PATTERN = (
        ('pattern 1' , 'pattern 1'),
        ('pattern 2 ','pattern 2 '),
    )
    patterns = models.CharField(max_length=25,choices=PATTERN)


class Product(models.Model):
    product_name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(Category,related_name='product', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    active =  models.BooleanField(default=True,verbose_name='в наличии')
    product_video = models.FileField(verbose_name='Видео',upload_to='vid/' , null=True , blank=True)
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    pattern = models.ForeignKey(Pattern,on_delete=models.CASCADE)


    def __str__(self):
        return self.product_name

    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return round(sum(rating.stars for rating in ratings) / ratings.count(), 1)
        return 0


class Consultation_Keys(models.Model):
    consultation = models.ForeignKey(Product, related_name='product_keys', on_delete=models.CASCADE)
    keys = models.CharField(max_length=512)


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product,related_name='product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='phoduct_images/')

#
# class Rating(models.Model):
#     product = models.ForeignKey(Product,related_name='ratings', on_delete=models.CASCADE)
#     user = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
#     stars = models.IntegerField(choices=[(i, str(i)) for i in range(1,6) ], verbose_name='Рейтинг ')
#
#     def __str__(self):
#         return f'{self.user} - {self.product} - {self.stars} stars'
#
#
#
# class Review(models.Model):
#     author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name='reviews',on_delete=models.CASCADE)
#     text = models.TextField()
#     created_date = models.DateTimeField(auto_now_add=True)
#     parent_review = models.ForeignKey('self', related_name='replies', null=True, blank=True, on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return f'{self.author} - {self.text}'
#
#
# class Cart(models.Model):
#     user = models.OneToOneField(UserProfile,on_delete=CASCADE)
#     created_date = models.DateField(auto_now_add=True)
#
#
#     def __str__(self):
#         return f'{self.user}'
#
#     def get_total_price(self):
#         return sum(item.get_total_price() for item in self.items.all())
#
#
# class CarItem(models.Model):
#     cart = models.ForeignKey(Cart,related_name='items',on_delete=CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveSmallIntegerField(default=1)
#
#     def get_total_price(self):
#         return self.product.price * self.quantity
