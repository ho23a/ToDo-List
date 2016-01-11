from unittest import skip
from .base import TodoFunctionalTest

class ItemValidationTest(TodoFunctionalTest):
    @skip("Haven't implemented this")
    def test_cannot_add_empty_list_item(self):
        # Edith goes to the homepage, and accidentally tries
        # to submit an empty list item.
        # She hits Enter on the empty input box

        # The home page refreshes, adn there is an error message
        # saying that list items cannot be blank

        # She tries again with some text for the item,
        # which now works

        # Perversely tries to enter a second blank items

        # She receives a similar warning on the list page_text

        # And she can correct it by filling some text in
        self.fail('Finish the test!')


        # Satisfied, they both go back to sleep

        # ______ DELETED _______
        # Edith wonders whether the site will remember her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect

        # She visits that URL - her to-do list is still there

        # Satisfied, she goes back to sleep
        # self reminder to finish the app
        # self.fail('Finish the app!')

    # test to verify the behavior
    #def test_can_log_in_to_a_new_account(self):


# main method
# if __name__ == '__main__':
#     unittest.main()
