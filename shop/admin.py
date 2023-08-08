from django.contrib import admin
from shop.models import Product,ProductImage,ProductPrice,ProductDiscountTax,ProductUnit,ProductStock,ProductVisibility,ProductStok,ProductVisibility,Reg,Log,AddcartProduct,Payment,address,paydetails

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductPrice)
admin.site.register(ProductDiscountTax)
admin.site.register(ProductUnit)
admin.site.register(ProductStock)
admin.site.register(ProductVisibility)
admin.site.register(ProductStok)
admin.site.register(Reg)
admin.site.register(Log)
admin.site.register(AddcartProduct)
admin.site.register(Payment)
admin.site.register(address)
admin.site.register(paydetails)



