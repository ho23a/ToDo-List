from unittest import skip
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import unittest

# inside () is extends
class TodoFunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # after 3 seconds, if nothing executed, inform Failed
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def find_table_row(self, item_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        for row in rows:
            row_text = row.find_elements_by_tag_name('td')[2].text
            if item_text == row_text:
                return row
        return None

    # refactoring, help function
    def check_for_row_in_list_table(self, row_text):
        row = self.find_table_row(row_text)
        self.assertIsNotNone(row)
        # self.assertIn(row_text + " Delete", [row.text for row in rows])

    # refactoring, help function
    def enter_a_new_item(self, item_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)
