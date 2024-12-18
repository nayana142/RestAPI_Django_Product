from rest_framework import serializers
from .models import ProductDetails,ProductCategory,SubCategory,UnitCategory,Pricing,BatchDetails


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductCategory
        fields='__all__'
       

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=SubCategory
        fields='__all__'
        extra_kwargs={
            'fk_category':{'read_only':True}
        }

class UnitCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=UnitCategory
        fields='__all__'

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductDetails
        fields='__all__'
        extra_kwargs={
            'fk_product_category':{'read_only':True},
            'fk_sub_category':{'read_only':True}
        }

class BatchDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=BatchDetails
        fields='__all__'
        extra_kwargs={
            
            'fk_product':{'read_only':True},
            'fk_unit_category':{'read_only':True}
        }
class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pricing
        fields='__all__'
        extra_kwargs={
            'fk_product':{'read_only':True}
        }


# class ProductDetailsNestedSerializer(serializers.ModelSerializer):
#     fk_product_category = ProductCategorySerializer()
#     fk_sub_category = SubCategorySerializer()
#     batchdetails_set = BatchDetailsSerializer(many=True)
#     pricing_set = PricingSerializer(many=True)

#     class Meta:
#         model = ProductDetails
#         fields = '__all__'

class ProductDetailsNestedSerializer(serializers.ModelSerializer):
    product_category = serializers.SerializerMethodField()
    product_subcategory = serializers.SerializerMethodField()
    pricing = serializers.SerializerMethodField()
    batches = serializers.SerializerMethodField()
    unit_category = serializers.SerializerMethodField()

    class Meta:
        model = ProductDetails
        fields = '__all__'  
        
    # Create custom method to retrieve and serialize related data.

    def get_product_category(self, obj):
        return ProductCategorySerializer(obj.fk_product_category).data

    def get_product_subcategory(self, obj):
        return SubCategorySerializer(obj.fk_sub_category).data

    def get_pricing(self, obj):
        pricing = Pricing.objects.filter(fk_product=obj)
        return PricingSerializer(pricing, many=True).data

    def get_batches(self, obj):
        batch = BatchDetails.objects.filter(fk_product=obj)
        return BatchDetailsSerializer(batch, many=True).data

    def get_unit_category(self, obj):
        unit = UnitCategory.objects.filter(batchdetails__fk_product=obj)
        return UnitCategorySerializer(unit, many=True).data
