from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest
from lists.models import Item, List
from lists.views import home_page

class HomePageTest(TestCase):

    # test home page's url set up correctly
    def test_root_url_resolves_to_home_page_view(self):
        # pass in whatever after the domain name
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest() # url
        # get a response of home_page from the request
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

        #self.assertTrue(response.content.startswith('<html>'))
        #self.assertIn('<title>To-Do lists</title>', response.content)
        # strips() gets rid of white space in '</html>'
        #self.assertTrue(response.content.strips().endswith('</html>'))

    # def test_home_page_doesnt_save_on_GET_request(self):
        # request = HttpRequest()
        # home_page(request)
        # self.assertEqual(Item.objects.count(), 0)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        self.client.post(
            '/lists/new', # convention: POST: no trailing slash to do action, GET: trailing slash
            data={'item_text': 'A new list item'}
        )
        # request = HttpRequest()
        # # POST to send data. Have to set method
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'
        # response = home_page(request)

        # test if added a new item
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirecting_after_POST(self):
        response = self.client.post(
            '/lists/new', # convention: POST: no trailing slash to do action, GET: trailing slash
            data={'item_text': 'A new list item'}
        )
        # request = HttpRequest()
        # # POST to send data. Have to set method
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'
        # response = home_page(request)

        self.assertRedirects(response, '/lists/the-only-list/')
        # redirect's status code = 302
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list/')

        # test homepage render
        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string(
        #     'home.html', { 'new_item_text': 'A new list item'}
        # )
        # self.assertEqual(response.content.decode(), expected_html)

    # homepage now displays list, not all items
    # def test_home_page_displays_all_items(self):
    #     Item.objects.create(text='itemey 1')
    #     Item.objects.create(text='itemey 2')
    #
    #     request = HttpRequest()
    #     response = home_page(request)
    #
    #     self.assertIn('itemey 1', response.content.decode())
    #     self.assertIn('itemey 2', response.content.decode())

# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        # GET request on the given URL
        response = self.client.get('/lists/the-only-list/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_items(self):
        new_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=new_list)
        Item.objects.create(text='itemey 2', list=new_list)

        response = self.client.get('/lists/the-only-list/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

class ItemAndListModelsTest(TestCase):
    def test_saving_and_retrieving_items_in_list(self):
        new_list = List()
        new_list.save()

        # get 2 new list items
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = new_list
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = new_list
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(new_list, saved_list)

        # get the list of all saved items
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(first_saved_item.list, new_list)
        self.assertEqual(second_saved_item.list, new_list)
