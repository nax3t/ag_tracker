from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Product
from .forms import ProductForm

def product_list(request):
    # If user is logged in, show their products, otherwise show all products
    if request.user.is_authenticated:
        products = Product.objects.filter(user=request.user)
        low_stock = products.filter(quantity__lte=models.F('minimum_stock'))
    else:
        products = Product.objects.all()
        low_stock = []
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'low_stock': low_stock
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
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