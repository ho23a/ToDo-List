from django.core.urlresolvers import resolve
from django.utils.html import escape
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
            '/lists/new', # convention: POST: no trailing slash to do action,
            #GET: trailing slash
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
            '/lists/new',
            data={'item_text': 'A new list item'}
        )
        # request = HttpRequest()
        # # POST to send data. Have to set method
        # request.method = 'POST'
        # request.POST['item_text'] = 'A new list item'
        # response = home_page(request)

        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))
        # redirect's status code = 302
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'], '/lists/the-only-list/')

        # test homepage render
        # self.assertIn('A new list item', response.content.decode())
        # expected_html = render_to_string(
        #     'home.html', { 'new_item_text': 'A new list item'}
        # )
        # self.assertEqual(response.content.decode(), expected_html)

    def test_validation_errors_are_sent_back_to_home_page(self):
        response = self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_arent_save(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

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

class DeleteItemTest(TestCase):
    def test_deleting_item(self):
        correct_list = List.objects.create()
        todelete = Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        response = self.client.get('/lists/items/%d/delete_item' % (todelete.id,))

        # WHY NOT WORK? 302 != 200
        # self.assertNotContains(response, 'itemey 1')
        # self.assertContains(response, 'itemey 2')

        self.assertEqual(Item.objects.count(), 1)

        # appropriate & necessary?
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id))

class ListViewTest(TestCase):

    def test_uses_list_template(self):
        new_list = List.objects.create()
        # GET request on the given URL
        response = self.client.get('/lists/%d/' % (new_list.id,)) # id: number
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_list(self):
        new_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=new_list)
        Item.objects.create(text='itemey 2', list=new_list)

        other_list = List.objects.create()
        Item.objects.create(text='other item 1', list=other_list)
        Item.objects.create(text='other item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (new_list.id,)) # id: number

        # assert new_list has its items, not other_list's items
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other item 1')
        self.assertNotContains(response, 'other item 2')

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post(
            '/lists/%d/' % (correct_list.id,),
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_validation_errors_stay_on_list_page(self):
        current_list = List.objects.create()
        response = self.client.post(
            '/lists/%d/' % (current_list.id,),
            data={'item_text': ''}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list.html')
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_items_arent_saved(self):
        current_list = List.objects.create()
        self.client.post(
            '/lists/%d/' % (current_list.id,),
            data={'item_text': ''}
        )
        self.assertEqual(Item.objects.count(), 0)

    def test_list_view_displays_checkbox(self):
        current_list = List.objects.create()
        Item.objects.create(text="Item 1", list=current_list)
        Item.objects.create(text="Item 2", list=current_list)

        response = self.client.get('/lists/%d/' % (current_list.id,))

        self.assertContains(response, 'input type="checkbox"')

    # test POST when there's toggle done
    def test_POST_items_toggles_done(self):
        pass
    # def test_redirects_to_list_view(self):
    #     correct_list = List.objects.create()
    #
    #     response = self.client.post(
    #         '/lists/%d/' % (correct_list.id,),
    #         data={'item_text': 'A new item for an existing list'}
    #     )
    #
    #     self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))
