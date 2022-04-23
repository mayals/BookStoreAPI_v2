from rest_framework import serializers
from .models import Category, Book, Publisher, Author, Review, UserModel, Order, Ordering, Cart
from rest_framework.validators import UniqueValidator



###################################################[ BookSerializer ]#####################################################
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
                'id','category','publisher','authors','title',
                'slug','publication_date','num_pages','price',
                'coverpage','bookpage','condition','stock','created_at','updated_at',
                  ]








###################################################[ CategorySerializer ]#####################################################
class CategorySerializer(serializers.ModelSerializer):
    
    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')

    name  = serializers.CharField(required=True, validators=[
                                                            required,
                                                            UniqueValidator(queryset=Category.objects.all())
                                                            ]
                                )
    url   = serializers.HyperlinkedIdentityField(read_only=True, view_name="category-detail",lookup_field='slug')  
    books = serializers.HyperlinkedRelatedField(many=True, read_only=True,  view_name='book-detail')
    icon = serializers.ImageField(required=True, validators=[
                                                            required,
                                                            UniqueValidator(queryset=Category.objects.all())
                                                            ]
                                )
    class Meta:
        model = Category
        fields = ['id','slug','name','url','icon','created_at','updated_at','books']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                    'books': {
                              'read_only'    : True,
                              'view_name'    : 'category-detail',
                              'lookup_field' : 'id' 
                            },
                    'url'  : {
                               'read_only'    : True,
                               'view_name'    : 'books_api:category-detail',
                               'lookup_field' : 'slug'     
                            },                      
                    }




################################################### CategorySerializer #####################################################
