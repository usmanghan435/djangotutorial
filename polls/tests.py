
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        question = Question(pub_date=time)

        self.assertIs(question.was_published_recently(), True)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=2)
        question = Question(pub_date=time)

        self.assertIs(question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=1)
        question = Question(pub_date=time)

        self.assertIs(question.was_published_recently(), False)





class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")

    def test_questions_are_displayed(self):
        question1 = Question.objects.create(
            question_text="First question",
            pub_date=timezone.now() - datetime.timedelta(days=5),
        )
        question2 = Question.objects.create(
            question_text="Second question",
            pub_date=timezone.now() - datetime.timedelta(days=2),
        )

        response = self.client.get(reverse("polls:index"))

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
    
    def test_future_question_is_not_displayed(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=30),
        )

        response = self.client.get(reverse("polls:index"))

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

