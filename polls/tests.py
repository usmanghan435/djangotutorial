
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
        Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=30),
        )

        response = self.client.get(reverse("polls:index"))

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [],
        )

    def test_past_question_with_future_question(self):
        past_question = Question.objects.create(
            question_text="Past question",
            pub_date=timezone.now() - datetime.timedelta(days=5),
        )

        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=5),
        )

        response = self.client.get(reverse("polls:index"))

        self.assertContains(response, past_question.question_text)
        self.assertNotContains(response, future_question.question_text)

    def test_only_five_questions_are_displayed(self):
        for day in range(6):
            Question.objects.create(
                question_text=f"Question {day}",
                pub_date=timezone.now() - datetime.timedelta(days=day),
            )

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(
            len(response.context["latest_question_list"]),
            5,
        )


class QuestionDetailViewTests(TestCase):

    def test_existing_question(self):
        question = Question.objects.create(
            question_text="A test question",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )

        response = self.client.get(
            reverse("polls:detail", args=(question.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
    
    def test_non_existing_question(self):
        response = self.client.get(
            reverse("polls:detail", args=(9999,))
        )

        self.assertEqual(response.status_code, 404)
    
    def test_future_question(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=30),
        )

        response = self.client.get(
            reverse("polls:detail", args=(future_question.id,))
        )

        self.assertEqual(response.status_code, 404)

class QuestionResultsViewTests(TestCase):

    def test_existing_question(self):
        question = Question.objects.create(
            question_text="A test question",
            pub_date=timezone.now() - datetime.timedelta(days=1),
        )

        response = self.client.get(
            reverse("polls:results", args=(question.id,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question.question_text)
    
    def test_non_existing_question(self):
        response = self.client.get(
            reverse("polls:results", args=(9999,))
        )

        self.assertEqual(response.status_code, 404)
    
    def test_future_question(self):
        future_question = Question.objects.create(
            question_text="Future question",
            pub_date=timezone.now() + datetime.timedelta(days=30),
        )

        response = self.client.get(
            reverse("polls:results", args=(future_question.id,))
        )

        self.assertEqual(response.status_code, 404)


