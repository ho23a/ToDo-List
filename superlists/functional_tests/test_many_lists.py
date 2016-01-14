from .base import TodoFunctionalTest

class ManyListsTest(TodoFunctionalTest):
    def test_can_create_and_view_multiple_lists(self):
        # Edith comes to the home page, creates a new list,
        # and fills in her grocery List
        self.browser.get(self.live_server_url)
        self.enter_a_new_item('Buy milk')
        self.enter_a_new_item('Buy cheese')
        self.check_for_row_in_list_table('Buy milk')
        self.check_for_row_in_list_table('Buy cheese')

        # She sees she can change a list name
        self.change_list_name('Groceries')

        # Edith goes back to the home page, and sees her grocery List
        self.browser.get(self.live_server_url)
        self.check_for_row_in_list_table('Buy milk')

        # Edith creates a new list for her Art History homework
        self.enter_a_new_item('Read Camille') # Read Camille auto becomes list name

        # Edith opens the home page later and sees both ListViewTest
        self.browser.get(self.live_server_url)
        self.check_for_row_in_list_table('Groceries')
        self.check_for_row_in_list_table('Read Camille')

        # Edith goes to the grocery list and sees what she needs to Buy
        row = self.find_table_row('id_list_table')
        row.find_element_by_tag_name('a').click()
        self.check_for_row_in_list_table('Buy milk')
        self.check_for_row_in_list_table('Buy cheese')