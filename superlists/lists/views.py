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
    Item.objects.create(text = request.POST['item_text'], list=new_list)
    return redirect('/lists/%d/' % (new_list.id,))

def view_list(request, list_id):
    # whatever between slashes lists/235901/ will be list_id
    list_ = List.objects.get(id=list_id) # find list with given list id. id is int
    # items: array of items in list_
    # items = Item.objects.filter(list=list_) # all saved items in list_
    return render(
        request, 'list.html',
        # { 'items': items,
        { 'list': list_, }
    )

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/%d/' % (list_.id))
