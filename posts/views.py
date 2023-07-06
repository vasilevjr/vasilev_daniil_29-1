from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, View, CreateView

from posts.models import Product, Category
from posts.forms import ProductCreateForm
from posts.constants import PAGINATION_LIMIT



class MainPageCBV(ListView):
    model = Product
    template_name = 'layoutеs/index.html'


class ProductsCBV(ListView):
    def get(self, request, *args, **kwargs):
        posts = self.model.objects.all()
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        max_page = posts.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
                max_page = round(max_page) + 1
        else:
                max_page = round(max_page)

        posts = posts[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        if search_text:
            ''' startswith, endswith, contains '''
            ''' AND, OR '''

            posts = posts.filter(Q(title__contains=search_text) | Q(description__contains=search_text))

            context_data = {
                'posts': posts,
                'user': request.user,
                'pages': range(1, max_page + 1)
            }

            return render(request, self.template_name, context=context_data)


def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()

        context_data = {
            'categories': categories
        }

        return render(request, 'products/categories.html', context=context_data)

def product_detail_view(request, pk):
    if request.method == 'GET':
        try:
            post = Product.objects.get(id=pk)
        except Product.DoesNotExist:
            return render(request, 'products/detail.html')

        context_data = {
            'post': post
        }

        return render(request, 'products/detail.html', context=context_data)

def post_create_view(request):
    if request.user.is_anonymous:
        return redirect('/products/')
    if request.method == 'GET':
        context_data = {
            'form': ProductCreateForm
        }

        return render(request, 'products/create.html', context=context_data)

    if request.method == 'POST':
        data, file = request.POST, request.FILES
        form = ProductCreateForm(data, file)

        if form.is_valid():
            Product.objects.create(
                image=form.cleaned_data.get('image'),
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
            )
            return redirect('/products/')

        return render(request, 'products/create.html', context={
            'form': form
        })




