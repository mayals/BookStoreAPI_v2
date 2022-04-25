from rest_framework import serializers
from .models import Category, Book, Publisher, Author, Review, UserModel, Order, Ordering, Cart
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse







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
    
    icon = serializers.ImageField(required=True, validators=[
                                                            required,
                                                            UniqueValidator(queryset=Category.objects.all())
                                                            ]
                                )
    # books = serializers.HyperlinkedRelatedField(many=True, read_only=True,  view_name='book-detail')                            
    books = serializers.HyperlinkedIdentityField(many=True, read_only=True,  view_name='book-detail',lookup_field='slug') 
   
    class Meta:
        model = Category
        fields = ['id','slug','name','url','icon','created_at','updated_at','books']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                    'books': {
                              'read_only'    : True,
                              'view_name'    : 'book-detail',
                              'lookup_field' : 'id' 
                            },
                    'url'  : {
                               'read_only'    : True,
                               'view_name'    : 'books_api:category-detail',
                               'lookup_field' : 'slug'     
                            },                      
                    }






################################################### AuthorSerializer #####################################################
class AuthorSerializer(serializers.ModelSerializer):
    
    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')

    def textarea_config(value):
        if value is None:
            raise serializers.ValidationError('This field is required')
        mytext = str(value)
        if len(mytext) > 10  or  len(mytext) < 5 :                         # url.hostname     "www.example.com"
            raise serializers.ValidationError('please enter   10 > text > 5')
       

    first_name  = serializers.CharField(required=True, validators=[required])
                                                                 
    last_name  = serializers.CharField(required=True, validators=[required])
                                                                                                                                                  
    url   = serializers.HyperlinkedIdentityField(read_only=True, view_name="author-detail",lookup_field='slug')  
                                                       
    pic = serializers.ImageField(required=True, validators=[required])
                                                           
    bio = serializers.CharField(required=True, validators=[required,textarea_config])                                                                       
       

    class Meta:
        model = Author
        fields = ['id','slug','first_name','last_name','email','url','pic','bio','created_at','updated_at']
        extra_kwargs = {
                    'id'         : {'read_only': True },
                    'slug'       : {'read_only': True },
                    'first_name' : {'required' : True },    # required
                    'last_name'  : {'required' : True },    # required
                    'email'      : {'required' : True },    # required
                    'bio'        : {'required' : True },    # required
                    'pic'        : {'required': True },     # required
                    'url'        : {
                                    'read_only'    : True,
                                    'view_name'    : 'books_api:author-detail',
                                    'lookup_field' : 'slug'     
                                 },                  
                    } 




###################################################[ BookSerializer ]#####################################################
class BookSerializer(serializers.ModelSerializer):
    def required(value):
            if value is None:
                raise serializers.ValidationError('This field is required')

    
    
    # this foreignkey field :to show category_id  for each book object as readable (as word - not number):
    category = serializers.SlugRelatedField(
                            queryset = Category.objects.all(),
                            slug_field = 'name'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    
    title  = serializers.CharField(required=True, validators=[
                                                            required,
                                                            UniqueValidator(queryset=Book.objects.all())
                                                            ]
                                )
    url   = serializers.HyperlinkedIdentityField(read_only=True, view_name="book-detail",lookup_field='slug')  
    
    
    publisher = serializers.SlugRelatedField(
                            queryset = Publisher.objects.all(),
                            slug_field = 'name'  # to display category_id asredable  use name field  insead of id field 
                            ) 
    
                   
    authors = AuthorSerializer(read_only=True, many=True)                  # many to many relations field
    
    coverpage = serializers.ImageField(required=True, validators=[required])
    bookpage = serializers.ImageField(required=True, validators=[required])
    condition  = serializers.CharField(required=True, validators=[required])                     
    stock = serializers.CharField(required=True, validators=[required,])
    
    
        
    class Meta:
        model = Book
        fields = [
                'id','url','category','title','publisher','authors',
                'slug','publication_date','num_pages','price',
                'coverpage','bookpage','condition','stock','created_at','updated_at',
                  ]
        
 
       
        extra_kwargs = {
                    'id'   : {'read_only': True },
                    'slug' : {'read_only': True },
                    'category': {'required' : True },                     # required
                    'title' : {'required' : True },                       # required
                    'publisher' : {'required' : True },                   # required
                    'authors' : {'required' : True },                     # required
                    'publication_date' : {'required' : True },            # required
                    'num_pages' : {'required' : True },                   # required
                    'price' : {'required' : True },                       # required
                    'coverpage' : {'required' : True },                   # required
                    'bookpage' : {'required' : True },                    # required
                    'condition' : {'required' : True },                   # required
                    'stock' : {'required' : True },                       # required
                   
                    'url'  : {
                            'read_only'    : True,
                            'view_name'    : 'books_api:book-detail',       # 'applicationname:basename'
                            'lookup_field' : 'id'     
                            },                      
                    }








################################################### PublisherSerializer #####################################################
class PublisherSerializer(serializers.ModelSerializer):
    def required(value):
        if value is None:
            raise serializers.ValidationError('This field is required')
    
    def validate_url(value):
        if value is None:
            raise serializers.ValidationError('This field is required')
        obj = urlparse(value)
        if 'com' not in obj.hostname or 'www' not in obj.hostname :   # url.hostname     "www.example.com"
            raise serializers.ValidationError('please enter valid website url')
       

    name  = serializers.CharField(required=True, validators=[
                                                            required,
                                                            UniqueValidator(queryset=Publisher.objects.all())
                                                            ]
                                )
    url   = serializers.HyperlinkedIdentityField(read_only=True, view_name="publisher-detail",lookup_field='slug')
    website = serializers.CharField(required=True, validators=[validate_url])
    address = serializers.CharField(required=True)
    books = serializers.HyperlinkedRelatedField(many=True, read_only=True,  view_name='book-detail',lookup_field='slug') 
    # books = BookSerializer()
    class Meta:
        model = Publisher
        fields = ['id','slug','name','url','address','website','created_at','updated_at','books']
        extra_kwargs = {
                    'name' : {'required' : True },
                    'address' : {'required' : True },
                    'website' : {'required' : True },

                    'id'   : {'read_only': True },

                    'slug' : {'read_only': True },
                    
                    'url'  : {
                               'read_only'    : True,
                               'view_name'    : 'books_api:publisher-detail',
                               'lookup_field' : 'slug'     
                            },

                    'books': {
                              'read_only'    : True,
                              'view_name'    : 'book-detail',
                              'lookup_field' : 'id' 
                            }                      
                    } 






################################################### ReviewSerializer #####################################################

################################################### UserModelSerializer #####################################################


################################################### OrderSerializer #####################################################


################################################### OrderingSerializer #####################################################


################################################### CartSerializer #####################################################
