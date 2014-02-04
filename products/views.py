import json
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from books.utils import JSONEncoder
from forms import AddProductForm
from products.models import Product


@login_required(login_url='/')
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
    if request.method == 'POST':
        query = request.POST.get('query')
        products = Product.objects.filter(title__icontains=query)
        context['products'] = products
        return render_to_response('search-result.html', context)
    return render_to_response('search.html', context)
def product_view(request, product_id):
    context = {}
    product = Product.objects.get(pk=product_id)
    context['product'] = product
    return render_to_response("products/product-view.html", context)
