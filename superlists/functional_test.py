from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# inside () is extends
class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        # after 3 seconds, if nothing executed, inform Failed
        self.browser.implicitly_wait(3)


    def tearDown(self):
        self.browser.quit()

    # refactoring, help function
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # refactoring, help function
    def enter_a_new_item(self, item_text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    # test to verify the behavior
    def test_can_start_a_list_and_retrieve_it_later(self):

        # Edith has heard about a cool new online to-do app
        # She goes to check out its homepage
        # reference to firefox
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        # assert 'To-Do' in browser.title
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # same as the above line, more specific exception
        #if ! 'Django' in browser.title:
        #    throw new AssertionError

        # She is invited to enter a to-do item straight away
        # placeholder hints what to put in the inputbox
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a test box
        # (Edith's hobby is tying fly-fishing lures)
        self.enter_a_new_item('Buy peacock feathers')

        # When she hits enter, the page updates , and now the page lists
        # "1. Buy peacock feathers" as an item in a to-do lists

        # wait 15 seconds to read error
        # import time
        # time.sleep(15)

        self.check_for_row_in_list_table('1. Buy peacock feathers')
        # self.assertTrue(
        #     # quick and dirty way
        #     any(row.text == '1. Buy peacock feathers' for row in rows),
        #     "New item did not appear -- text was:\n%s"%(table.text,)
        # )

        # There's still a text box inviting her to add another item
        # She enters 'Use peacock feathers to make fly'
        # (Edith is very methodolical)
        self.enter_a_new_item('Use peacock feathers to make fly')

        # The homepage updates again and now shows both items on her lists
        self.check_for_row_in_list_table('1. Buy peacock feathers')
        self.check_for_row_in_list_table('2. Use peacock feathers to make fly')

        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect

        # She visits that URL - her to-do list is still there

        # Satisfied, she goes back to sleep
        # self reminder to finish the app
        self.fail('Finish the app!')

    # test to verify the behavior
    #def test_can_log_in_to_a_new_account(self):


# main method
if __name__ == '__main__':
    unittest.main()
