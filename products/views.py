import json

from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from books.utils import JSONEncoder
from forms import AddProductForm
from products.models import Product


@login_required(login_url='/login-view')
def add(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        context['login_mode'] = True
        context['user'] = request.user
        if request.user.is_superuser:
            context['user_admin'] = True
    form = AddProductForm()
    context['form'] = form
    if request.method == 'POST':
        form = AddProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            dict = {'add': True, 'username': request.user.username}
            data = json.dumps(dict, cls=JSONEncoder)
            return HttpResponse(data, content_type="application/json")
        else:
            errors_dict = {}
            if form.errors:
                for error in form.errors:
                    e = form.errors[error]
                    errors_dict[error] = unicode(e)
            data = json.dumps(errors_dict, cls=JSONEncoder)
            return HttpResponse(data, content_type="application/json")

    return render_to_response('products/add-product.html', context)


def search(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        context['login_mode'] = True
        context['user'] = request.user
        if request.user.is_superuser:
            context['user_admin'] = True

    objects = Product.objects.all().order_by('-created_at')
    p = Paginator(objects, 2)
    products = p.page(1)
    context['products'] = products
    context['total_products'] = len(objects)
    return render_to_response('search.html', context)

def recent_search(request):
    context = {}
    page_number = 1
    if request.method == 'POST':
        page_number = request.POST.get('page')

    objects = Product.objects.all().order_by('-created_at')
    p = Paginator(objects, 2)
    products = p.page(page_number)
    context['products'] = products
    return render_to_response('recent-posts.html', context)


def search_result(request):
    if request.method == 'POST':
        context = {}
        query = request.POST.get('query')
        page_number = request.POST.get('page', 1)
        objects = Product.objects.filter(title__icontains=query).order_by('-created_at')
        p = Paginator(objects, 2)
        products = p.page(page_number)
        context['products'] = products
        context['total_products'] = len(objects)
        return render_to_response('search-result.html', context)

def product_view(request, product_id):
    context = {}
    if request.user.is_authenticated():
        context['login_mode'] = True
        context['user'] = request.user
        if request.user.is_superuser:
            context['user_admin'] = True
    product = Product.objects.get(pk=product_id)
    context['product'] = product
    return render_to_response("products/product-view.html", context)
