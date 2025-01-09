
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'date_registered', 'phono_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','last_name']

class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


# class ReviewSerializer(serializers.ModelSerializer):
#     author = UserProfileSerializer()
#     created_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
#     class Meta:
#         model =  Review
#         fields = ['id','author','text','created_date']




# class RatingSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer()
    # class Meta:
    #     model = Rating
    #     fields = ['user','stars']

class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ['photo']


class ProductListSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%Y-%m-%d')

#    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id','product_name','date']
    #

class CategorySerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True,many=True)
    class Meta:
        model = Category
        fields = ['category_name','product']


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']
    # def get_average_rating(self, obj):
    #     return obj.get_average_rating()
class Consultation_KeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation_Keys
        fields = ['consultation','keys']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer()
    # ratings = RatingSerializer(read_only=True,many=True)
    # reviews = ReviewSerializer(read_only=True,many=True)
    product = ProductPhotosSerializer(read_only=True,many=True)
    date = serializers.DateTimeField(format='%d-%m-%Y')
    # average_rating = serializers.SerializerMethodField()
    owner = UserProfileSerializer()
    class Meta:
        model = Product

        fields = ['product_name','category','description','price','product_video',
                  'active','date', 'product']

        # def get_average_rating(self, obj):
        #     return obj.get_average_rating()





#
# class UserProfileAllSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
#
# class CartItemSerializer(serializers.ModelSerializer):
#     product = ProductListSerializer(read_only=True)
#     product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),write_only=True,source='product')
#
#     class Meta:
#         model = CarItem
#         fields = ['id','product','product_id','get_total_price']
#
# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True,read_only=True)
# #    total_price = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Cart
#         fields = ['id','user','items','total_price']
#
#     #
#     # def get_total_price(self,obj):
#     #     return obj.get_total_price