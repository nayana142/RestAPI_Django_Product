from django.db import models

# Create your models here.

from django.db import models
class ProductCategory(models.Model):
    product_category_name=models.CharField(max_length=50)


class SubCategory(models.Model):
    fk_category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    sub_category_name=models.CharField(max_length=50)


class UnitCategory(models.Model):
    unit_name=models.CharField(max_length=10)


class ProductDetails(models.Model):
    fk_product_category=models.ForeignKey(ProductCategory,on_delete=models.CASCADE)
    fk_sub_category=models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    p_title=models.CharField(max_length=50)
    p_quantity=models.IntegerField()
    p_image=models.ImageField(upload_to='productimages/',null=True)
    p_video=models.FileField(upload_to='productvideo/',null=True)
    p_description=models.TextField()
    p_brand=models.CharField(max_length=15)
    

class BatchDetails(models.Model):
    fk_product=models.ForeignKey(ProductDetails,on_delete=models.CASCADE)
    fk_unit_category=models.ForeignKey(UnitCategory,on_delete=models.CASCADE)
    low_stock_alert=models.IntegerField()
    batch_number=models.CharField(max_length=25)
    b_quantity=models.IntegerField()
    unit=models.IntegerField()          
    packet_numbers=models.IntegerField()
    created_date=models.DateField(auto_now=True)
    expiry_date=models.DateField()
    manufacture_date=models.DateField()


class Pricing(models.Model):
    fk_product=models.ForeignKey(ProductDetails,on_delete=models.CASCADE)
    selling_price=models.DecimalField(max_digits=10,decimal_places=2)
    mrp=models.DecimalField(max_digits=10,decimal_places=2)