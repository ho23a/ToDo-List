from selenium import webdriver

# Edith has heard about a cool new online to-do app
# She goes to check out its homepage

# reference to firefox
browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# She notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

# same as the above line, more specific exception
#if ! 'Django' in browser.title:
#    throw new AssertionError

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a test box
# (Edith's hobby is tying fly-fishing lures)

# When she hits enter, the page updates , and now the page lists
# "1. Buy peacock feathers" as an item in a to-do lists

# There's still a text box inviting her to add another item
# She enters 'Use peacock feathers to make fly'
# (Edith is very methodolical)

# The homepage updates again and now shows both items on her lists

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect

# She visits that URL - her to-do list is still there

# Satisfied, she goes back to sleep
browser.quit()
