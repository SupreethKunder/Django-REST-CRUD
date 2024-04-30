from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from . import validators


class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field = 'pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)
    

class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    other_products = serializers.SerializerMethodField(read_only=True)
    
    def get_other_products(self,obj):
        print(obj)
        user=obj
        my_products_qs = user.product_set.all()[:5]
        return UserProductInlineSerializer(my_products_qs,many=True,context=self.context).data

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk", read_only=True
    )
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source="user", read_only=True)
    # related_products = ProductInlineSerializer(
    #     source="user.product_set.all", read_only=True,many=True
    # )
    # my_user_data = serializers.SerializerMethodField(read_only=True)
    # my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail", lookup_field="pk"
    )
    title = serializers.CharField(
        validators=[validators.validate_title_no_yo, validators.unique_product_title]
    )
    body = serializers.CharField(source='content')
    # email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Product
        fields = [
            # 'user',
            "owner",
            "url",
            "edit_url",
            "pk",
            "title",
            # 'name',
            'body',
            # "content",
            "price",
            "sale_price",
            # "my_discount",
            # "my_user_data",
            # "related_products",
        ]

    def get_my_user_data(self, obj):
        return {"username": obj.user.username}

    # def validate_title(self, value):
    #     request = self.context.get('request')
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name.")
    #     return value

    # def create(self, validated_data):
    #     # return Product.obejcts.create(**validated_data)
    #     # email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     # print(email, obj)
    #     return obj

    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)

    def get_edit_url(self, obj):
        request = self.context.get("request")  # self.request
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    # def get_my_discount(self, obj):
    #     if not hasattr(obj, "id"):
    #         return None
    #     if not isinstance(obj, Product):
    #         return None
    #     return obj.get_discount()
