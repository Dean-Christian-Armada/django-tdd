from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.utils import override_settings
from django.test import TestCase, LiveServerTestCase
from django.conf import settings

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from collections import namedtuple

import time

# Take note that you need to create values in the database like a new User Account as the test database will not read anything from the test database
# To create these values you will dump data into a json file
# Ex. mkdir fts/fixtures
## python manage.py dumpdata auth.User --indent=2 > fts/fixtures/admin_user.json 

# Create your tests here.


message_interval = 1 # seconds
not_long_enough = 0.7 # seconds
long_enough = 3 # seconds

PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question="How awesome is Test-Driven Development?",
    choices=[
        'Very awesome',
        'Quite awesome',
        'Moderately awesome',
    ],
)
POLL2 = PollInfo(
    question="Which workshop treat do you prefer?",
    choices=[
        'Beer',
        'Pizza',
        'The Acquisition of Knowledge',
    ],
)

# LiveServerTestCase is used for selenium where a browser will open for demo
class PollsTest(StaticLiveServerTestCase):

	# @override_settings(DEBUG=True)
	# def test_debug(self):
	# 	assert settings.DEBUG

	# fixtures is the same as getting data and in this case we get it from a json file
	fixtures = ['admin_user.json']

	def setUp(self):
		# self.browser is the selenium object which represents the web browser, aka the WebDriver.
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_create_new_poll_via_admin_site(self):
		# opens the web browser, and goes to the admin page
		self.browser.get(self.live_server_url+'/admin/') # .get is tells the browser to go to a new page

		# sees the familiar 'Django Administration' heading
		body = self.browser.find_element_by_tag_name('body') # find_element_by_tag_name, which tells Selenium to look through the page and find the HTML element for a particular tag
		# assertion - where we say what we expect, and the test should pass or fail at this point:
		self.assertIn('Django administration', body.text)

		# Types her username and passwords hits return
		username_field = self.browser.find_element_by_name('username') # .find_element_by_name finds the name attribute
		username_field.send_keys('admin')
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('adgcadgc')
		# Keys.RETURN is the same as Enter
		password_field.send_keys(Keys.RETURN)

		# username and password must be accepted and is taken to the Site Administration page
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Site administration', body.text)

		# Looking for a couple of hyperlink that says "Polls"
		# print ("-----")
		# time.sleep(long_enough)
		polls_links = self.browser.find_elements_by_link_text('Polls') # Finds element's' with all that text in a link
		# self.assertEquals(len(polls_links), 2) # Tells that ther must be two links of the Polls

		# clicks the second link
		polls_links[0].click()

		# taken to the polls listing page, which shows she has no polls yet
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('0 polls', body.text)

		# She sees a link to 'add' a new poll, so she clicks it
		new_poll_link = self.browser.find_element_by_link_text('ADD POLL')
		new_poll_link.click()

		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Question', body.text)
		self.assertIn('Date published', body.text)

		# types in an interesting question for the Poll
		question_field = self.browser.find_element_by_name('question')
		question_field.send_keys("How awesome is Test-Driven Development?")

		# sets the date and time of publication - it'll be a new year's poll!
		date_field = self.browser.find_element_by_name('pub_date_0')
		date_field.send_keys('01/01/12')
		time_field = self.browser.find_element_by_name('pub_date_1')
		time_field.send_keys('00:00')

		choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
		choice_1.send_keys('Very awesome')
		choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
		choice_2.send_keys('Quite awesome')
		choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
		choice_3.send_keys('Moderately awesome')

		# Click the save button
		save_button = self.browser.find_element_by_css_selector("input[value='Save']")
		save_button.click()

		new_poll_links = self.browser.find_elements_by_link_text("How awesome is Test-Driven Development?")
		self.assertEquals(len(new_poll_links), 1)

		self.browser.get(self.live_server_url+'/admin/')
		self.browser.find_element_by_link_text('LOG OUT').click()

	def _setup_polls_via_admin(self):
		# logs into the admin site
		self.browser.get(self.live_server_url+'/admin/')
		username_field = self.browser.find_element_by_name('username')
		username_field.send_keys('admin')
		password_field = self.browser.find_element_by_name('password')
		password_field.send_keys('adgcadgc')
		password_field.send_keys(Keys.RETURN)

		# User has a number of polls to enter.  For each one, user:
		for poll_info in [POLL1, POLL2]:
			# Follows the link to the Polls app, and adds a new Poll
			self.browser.find_elements_by_link_text('Polls')[0].click()
			self.browser.find_element_by_link_text('ADD POLL').click()

			# Enters its name, and uses the 'today' and 'now' buttons to set the publish date
			question_field = self.browser.find_element_by_name('question')
			question_field.send_keys(poll_info.question)
			self.browser.find_element_by_link_text('Today').click()
			self.browser.find_element_by_link_text('Now').click()

			# Sees she can enter choices for the Poll on this same page, so she does
			for i, choice_text in enumerate(poll_info.choices):
				choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
				choice_field.send_keys(choice_text)

			# Saves her new poll
			save_button = self.browser.find_element_by_css_selector("input[value='Save']")
			save_button.click()

			# Is returned to the "Polls" listing, where she can see her new poll, listed as a clickable link by its name
			new_poll_links = self.browser.find_elements_by_link_text(poll_info.question)
			self.assertEquals(len(new_poll_links), 1)

			# She goes back to the root of the admin site
			self.browser.get(self.live_server_url+'/admin/')

		# She logs out of the admin site
		self.browser.find_element_by_link_text('LOG OUT').click()

	@override_settings(DEBUG=True) # This command shows the errors
	def test_voting_on_a_new_poll(self):
		# First, Gertrude the administrator logs into the admin site and
	    # creates a couple of new Polls, and their response choice
	    self._setup_polls_via_admin()

	    # Now, Herbert the regular user goes to the homepage of the site. He sees a list of polls.
	    self.browser.get(self.live_server_url)
	    heading = self.browser.find_element_by_tag_name('h1')
	    self.assertEquals(heading.text, 'Polls')

	    # He clicks on the link to the first Poll, which is called
	    # 'How awesome is test-driven development?'
	    first_poll_title = POLL1.question
	    # time.sleep(long_enough)
	    self.browser.find_element_by_link_text(first_poll_title).click()

	    # He is taken to a poll 'results' page, which says
	    # "no-one has voted on this poll yet"
	    main_heading = self.browser.find_element_by_tag_name('h1')
	    self.assertEquals(main_heading.text, 'Poll Results')
	    sub_heading = self.browser.find_element_by_tag_name('h2')
	    self.assertEquals(sub_heading.text, first_poll_title)
	    body = self.browser.find_element_by_tag_name('body')
	    self.assertIn('No-one has voted on this poll yet', body.text)

	    # He also sees a form, which offers him several choices.
	    # He decided to select "very awesome"

	    # He clicks 'submit'

	    # The page refreshes, and he sees that his choice
	    # has updated the results.  they now say
	    # "100 %: very awesome".

	    # The page also says "1 votes"