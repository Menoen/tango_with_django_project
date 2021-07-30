from rango.forms import CategoryForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from rango.models import Category
from rango.models import Page
from django.urls import reverse
from rango.forms import PageForm

# Create your views here.
def index(request):
  category_list = Category.objects.order_by('-likes')[:5]
  pages = Page.objects.order_by('-views')[:5]
  context_dict = {}
  context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
  context_dict['categories'] = category_list
  context_dict['pages'] = pages
  return render(request, 'rango/index.html', context = context_dict)

def about(request):
  context_dict = {'yourname':'Weiwei Zhao'}
  return render(request, 'rango/about.html',context=context_dict)

def show_category(request, category_name_slug):
  context_dict = {}
  try:
    category = Category.objects.get(slug = category_name_slug)
    pages = Page.objects.filter(category = category)
    context_dict['pages'] = pages
    context_dict['category'] = category
  except Category.DoesNotExist:
    context_dict['pages'] = None
    context_dict['category'] = None
  return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
  form = CategoryForm()
  # is a HTTP POST?
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    # is a valid form?
    if form.is_valid():
      cat = form.save(commit=True)
      print(cat, cat.slug)
      return redirect('/rango/')
    else:
      # print errors
      print(form.errors)
  return render(request, 'rango/add_category.html',{'form':form})

def add_page(request, category_name_slug):
  try:
      category = Category.objects.get(slug=category_name_slug)
  except:
      category = None
      
  if category is None:
      return redirect(reverse('rango:index'))

  form = PageForm()

  if request.method == 'POST':
      form = PageForm(request.POST)

      if form.is_valid():
          if category:
              page = form.save(commit=False)
              page.category = category
              page.views = 0
              page.save()
              return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
      else:
          print(form.errors)  

  context_dict = {'form': form, 'category': category}
  return render(request, 'rango/add_page.html', context=context_dict)
