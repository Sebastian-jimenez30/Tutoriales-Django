from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Product

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView): 
    template_name = 'pages/about.html' 
     
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context.update({ 
            "title": "About us - Online Store", 
            "subtitle": "About us", 
            "description": "This is an about page ...", 
            "author": "Developed by: Juan Miguel", 
        }) 
 
        return context

class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.objects.all() 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'products/show.html' 
 
 
    def get(self, request, id):

        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product id must be 1 or greater")
            product = get_object_or_404(Product,pk=product_id)
        
        except (IndexError, ValueError):
            return HttpResponseRedirect(reverse('home')) 
        
        viewData = {}
        product = get_object_or_404(Product,pk=product_id)  
        viewData["title"] = product.name + " - Online Store" 
        viewData["subtitle"] =  product.name + " - Product information" 
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title']  = 'Products - Online Store'
        context['subtitle'] = 'List of products'

        return context
        

class ProductForm(forms.ModelForm): 
    
    class Meta:
        model = Product
        fields = ['name','price']

    def clean_price(self): 
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError('The price must be greater than zero.')
        return price
 
class ProductCreateView(View): 
    template_name = 'products/create.html' 
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save()
            return redirect('created')  
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)

class ProductCreatedView(TemplateView):
    template_name = 'products/created.html'