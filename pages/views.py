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
            "author": "Developed by: Anderson Jimenez", 
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


class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        # Obtener todos los productos de la base de datos
        products = {
            121: {'name': 'Tv Samsung', 'price': '1000'},
            11: {'name': 'iPhone', 'price': '2000'}
        }

        # Obtener productos en el carrito desde la sesión
        cart_product_data = request.session.get('cart_product_data', {})
        cart_products = {int(key): products[int(key)] for key in cart_product_data if int(key) in products}

        # Preparar datos para la vista
        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping Cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        # Obtener productos en el carrito desde la sesión
        cart_product_data = request.session.get('cart_product_data', {})

        # Agregar producto al carrito si no está ya agregado
        cart_product_data[str(product_id)] = True  # Se usa `True` para indicar que el producto está en el carrito

        # Guardar en sesión
        request.session['cart_product_data'] = cart_product_data
        request.session.modified = True  # Asegura que la sesión se actualice

        return redirect('cart_index')



class CartRemoveAllView(View):
    def post(self, request):
        # Remove all products from cart in session
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']
        return redirect('cart_index')

def ImageViewFactory(image_storage):
    class ImageView(View):
        template_name = 'images/index.html'

        def get(self, request):
            image_url = request.session.get('image_url', '')
            return render(request, self.template_name, {'image_url': image_url})

        def post(self, request):
            image_url = image_storage.store(request)
            request.session['image_url'] = image_url
            return redirect('image_index')

    return ImageView
