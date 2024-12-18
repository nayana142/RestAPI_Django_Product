
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ProductCategory,SubCategory,UnitCategory,Pricing,ProductDetails,BatchDetails
from .serializers import ProductCategorySerializer,SubCategorySerializer,UnitCategorySerializer,PricingSerializer,ProductDetailsSerializer,BatchDetailsSerializer,ProductDetailsNestedSerializer


# Create your views here.
class ProductDetailView(APIView):
    # Insert new data
    def post(self,request):
        pcategory_serializer=ProductCategorySerializer(data=request.data)
        if pcategory_serializer.is_valid():
            p_category=pcategory_serializer.save()
            psubcategory_serializer=SubCategorySerializer(data=request.data)
            if psubcategory_serializer.is_valid():
                p_subcategory=psubcategory_serializer.save(fk_category=p_category) 
                product_serializer=ProductDetailsSerializer(data=request.data)
                if product_serializer.is_valid():
                    product=product_serializer.save(fk_product_category=p_category,fk_sub_category=p_subcategory)   
                    unit_serializer=UnitCategorySerializer(data=request.data)
                    low_stock_serializer=BatchDetailsSerializer(data=request.data)          
                    price_serializer=PricingSerializer(data=request.data)
                    if unit_serializer.is_valid() and price_serializer.is_valid():            
                        unit= unit_serializer.save()
                        price_serializer.save(fk_product=product)
                        if low_stock_serializer.is_valid() :
                            low_stock_serializer.save(fk_product=product,fk_unit_category=unit)
                            return Response(
                                {
                                    "success":True,
                                    "data":{
                                        "product_category":pcategory_serializer.data,
                                        "product_subcategory":psubcategory_serializer.data,
                                        "product_details":product_serializer.data,
                                        "unit_category":unit_serializer.data,
                                        "low_stock":low_stock_serializer.data,
                                        "pricing":price_serializer.data

                                    },
                                    'message':'product created with low stock and pricing details'
                                },
                                status=status.HTTP_201_CREATED,
                            )
                        else:
                            return Response(
                                    {
                                        "success": False,
                                        "data": product_serializer.data,
                                        "message": "low stock creation failed",
                                        "error": low_stock_serializer.errors,
                                    },
                                    status=status.HTTP_201_CREATED,
                            )
                    else:
                        errors={
                            "unit_errors":unit_serializer.errors,
                            "price_errors":price_serializer.errors
                        }
                        return Response(
                                {
                                    "success": False,
                                    "data": product_serializer.data,
                                    "message": "unit and price creation failed",
                                    "error": errors
                                },
                                status=status.HTTP_201_CREATED,
                            )
                else:
                    return Response(
                        {
                            "success": False,
                            "data": None,
                            "message": "product creation failed",
                            "errors": product_serializer.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {
                        "success": False,
                        "data": None,
                        "message": "subcategory creation failed",
                        "errors": psubcategory_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
                return Response(
                    {
                        "success": False,
                        "data": None,
                        "message": "category creation failed",
                        "errors": pcategory_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
    
    # Display all data
    def get(self, request):
        try:
            products = ProductDetails.objects.all()
            serializer = ProductDetailsNestedSerializer(products, many=True)

            return Response(
                {
                    "success": True,
                    "data": serializer.data,
                    "message": "Products retrieved successfully",
                },    
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    "success": False,
                    "message": f"An error occurred: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
    # Edit 
    def put(self,request,pk):
        try:
            # Fetch the ProductDetails object 
            product = ProductDetails.objects.get(id=pk)
        except ProductDetails.DoesNotExist:
            return Response(
                {"success": False,
                 "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # product category
        pcategory_serializer = ProductCategorySerializer(product.fk_product_category, data=request.data, partial=True)
        if pcategory_serializer.is_valid():
            p_category = pcategory_serializer.save()

            # Subcategory
            psubcategory_serializer = SubCategorySerializer(product.fk_sub_category, data=request.data, partial=True)
            if psubcategory_serializer.is_valid():
                p_subcategory = psubcategory_serializer.save()

                # product details
                product_serializer = ProductDetailsSerializer(product, data=request.data, partial=True)
                if product_serializer.is_valid():
                    product = product_serializer.save(fk_product_category=p_category, fk_sub_category=p_subcategory)

                    # Fetch the related batch and unit category
                    batch = BatchDetails.objects.filter(fk_product=product).first()
                    if batch:
                        unit_serializer = UnitCategorySerializer(batch.fk_unit_category, data=request.data, partial=True)
                    else:
                        unit_serializer = UnitCategorySerializer(data=request.data)

                    # Deserialize and update pricing
                    price_serializer = PricingSerializer(product.pricing_set.first(), data=request.data, partial=True)
                    # Deserialize and update low stock details
                    low_stock_serializer = BatchDetailsSerializer(batch, data=request.data, partial=True)

                    if (unit_serializer.is_valid() and price_serializer.is_valid() and low_stock_serializer.is_valid()):
                        unit = unit_serializer.save()
                        price_serializer.save(fk_product=product)
                        low_stock_serializer.save(fk_product=product, fk_unit_category=unit)
                        
                        return Response(
                            {
                                "success": True,
                                "data": {
                                    "product_category": pcategory_serializer.data,
                                    "product_subcategory": psubcategory_serializer.data,
                                    "product_details": product_serializer.data,
                                    "unit_category": unit_serializer.data,
                                    "low_stock": low_stock_serializer.data,
                                    "pricing": price_serializer.data,
                                },
                                "message": "Product updated successfully",
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        errors = {
                            "unit_errors": unit_serializer.errors,
                            "price_errors": price_serializer.errors,
                            "low_stock_errors": low_stock_serializer.errors,
                        }
                        return Response(
                            {
                                "success": False,
                                "message": "Unit, price, or low stock update failed.",
                                "errors": errors,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response(
                        {
                            "success": False,
                            "message": "Product details update failed.",
                            "errors": product_serializer.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Subcategory update failed.",
                        "errors": psubcategory_serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Category update failed.",
                    "errors": pcategory_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
    # Delete   
    def delete(self, request, id):
        try:
            product = ProductDetails.objects.get(id=id)
        except ProductDetails.DoesNotExist:
            return Response(
                {"success": False, "message": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


    






# Create your views here.
# class ProductDetailView(APIView):
#     def post(self,request):
#         product_serializer=ProductDetailsSerializer(data=request.data)
#         if product_serializer.is_valid():
#             product=product_serializer.save()
            

#             pcategory_serializer=ProductCategorySerializer(data=request.data)
#             psubcategory_serializer=SubCategorySerializer(data=request.data)
#             unit_serializer=UnitCategorySerializer(data=request.data)
#             low_stock_serializer=LowStockAlertSerializer(data=request.data)          
#             price_serializer=PricingSerializer(data=request.data)
            

#             if pcategory_serializer.is_valid() and psubcategory_serializer.is_valid() and unit_serializer.is_valid() and low_stock_serializer.is_valid() and price_serializer.is_valid():
#                 pcategory_serializer.save()
#                 psubcategory_serializer.save()              
#                 unit= unit_serializer.save()
#                 low_stock_serializer.save(fk_product=product,unitcategory=unit)
#                 price_serializer.save(fkproduct=product)
#                 return Response(
#                     {
#                         "success":True,
#                         "data":{
#                             "product_category":pcategory_serializer.data,
#                             "product_subcategory":psubcategory_serializer.data,
#                             "product_details":product_serializer.data,
#                             "unit_category":unit_serializer.data,
#                             "low_stock":low_stock_serializer.data,
#                             "pricing":price_serializer.data

#                         },
#                         'message':'product created with low stock and pricing details'
#                     },
#                     status=status.HTTP_201_CREATED,
#                 )
#             else:
#                 errors={
#                     "product_category_errors":pcategory_serializer.errors,
#                     "product_subcategory_errors":psubcategory_serializer.errors,
#                     "unit_errors":unit_serializer.errors,
#                     "low_stock_errors":low_stock_serializer.errors,
#                     "price_errors":price_serializer.errors
#                 }
#                 return Response(
#                         {
#                             "success": True,
#                             "data": product_serializer.data,
#                             "message": "Product created without low stock and pricing details",
#                             "error": errors
#                         },
#                         status=status.HTTP_201_CREATED,
#                     )
#         else:
#                 return Response(
#                     {
#                         "success": False,
#                         "data": None,
#                         "message": "Product creation failed",
#                         "errors": product_serializer.errors,
#                     },
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )


