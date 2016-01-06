from django.shortcuts import render, redirect
from lists.models import Item
#from django.http import HttpResponse

# Create your views here.
def home_page(request):
    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()

    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/lists/the-only-list/') # redirect if POST

    return render(request, 'home.html')
    #return HttpResponse('<html><title>To-Do lists</title></html>')

# not a function
#home_page = None

def view_list(request):
    items = Item.objects.all() # all saved items
    return render(request, 'list.html', { 'items': items, })
