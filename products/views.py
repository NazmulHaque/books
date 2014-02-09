import json
import datetime

from django.core.paginator import Paginator
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from books.utils import JSONEncoder
from forms import AddProductForm
from products.models import Products
from books import settings


@login_required(login_url='/login-view')
def add(request):
    context = {}
    context.update(csrf(request))
    if request.user.is_authenticated():
        context['login_mode'] = True
        context['user'] = request.user
    context['categories'] = settings.PRODUCT_CATEGORY_LIST
    context['languages'] = settings.PRODUCT_LANGUAGES_LIST
    context['conditions'] = settings.PRODUCT_CONDITION_LIST

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
    context['categories'] = settings.PRODUCT_CATEGORY_LIST
    context['languages'] = settings.PRODUCT_LANGUAGES_LIST
    context['conditions'] = settings.PRODUCT_CONDITION_LIST
    context['districts'] = settings.DISTRICT_LIST
    if request.user.is_authenticated():
        context['login_mode'] = True
        context['user'] = request.user

    #objects = Products.objects.filter(status='Public').order_by('-created_at')
    objects = Products.objects.all().order_by('-created_at')
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

    objects = Products.objects.all().order_by('-created_at')
    p = Paginator(objects, 2)
    products = p.page(page_number)
    context['products'] = products
    return render_to_response('recent-posts.html', context)


def search_result(request):
    if request.method == 'POST':
        context = {}
        query_dict = {}
        #query_dict['status'] = 'Public'
        query = request.POST.get('query')
        if query:
            query_dict['title__icontains'] = query
        category = request.POST.get('category')
        if category:
            query_dict['category'] = category
        language = request.POST.get('language')
        if language:
            query_dict['language'] = language
        condition = request.POST.get('condition')
        if condition:
            query_dict['condition'] = condition
        location = request.POST.get('location')
        if location:
            query_dict['user__userprofile__district'] = location

        page_number = request.POST.get('page', 1)
        objects = Products.objects.filter(**query_dict).order_by( '-created_at')
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
    product = Products.objects.get(pk=product_id)
    context['product'] = product
    return render_to_response("products/product-view.html", context)

@login_required(login_url='/login-view')
def info_edit(request, product_id):
    context = {}
    context.update(csrf(request))

    if request.user.is_authenticated():
        context['login_mode'] = True
        context['user'] = request.user

    form = AddProductForm()
    context['form'] = form

    product = Products.objects.get(pk=product_id)

    if request.method == 'POST':
        form = AddProductForm(request.POST)

        if form.is_valid():
            product.title = request.POST.get('title')
            product.description = request.POST.get('description')
            product.category = request.POST.get('category')
            product.condition = request.POST.get('condition')
            product.price = request.POST.get('price')
            product.language = request.POST.get('language')
            product.updated_at = datetime.datetime.now()
            product.save()
            return HttpResponse('True')
        else:
            return HttpResponse('False')
    return render_to_response('products/product-edit-view.html', context)






