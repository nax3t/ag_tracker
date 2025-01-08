from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Product
from .forms import ProductForm
from django.db.models import Count, Sum
from django.db.models.functions import Round
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

PRODUCTS_PER_PAGE = 10

def product_list(request):
    products_list = Product.objects.all()
    
    paginator = Paginator(products_list, PRODUCTS_PER_PAGE)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        products = paginator.page(paginator.num_pages)
    
    # Rest of your existing view code...
    low_stock = []
    category_data = products_list.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    stock_status = None
    products_json = []
    for product in products_list:  # Use products_list here, not paginated products
        if product.latitude and product.longitude:
            products_json.append({
                'name': product.name,
                'latitude': float(product.latitude),
                'longitude': float(product.longitude),
                'location': product.location
            })

    return render(request, 'products/product_list.html', {
        'products': products,  # This is now paginated
        'low_stock': low_stock,
        'category_data': category_data,
        'products_json': json.dumps(products_json, cls=DjangoJSONEncoder),
        'stock_status': stock_status,
    })
    products = Product.objects.all()
    low_stock = []
    
    # Chart data for all products
    category_data = products.values('category').annotate(
        count=Count('id')
    ).order_by('-count')
    
    stock_status = None

    # Prepare product location data for the map
    products_json = []
    for product in products:
        if product.latitude and product.longitude:
            products_json.append({
                'name': product.name,
                'latitude': float(product.latitude),
                'longitude': float(product.longitude),
                'location': product.location
            })

    return render(request, 'products/product_list.html', {
        'products': products,
        'low_stock': low_stock,
        'category_data': list(category_data),
        'stock_status': stock_status,
        'products_json': json.dumps(products_json, cls=DjangoJSONEncoder)
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, 'Product created successfully.')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Edit Product',
        'product': product
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('products:list')
    return render(request, 'products/product_confirm_delete.html', {'product': product}) 