from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from django.utils import timezone

from .models import Poll, Choice

# Create your tests here.
class PollModelTest(TestCase):
	 def test_creating_a_new_poll_and_saving_it_to_the_database(self):
	 	# Create a new poll object with its "question" set
	 	poll = Poll()
	 	poll.question = "What's up?"
	 	poll.pub_date = timezone.now()
	 	poll.save()

	 	# now check we can find it in the database again
	 	all_polls_in_database = Poll.objects.all()
	 	self.assertEquals(len(all_polls_in_database), 1)
	 	only_poll_in_database = all_polls_in_database[0]
	 	self.assertEquals(only_poll_in_database, poll)

	 	# check that it's saved its two attributes: question and pub_date
	 	self.assertEquals(only_poll_in_database.question, "What's up?")
	 	self.assertEquals(only_poll_in_database.pub_date, poll.pub_date)

	 	# self.fail('test_creating_a_new_poll_and_saving_it_to_the_database Done')

	 def test_poll_objects_are_named_after_their_question(self):
	 	p = Poll()
	 	p.question = "How is baby formed?"
	 	self.assertEquals(str(p), "How is baby formed?")

	 	# self.fail('test_poll_objects_are_named_after_their_question Done')


	 def test_creating_some_choices_for_a_poll(self):
	 	poll = Poll()
	 	poll.question = "What's up?"
	 	poll.pub_date = timezone.now()
	 	poll.save()

	 	# create a Choice object
	 	choice = Choice()

	 	# link it with our Poll
	 	choice.poll = poll

	 	# give it some text
	 	choice.choice = "doin' fine..."

	 	# and let's say it's had some votes
	 	choice.votes = 3

	 	# save it
	 	choice.save()

	 	# try retrieving it from the database, using the poll object's reverse lookup
	 	poll_choices = poll.choice_set.all()
	 	self.assertEquals(poll_choices.count(), 1)

	 	choice_from_db = poll_choices[0]
	 	self.assertEquals(choice_from_db, choice)
	 	self.assertEquals(choice_from_db.choice, "doin' fine...")
	 	self.assertEquals(choice_from_db.votes, 3)

	 def test_choice_defaults(self):
	 	choice = Choice()
	 	self.assertEquals(choice.votes, 0)

class HomePageViewTest(TestCase):
	def test_root_url_shows_all_polls(self):
		# set up some polls
		poll1 = Poll(question='6 times 7', pub_date=timezone.now())
		poll1.save()
		poll2 = Poll(question='life, the universe and everything', pub_date=timezone.now())
		poll2.save()

		response = self.client.get('/') # This is the self.browser.get version of StaticLiveServerTestCase in TestCase

		# check we've used the right template
		self.assertTemplateUsed(response, 'home.html')

		# check we've passed the polls to the template
		polls_in_context = response.context['polls']
		self.assertEquals(list(polls_in_context), [poll1, poll2])

		self.assertIn(poll1.question, response.content)
		self.assertIn(poll2.question, response.content)

		# check the page also contains the urls to individual polls pages
		poll_url = reverse('polls.views.poll', args=[poll1.id])
		self.assertIn(poll_url, response.content)
		poll2_url = reverse('polls.views.poll', args=[poll2.id])
		self.assertIn(poll2_url, response.content)