from django.shortcuts import render, redirect
from shop.models import Product, ProductImage, ProductPrice, ProductDiscountTax, ProductUnit, ProductStock,ProductVisibility,ProductStok,Reg,Log,AddcartProduct,Payment,address,paydetails
from django.contrib import messages
from .forms import ProductForm
from .forms1 import editProductForm
from .forms2 import registerForm, loginForm
from django.forms.utils import ErrorDict
from django.db import IntegrityError
import datetime
import os
import uuid
import socket
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse


def create(request):
    if request.method == 'POST':
        forms = ProductForm(request.POST ,request.FILES)
        if forms.is_valid():
            product = Product(
                name=forms.cleaned_data['name'],
                unit=forms.cleaned_data['unit'],
                slug=forms.cleaned_data['slug'],
                description=forms.cleaned_data['description'],
                short_description=forms.cleaned_data['short_description'],
                visibility=forms.cleaned_data['visibility'],
                publish_date=forms.cleaned_data['publish_date'],)
            existing_slugs = Product.objects.exclude(deleted_at__isnull=True).values_list('slug', flat=True)
            if product.slug in existing_slugs:
                errors = forms.errors.setdefault('slug', ErrorDict())
                errors[""] = forms.error_class(["Slug should be unique."])
            try:
                product.save()  # Save the product to the database
                print(product.id)
            except Exception as e:
                print(f"Error saving product: {e}")
 


            
             
            images = []
           
            if forms.cleaned_data['image1']:
                image1 = {'image': forms.cleaned_data['image1'], 'alt': forms.cleaned_data['alt1']}
                images.append(image1)
                if forms.cleaned_data['image2']:
                    image2 = {'image': forms.cleaned_data['image2'], 'alt': forms.cleaned_data['alt2']}
                    images.append(image2)
                    if forms.cleaned_data['image3']:
                        image3 = {'image': forms.cleaned_data['image3'], 'alt': forms.cleaned_data['alt3']}
                        images.append(image3)
                        for image in images:
                            product_image = ProductImage(
                                Product_id=product.id,
                                image=image['image'], alt=image['alt'])
                            
                            product_image.save()



            price = ProductPrice(
                Product_id=product.id,
                price=forms.cleaned_data['price'])
            price.save()

            discount_tax = ProductDiscountTax(
                Product_id=product.id,
                discount=forms.cleaned_data['discount'],
                tax=forms.cleaned_data['tax'])
            discount_tax.save()

            selected_unit = forms.cleaned_data['unit']

            # Map the selected unit choice to the corresponding value
            unit_mapping = {
                '1': 'Qty',
                '2': 'Ltr',
                '3': 'ML',
                '4': 'KG',
                '5': 'GM',
                '6': 'meter',
            }
            unit_name = unit_mapping.get(selected_unit)
   
            unit = ProductUnit(
                Product_id=product.id,
                units=unit_name)
            
            unit.save()

            selected_visibility = forms.cleaned_data['visibility']
            visibility_mapping = {
                '1': 'published',
                '2': 'hidden',
                
            }
            visibility = visibility_mapping.get(selected_visibility)
   
            visibility = ProductVisibility(
                Product_id=product.id,
                visibility=visibility)
            
            visibility.save()


            selected_stok= forms.cleaned_data['Stock']
            stok_mapping = {
                '1': 'in_stock',
                '2': 'out_of_stock',
                
            }
            stok= stok_mapping.get(selected_stok)
   
            stok = ProductStok(
                Product_id=product.id,
                stock=stok)
            
            stok.save()




            stock = ProductStock(
                Product_id=product.id,
                stock=forms.cleaned_data['Stock'],
                stockqty=forms.cleaned_data['stockqty'])
            stock.save()
            
            messages.success(request, "Data Saved")
            forms = ProductForm()

    else:
        forms = ProductForm()
    return render(request, 'shop/create.html', {'forms': forms})



def products(request):
    return render(request, "shop/products.html")

def pro(request):
    products = Product.objects.all()
    merged_data = []
    images = []
    prices = []
    discount_taxes = []
    units = []
    stocks = []
    visibility = []
    stoks = []

  
    for product in products:
        if product.deleted_at == None:
            images = ProductImage.objects.filter(Product_id=product.id)
            prices = ProductPrice.objects.filter(Product_id=product.id)
            discount_taxes = ProductDiscountTax.objects.filter(Product_id=product.id)
            units = ProductUnit.objects.filter(Product_id=product.id)
            stocks = ProductStock.objects.filter(Product_id=product.id)
            visibility = ProductVisibility.objects.filter(Product_id=product.id)
            stoks= ProductStok.objects.filter(Product_id=product.id)
        
            merged_data.append((product, images, prices, discount_taxes, units, stocks,visibility,stoks))
    
    return render(request, "shop/pro.html", {'merged_data': merged_data})



def edit(request, id):

    # Retrieve the product instance from the database based on the ID
    product = Product.objects.get(id=id)
    images = ProductImage.objects.filter(Product_id=product.id)
    prices = ProductPrice.objects.filter(Product_id=product.id).latest('id')
    discount_taxes = ProductDiscountTax.objects.filter(Product_id=product.id).latest('id')
    stock = ProductStock.objects.filter(Product_id=product.id).latest('id')
    if request.method == 'POST':
        forms1 = editProductForm(request.POST, request.FILES)
        if forms1.is_valid():
            try:
                product = Product.objects.get(id=id)  
                product.slug = request.POST.get('slug')
                product.name = request.POST.get('name')
                product.unit = request.POST.get('unit')
                product.description = request.POST.get('description')
                product.short_description = request.POST.get('short_description')
                product.visibility = request.POST.get('visibility')
                product.publish_date = request.POST.get('publish_date')
            
                product.save()


                Images = ProductImage.objects.filter(Product_id=product.id)
                if forms1.cleaned_data['image1']:
                    image1 = request.FILES.get('image1')
                    alt1 = request.POST.get('alt1')
                    if len(Images) > 0:
                        if image1 and Images[0].image != image1:
                            Images[0].image = image1
                        if alt1 and Images[0].alt != alt1:
                            Images[0].alt = alt1
                            Images[0].save()
                    else:
                        new_image = ProductImage(Product_id=product.id, image=image1, alt=alt1)
                        new_image.save()
                elif forms1.cleaned_data['alt1']:
                    alt1 = request.POST.get('alt1')
                    if len(Images) > 0 and Images[0].alt != alt1:
                        Images[0].alt = alt1
                        Images[0].save()        

                if forms1.cleaned_data['image2']:
                    image2 = request.FILES.get('image2')
                    alt2 = request.POST.get('alt2')
                    if len(Images) > 1:
                        if image2 and Images[1].image != image2:
                            Images[1].image = image2
                        if alt2 and Images[1].alt != alt2:
                            Images[1].alt = alt2
                        Images[1].save()
                    elif len(Images) == 1:
                        new_image = ProductImage(Product_id=product.id, image=image2, alt=alt2)
                        new_image.save()
                elif forms1.cleaned_data['alt2']:
                    alt1 = request.POST.get('alt2')
                    if len(Images) > 1 and Images[1].alt != alt1:
                        Images[1].alt = alt1
                        Images[1].save()              

                if forms1.cleaned_data['image3']:
                    image3 = request.FILES.get('image3')
                    alt3 = request.POST.get('alt3')
                    if len(Images) > 2:
                        if image3 and Images[2].image != image3:
                            Images[2].image = image3
                        if alt3 and Images[2].alt != alt3:
                            Images[2].alt = alt3
                        Images[2].save()
                    elif len(Images) == 2:
                        new_image = ProductImage(Product_id=product.id, image=image3, alt=alt3)
                        new_image.save()
                elif forms1.cleaned_data['alt3']:
                    alt1 = request.POST.get('alt3')
                    if len(Images) > 2 and Images[2].alt != alt1:
                        Images[2].alt = alt1
                        Images[2].save()      


                price = ProductPrice(
                    Product_id=product.id,
                    price=forms1.cleaned_data['price'])
                price.save()


                discount_tax = ProductDiscountTax(
                    Product_id=product.id,
                    discount=forms1.cleaned_data['discount'],
                    tax=forms1.cleaned_data['tax'])
                discount_tax.save()

                selected_unit = forms1.cleaned_data['unit']
                # Map the selected unit choice to the corresponding value
                unit_mapping = {
                    '1': 'Qty',
                    '2': 'Ltr',
                    '3': 'ML',
                    '4': 'KG',
                    '5': 'GM',
                    '6': 'meter',
                }
                unit_name = unit_mapping.get(selected_unit)
                unit = ProductUnit(
                Product_id=product.id,
                units=unit_name)
                unit.save()

                selected_visibility = forms1.cleaned_data['visibility']
                visibility_mapping = {
                    '1': 'published',
                    '2': 'hidden',
                }
                visibility = visibility_mapping.get(selected_visibility)
                visibility = ProductVisibility(
                    Product_id=product.id,
                    visibility=visibility)
                visibility.save()

                selected_stok= forms1.cleaned_data['Stock']
                stok_mapping = {
                    '1': 'in_stock',
                    '2': 'out_of_stock',
                }
                stok= stok_mapping.get(selected_stok)
                stok = ProductStok(
                    Product_id=product.id,
                    stock=stok)
                stok.save()
                stock = ProductStock(
                    Product_id=product.id,
                    stock=forms1.cleaned_data['Stock'],
                    stockqty=forms1.cleaned_data['stockqty'])
                stock.save()
                messages.success(request, "Data Saved")
                forms1 = editProductForm()

                

            except IntegrityError:
                existing_slugs = Product.objects.exclude(id=id).values_list('slug', flat=True)
                if products.slug in existing_slugs:
                    errors = forms1.errors.setdefault('slug', ErrorDict())
                    errors[""] = forms1.error_class(["Slug should be unique."])

                                                                                                    
    else:
        forms1 = editProductForm(initial={
            'name': product.name,
            'unit': product.unit,
            'slug': product.slug,
            'description': product.description,
            'short_description': product.short_description,
            'image1': images[0].image.url if images.exists() else None,
            'alt1': images[0].alt,
            'image2': images[1].image.url if images.count() > 1 else None,
            'alt2': images[1].alt,
            'image3': images[2].image.url if images.count() > 2 else None,
            'alt3': images[2].alt,
            'visibility': product.visibility,
            'publish_date': product.publish_date,
            'price': prices.price,
            'discount': discount_taxes.discount,
            'tax': discount_taxes.tax,
            'Stock': stock.stock,
            'stockqty': stock.stockqty
        })

    
    context = {
        'forms1': forms1,
        'product': product
    }
    return render(request, 'shop/edit.html', context)




from datetime import datetime
from django.shortcuts import redirect, render
from .models import Product

def delete(request, id):
    if request.method == 'POST':
        product = Product.objects.get(id=id)
        product.deleted_at = datetime.now()
        product.save()
        return redirect('/pro')  # Redirect to the desired page after deletion
    
    return render(request, "shop/pro.html")


def duplicate(request, id):
    if request.method == 'POST':
        original_product = Product.objects.get(id=id)

        # Generate a unique slug based on the existing name
        new_slug = original_product.name
        counter = 1
        while Product.objects.filter(slug=new_slug).exists():
            new_slug = f"{original_product.name}-{counter}"
            counter += 1

        # Create a new product instance with the duplicated data
        new_product = Product(
            name=original_product.name,
            slug=new_slug,
            unit=original_product.unit,
            description=original_product.description,
            short_description=original_product.short_description,
            visibility=original_product.visibility,
            publish_date=original_product.publish_date,
            
            # Add other fields as needed
        )

        # Save the new product instance
        new_product.save()       


        Images = ProductImage.objects.filter(Product_id=original_product.id)
        for image in Images:
            new_image =ProductImage(Product_id=new_product.id,image=image.image, alt=image.alt)
            new_image.save()

        DiscountTax = ProductDiscountTax.objects.filter(Product_id=original_product.id)
        for discount_tax in DiscountTax:
            new_discount_tax = ProductDiscountTax(Product_id=new_product.id, discount=discount_tax.discount, tax=discount_tax.tax)
            new_discount_tax.save()

        price=ProductPrice.objects.filter(Product_id=original_product.id)
        for price in price:
            new_price = ProductPrice(Product_id=new_product.id, price=price.price)
            new_price.save()

        stock=ProductStock.objects.filter(Product_id=original_product.id)
        for stock in stock:
            new_stock = ProductStock(Product_id=new_product.id, stock=stock.stock, stockqty=stock.stockqty)
            new_stock.save()

        stok=ProductStok.objects.filter(Product_id=original_product.id)
        for stok in stok:
            new_stok = ProductStok(Product_id=new_product.id, stock=stok.stock)
            new_stok.save()


        unit=ProductUnit.objects.filter(Product_id=original_product.id)
        for unit in unit:
            new_unit = ProductUnit(Product_id=new_product.id, units=unit.units)
            new_unit.save()


        visibility=ProductVisibility.objects.filter(Product_id=original_product.id)
        for visibility in visibility:
            new_visibility = ProductVisibility(Product_id=new_product.id, visibility=visibility.visibility)
            new_visibility.save()

        return redirect('/pro')

    return render(request, "shop/pro.html")

def register(request):
    forms2 = registerForm()  # Initialize with a default value

    if request.method == 'POST':
        forms2 = registerForm(request.POST)
        if forms2.is_valid():
            try:                
                password = forms2.cleaned_data['password']
                conform_password = forms2.cleaned_data['confirm_password']
                email = forms2.cleaned_data['email']
                phone= forms2.cleaned_data['mobilenumber']
                
                if conform_password!=password:
                    errors = forms2.errors.setdefault('conform_password', ErrorDict())
                    errors[""] = forms2.error_class(["Password does not match."])
                if Reg.objects.filter(email=email).exists():
                    errors = forms2.errors.setdefault('email', ErrorDict())
                    errors[""] = forms2.error_class(["Email already exists."])
                if Reg.objects.filter(phone=phone).exists():
                    errors = forms2.errors.setdefault('mobilenumber', ErrorDict())
                    errors[""] = forms2.error_class(["Mobile number already exists."])    
                else:
                    registeration=Reg(
                        name=forms2.cleaned_data['name'],
                        email=forms2.cleaned_data['email'],
                        phone=forms2.cleaned_data['mobilenumber'],
                        password=forms2.cleaned_data['password'],
                        confirm_password=forms2.cleaned_data['confirm_password']
                    )
                    registeration.save()
                    return redirect('/login')
            except IntegrityError:
                # Handle integrity error if needed
                pass

    return render(request, "shop/register.html", {'forms2': forms2})


def login(request):
    forms3 = loginForm()
    if request.method == 'POST':        
        forms3 = loginForm(request.POST)
        if forms3.is_valid():
            try:
                email = forms3.cleaned_data['email']
                password = forms3.cleaned_data['password']
                if Reg.objects.filter(email=email).exists():
                    user = Reg.objects.get(email=email)
                    if user.password == password:
                        request.session['user_id'] = user.id
                        log=Log(
                            userid=user.id,
                            email=forms3.cleaned_data['email'],
                            password=forms3.cleaned_data['password'],
                            login_time=datetime.now(),
                            ip_address=request.META.get('REMOTE_ADDR'),
                            device_name=socket.gethostname(),
                            logout_datetime=None,
                            mac_address=uuid.getnode(),
                            osName=os.name)
                        log.save()
                        return redirect('/purchase')        
                    else:
                        errors = forms3.errors.setdefault('password', ErrorDict())
                        errors[""] = forms3.error_class(["Password does not match."])
                else:
                    errors = forms3.errors.setdefault('email', ErrorDict())
                    errors[""] = forms3.error_class(["Email does not exist."])
                    
            except IntegrityError:
                # Handle integrity error if needed  
                pass                  
    return render(request, "shop/login.html", {'forms3': forms3})


def purchase(request):
 
    products = Product.objects.all()
    merged_data = []
    images = []
    prices = []
    discount_taxes = []
    units = []
    stocks = []
    visibility = []
    stoks = []

  
    for product in products:
        if product.deleted_at == None:
            images = ProductImage.objects.filter(Product_id=product.id)
            prices = ProductPrice.objects.filter(Product_id=product.id)
            discount_taxes = ProductDiscountTax.objects.filter(Product_id=product.id)
            units = ProductUnit.objects.filter(Product_id=product.id)
            stocks = ProductStock.objects.filter(Product_id=product.id)
            visibility = ProductVisibility.objects.filter(Product_id=product.id)
            stoks= ProductStok.objects.filter(Product_id=product.id)
            

        
            merged_data.append((product, images, prices, discount_taxes, units, stocks,visibility,stoks))
    
    return render(request, "shop/purchase.html", {'merged_data': merged_data,'user_id': request.user.id})


def AddToCart(request,id):
    user_id = request.session.get('user_id')
    if user_id:
        product = Product.objects.get(id=id)
        user = Log.objects.get(id=user_id)
                # Check if the product already exists in the AddcartProduct model
        try:
            if AddcartProduct.objects.filter(product_id=product.id, user_id=user.id).exists():
                qty = AddcartProduct.objects.get(product_id=product.id, user_id=user.id).qty + 1
                AddcartProduct.objects.filter(product_id=product.id, user_id=user.id).update(qty=qty)
            else:
                AddcartProduct.objects.create(product_id=product.id, user_id=user.id, qty=1)
        except:
            pass        
        return redirect('/purchase')
    else:
        # Handle the case when user ID is not found in the session
        return redirect('/login')
    
def Cart(request):
    user_id = request.session.get('user_id')
    if user_id:
        products = AddcartProduct.objects.filter(user_id=user_id)

        if len(products) == 0:
            print("Cart is empty")
        else:
            merged_data = []
            final=0

            for product in products:
                pro = Product.objects.get(id=product.product_id)
                images = ProductImage.objects.filter(Product_id=product.product_id)
                prices = ProductPrice.objects.filter(Product_id=product.product_id)
                discount_taxes = ProductDiscountTax.objects.filter(Product_id=product.product_id)
                quantity = AddcartProduct.objects.filter(product_id=product.product_id)
                total_price = prices[0].price * quantity[0].qty
                total_discount = (discount_taxes[0].discount / 100) * total_price
                total_tax = (discount_taxes[0].tax / 100) * total_price
                total = total_price - total_discount + total_tax
                
                final+=total


                merged_data.append((pro,images, total_price , discount_taxes, quantity,prices,total))

            return render(request, "shop/cart.html", {'merged_data': merged_data, 'final':final, 'user_id': user_id})
        
    return render(request, "shop/cart.html")


def update_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('qty')

        try:
            cart_product = AddcartProduct.objects.get(product_id=product_id)
            cart_product.qty = quantity
            cart_product.save()
            return JsonResponse({'qty': cart_product.qty})
        except AddcartProduct.DoesNotExist:
            return JsonResponse({'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'error': 'Error updating quantity: ' + str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    

def remove_from_cart(request, id):
    if request.method == 'POST':
        try:
            cart_product = AddcartProduct.objects.get(product_id=id)
            cart_product.delete()
            return redirect('/Cart')
        except AddcartProduct.DoesNotExist:
            return JsonResponse({'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'error': 'Error updating quantity: ' + str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})

                        
def BuyNow(request, id):
    merged_data = []
    product = Product.objects.get(id=id)
    images = ProductImage.objects.filter(Product_id=id)
    quantity = AddcartProduct.objects.filter(product_id=id)
    prices = ProductPrice.objects.filter(Product_id=id)
    discount_taxes = ProductDiscountTax.objects.filter(Product_id=id)

    # Check if the lists are not empty before accessing their elements
    if prices.exists() and quantity.exists() and discount_taxes.exists():
        total_price = prices[0].price * quantity[0].qty
        total_discount = (discount_taxes[0].discount / 100) * total_price
        total_tax = (discount_taxes[0].tax / 100) * total_price

        final = total_price - total_discount + total_tax
        qty = quantity[0].qty
        discount = discount_taxes[0].discount
        tax = discount_taxes[0].tax

        merged_data.append((product, images, total_price, quantity))
        return render(request, "shop/buynow.html", {'merged_data': merged_data,'product': product, 'final': final, 'qty': qty,'quantity':quantity[0].qty, 'discount': discount, 'tax': tax})
    else:
        merged_data = []
        product = Product.objects.get(id=id)
        images = ProductImage.objects.filter(Product_id=id)
        prices = ProductPrice.objects.filter(Product_id=id)
        discount_taxes = ProductDiscountTax.objects.filter(Product_id=id)
        quantity=1
        discount = discount_taxes[0].discount
        tax = discount_taxes[0].tax

        total_price = prices[0].price * quantity
        total_discount = (discount_taxes[0].discount / 100) * total_price
        total_tax = (discount_taxes[0].tax / 100) * total_price

        final = total_price - total_discount + total_tax
        qty=quantity
        merged_data.append((product, images, total_price, quantity))
        return render(request, "shop/buynow.html", {'merged_data': merged_data, 'final': final, 'qty': qty, 'quantity':quantity,'discount': discount, 'tax': tax})






        # return HttpResponse("Error: Product details not found.")


def buynow(request, id):
    user_id = request.session.get('user_id')
    if user_id:
        products = AddcartProduct.objects.filter(user_id=user_id)

        if len(products) == 0:
            print("Cart is empty")
        else:
            merged_data = []
            final=0
            qty=0

            for product in products:
                # pro = Product.objects.get(id=product.product_id)
                images = ProductImage.objects.filter(Product_id=product.product_id)
                prices = ProductPrice.objects.filter(Product_id=product.product_id)
                discount_taxes = ProductDiscountTax.objects.filter(Product_id=product.product_id)
                quantity = AddcartProduct.objects.filter(product_id=product.product_id)
                total_price = prices[0].price * quantity[0].qty
                total_discount = (discount_taxes[0].discount / 100) * total_price
                total_tax = (discount_taxes[0].tax / 100) * total_price
                total = total_price - total_discount + total_tax
                discount=discount_taxes[0].discount
                tax=discount_taxes[0].tax
                final+=total
                qty+=quantity[0].qty
                p=AddcartProduct.objects.filter(user_id=user_id)
                pro_list = []
                for i in p:
                    try:
                        pro = Product.objects.get(id=i.product_id)
                        pro_list.append(pro.id)
                    except:
                        pass

                d=AddcartProduct.objects.filter(user_id=user_id)
                d_list = [] 
                for i in d:
                    discount=discount_taxes[0].discount
                    try:
                        d_list.append(discount)
                    except:
                        pass
                t=AddcartProduct.objects.filter(user_id=user_id)
                t_list = []
                for i in t:
                    tax=discount_taxes[0].tax
                    try:
                        t_list.append(tax)
                    except:
                        pass
                pr=AddcartProduct.objects.filter(user_id=user_id)
                total_list=[]
                for i in pr:
                    to=total
                    try:
                        total_list.append(to)
                    except:
                        pass    
                q=AddcartProduct.objects.filter(user_id=user_id)
                quantity_list=[]
                for i in q:
                    qu=quantity[0].qty
                    try:
                        quantity_list.append(qu)
                    except:
                        pass



                merged_data.append((pro,images, total_price ,quantity,prices,total))

    return render(request, "shop/buynow.html" , {'merged_data': merged_data, 'final':final,'pro_list':pro_list, 'user_id': user_id,'quantity':quantity,'qty':qty, 'discount':discount, 'tax':tax, 'd_list':d_list, 't_list':t_list,'total':total, 'total_list':total_list,'quantity_list':quantity_list})



def payments(request):
    if request.method == 'POST':
        productid = request.POST.get('product_id')
        payment_id = request.POST.get('payment_id')
        payer_id = request.POST.get('payer_id')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        postal_code = request.POST.get('postal_code')
        name = request.POST.get('name')
        total = request.POST.get('total')
        addresss = request.POST.get('address')
        status = request.POST.get('status')
        created_at = request.POST.get('date_time')
        user_id = request.session.get('user_id')

        try:
            payment = Payment(                                                                             
                payment_id=payment_id,
                payer_id=payer_id,
                amount=total,  
                status=status,
                created_at=created_at
            )
            payment.save()
            add = address(
                name=name,
                address=addresss,
                city=city,
                state=state,
                country=country,
                postal_code=postal_code,
                created_at=created_at
            )
            add.save()
            product_ids = request.POST.getlist('product_id')
            for i in product_ids:
                try:
                    discount = ProductDiscountTax.objects.get(product=i)
                    quantity = AddcartProduct.objects.get(product=i)
                    price = ProductPrice.objects.get(Product=i)
                    pay = paydetails(
                        product_id=i,
                        user_id=user_id,
                        discount=discount.discount,
                        qty=quantity.qty,
                        tax=discount.tax,
                        amount=price.price,
                        created_at=created_at,
                        updated_at=created_at,)
                    pay.save()

                except (ProductDiscountTax.DoesNotExist, AddcartProduct.DoesNotExist, ProductPrice.DoesNotExist):
                    pass


            



            return JsonResponse({payment.status})
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'error': 'Error updating quantity: ' + str(e)})
    else:
        return JsonResponse({'error': 'Invalid request method'})



    











