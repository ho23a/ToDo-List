from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.models import Item, List
#from django.http import HttpResponse

# Create your views here.
def home_page(request):
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()

    # if request.method == 'POST':
    #     Item.objects.create(text = request.POST['item_text'])
    #     return redirect('/lists/the-only-list/') # redirect if POST

    return render(request, 'home.html')
    #return HttpResponse('<html><title>To-Do lists</title></html>')

# not a function
# home_page = None

def new_list(request):
    new_list = List.objects.create()
    # above method creates new list everytime POST, so final list only
    # has final item
    item = Item(text = request.POST['item_text'], list=new_list)
    # If validation passes, redirect. Else, return to home page
    try:
        item.full_clean()
        item.save() # only execute when validation passes
    except ValidationError:
        new_list.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect('/lists/%d/' % (new_list.id,))

def view_list(request, list_id):
    # whatever between slashes lists/235901/ will be list_id
    list_ = List.objects.get(id=list_id) # find list with given list id. id=int

    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'], list=list_)

    # items: array of items in list_
    # items = Item.objects.filter(list=list_) # all saved items in list_
    return render( # method == 'GET'
        request, 'list.html',
        # { 'items': items,
        { 'list': list_, }
    )

def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    list_ = item.list
    item.delete()

    return redirect('/lists/%d/' % (list_.id,))
