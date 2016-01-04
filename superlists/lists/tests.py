from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from lists.views import home_page
class HomePageTest(TestCase):

    # test home page's url set up correctly
    def test_root_url_resolves_to_home_page_view(self):
        # pass in whatever after the domain name
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        #url
        request = HttpRequest()
        # what the program returns --??
        response = home_page(request)

        self.assertTrue(response.content.startswith('<html>'))
        self.assertIn('<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith('</html>'))


# class SmokeTest(TestCase):
#     def test_bad_maths(self):
#         self.assertEqual(1 + 1, 3)
