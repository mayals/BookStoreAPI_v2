from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
import uuid


class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True, blank=False, null=True) 
    slug        = models.SlugField(max_length=120, blank=True, null=True)
    icon        = models.ImageField(upload_to = "category/%Y/%m/%d/", blank=False, null=True)
    created_at  = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_at  = models.DateTimeField(auto_now_add=False,auto_now=True)
       
    def __str__(self):   
        return self.name 

    def get_absolute_url(self):
        return reverse('category-detail', kwargs = {'slug':self.slug})      # view_name='{model_name}-detail'

    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)  # Call the "real" save() method.       
        
    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'




class Publisher(models.Model):
    name           = models.CharField(max_length=30, null=True)
    slug           = models.SlugField(max_length=120, blank=True, null=True)
    address        = models.CharField(max_length=50, null=True)
    website        = models.URLField(null=True)
    # city           = models.CharField(max_length=60, null=True)
    # state_province = models.CharField(max_length=30, null=True)
    # country        = models.CharField(max_length=50, null=True)
   

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book-publisher', kwargs = {'slug':self.slug})   # view_name='{model_name}-detail'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)                                   # Call the "real" save() method.   

    class Meta:
        ordering = ('name',)
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'





class Author(models.Model):
    first_name = models.CharField(max_length=10, null=True)
    last_name  = models.CharField(max_length=10, null=True)
    slug       = models.SlugField(max_length=120, blank=True, null=True)
    email      = models.EmailField(null=True)
    bio        = models.TextField()
    pic        = models.ImageField(upload_to = "author/%Y/%m/%d/")
    created_at= models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at= models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f'{self.first_name} + {self.last_name}'

    def get_absolute_url(self):
        return reverse('author-detail', kwargs = {'slug':self.slug})      #vue view_name='{model_name}-detail'

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.first_name) + str(self.last_name))
        super().save(*args, **kwargs)      # Call the "real" save() method. 
    
    class Meta:
        ordering = ('first_name',)
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

     








class Review(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True , blank=False, related_name='reviews')
    book        = models.ForeignKey('Book', on_delete=models.CASCADE, null=True , blank=False, related_name='reviews')
    review_star = models.IntegerField(blank=False, null=True)
    review_text = models.TextField(blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f'{self.user.username}-{self.created_at}'



"""https://docs.djangoproject.com/en/4.0/topics/auth/customizing/#substituting-a-custom-user-model"""
class UserModel(AbstractUser):
    username        = models.CharField(max_length = 50, null = True, unique = True)
    email           = models.EmailField(unique = True, null = True)
    first_name      = models.CharField(max_length = 10, null = True)
    last_name       = models.CharField(max_length = 10 ,null = True)
    born_date       = models.DateTimeField(null = True)
    phone           = models.CharField(max_length=40, null=True)
    address         = models.CharField(max_length=200)
    created_at      = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at      = models.DateTimeField(auto_now_add=False, auto_now=True)

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']
   
    def __str__(self):
       return "{}".format(self.username)    

    class Meta:
        ordering = ('first_name',)
        verbose_name = 'UserModel'
        verbose_name_plural = 'UsersModel'






class Order(models.Model):
    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)                     
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True , blank=False, related_name='orders')
    created_at   = models.DateTimeField(auto_now_add=True, auto_now=False)   
    is_finished  = models.BooleanField(default=False)
    books        =  models.ManyToManyField('Book',through='Ordering', null=True)  
    
    def __str__(self):
        return f'{self.id}-{self.user.username}-{self.created_at}'

    def get_cost(self):
        return self.unit_price * self.quantity
    
    def get_absolute_url(self):
        return reverse('order-detail', kwargs = {'id':self.id})      #vue view_name='{model_name}-detail'
    
    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

   

class Ordering(models.Model):
    id              = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order           = models.ForeignKey(Order, on_delete=models.CASCADE, null=True , blank=False, related_name='Orderings')
    book            = models.ForeignKey('Book', on_delete=models.CASCADE, null=True , blank=False, related_name='Orderings')
    unit_price      = models.DecimalField(max_digits=10, decimal_places=2)
    quantity        = models.PositiveIntegerField(default=1)
    # payment_method  = models.CharField(max_length = 20)
    # shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE, null=True , blank=False, related_name='orders')
    is_paid         = models.BooleanField(default=False)
    
    def __str__(self):
            return f'{self.id}-{self.order.user.username}-{self.book.title }'




class Book(models.Model):
    new = 'New'
    old = 'Old'
    CONDITION_CHOICES = [
                    (new,'New'),
                    (old,'Old'),
    ]

    T = 'In Stock'
    F = 'Out Of Stock'
    STOCK_CHOICES = [
                    (T,'In Stock'),
                    (F,'Out Of Stock'),
    ]       

    id               = models.UUIDField(primary_key=True, default= uuid.uuid4, editable= False)                        
    category         = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False, related_name='books')            
    publisher        = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True , blank=False, related_name='books')
    authors          = models.ManyToManyField(Author, blank=True, null=True) 
    title            = models.CharField(max_length=100, unique=True, blank=False, null=True)
    slug             = models.SlugField(max_length=120, blank=True, null=True)
    publication_date = models.DateField(auto_now_add=True, auto_now=False, null=True)
    num_pages        = models.IntegerField(blank=True, null=True)
    price            = models.DecimalField(max_digits=5, decimal_places=2)
    coverpage        = models.FileField(upload_to = "coverpage/%Y/%m/%d/")
    bookpage         = models.FileField(upload_to = "bookpage/%Y/%m/%d/")
    condition        = models.CharField(max_length=20, choices= CONDITION_CHOICES, null=True, blank=False)
    stock            = models.CharField(max_length=20, choices= STOCK_CHOICES, null=True, blank=False)
    created_at       = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at       = models.DateTimeField(auto_now_add=False, auto_now=True)


    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs = {'slug':self.slug})   # view_name='{model_name}-detail'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)                                 # Call the "real" save() method.   

    class Meta:
        ordering = ('title',)
        verbose_name = 'Book'
        verbose_name_plural = 'Books'




class Cart(models.Model): 
    user     = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False, related_name='cart') 
    books    = models.ManyToManyField(Book)    
 
    def __str__(self):
        return str(self.user.username)