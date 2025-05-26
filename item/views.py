from django.shortcuts import render , get_object_or_404,redirect
from .models import Item, Category
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import NewItemForm,EditItemForm


def browse(request):
    query = request.GET.get('query','')
    category_id = request.GET.get('category')
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id and category_id.isdigit():
        items = items.filter(Category__id=int(category_id))

    # if the query is not empty we filter the items by name or description


    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query) )

    return render(request , 'item/browse.html',{
        'items':items,
        'query':query,
        'categories':categories,
        'category_id': int(category_id) if category_id and category_id.isdigit() else None,

    })


# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk )
    related_items = Item.objects.filter(Category=item.Category,is_sold=False).exclude(pk=pk)[0:5]
    categories = Category.objects.all()
    return render(request ,'item/detail.html', {
        'item':item,
        'related_items':related_items,
        'categories': categories
    })

@staff_member_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
        
    return render(request , 'item/new.html', {
            'form':form,
            'title':'New Item',
    })


@login_required
def edit(request,pk):
    item = get_object_or_404(Item, pk=pk )
    if request.method == 'POST':
        form = EditItemForm(request.POST,request.FILES , instance=item)
        #checking if the form is valid and saving it
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        #passing the current data to the form so we can modify it
        form = EditItemForm(instance=item)
        
    return render(request , 'item/new.html', {
            'form':form,
            'title':'Edit Item',
    })

@login_required
def delete(request , pk):
    item = get_object_or_404(Item, pk=pk , created_by=request.user)
   
    item.delete()
    return redirect('dashboard:index')


