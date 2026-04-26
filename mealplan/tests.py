from django.test import TestCase
from django.urls import reverse


class MealplanQuestionnaireTests(TestCase):
    def test_start_redirects_to_first_question(self):
        response = self.client.get("/")

        self.assertRedirects(response, reverse("mealplan:question", kwargs={"number": 1}))

    def test_single_choice_saves_and_advances(self):
        response = self.client.post(
            reverse("mealplan:question", kwargs={"number": 1}),
            {"diet": "vegan"},
        )

        self.assertRedirects(response, reverse("mealplan:question", kwargs={"number": 2}))
        self.assertEqual(self.client.session["mealplan_answers"]["diet"], "vegan")

    def test_multi_choice_saves_list_and_rerenders_checked_inputs(self):
        self.client.post(reverse("mealplan:question", kwargs={"number": 1}), {"diet": "none"})
        response = self.client.post(
            reverse("mealplan:question", kwargs={"number": 2}),
            {"medical": ["diabetes", "ibs"]},
        )

        self.assertRedirects(response, reverse("mealplan:question", kwargs={"number": 3}))
        self.assertEqual(self.client.session["mealplan_answers"]["medical"], ["diabetes", "ibs"])

        response = self.client.get(reverse("mealplan:question", kwargs={"number": 2}))
        self.assertContains(response, 'id="medical_diabetes"')
        self.assertContains(response, 'value="diabetes" checked')
        self.assertContains(response, 'id="medical_ibs"')
        self.assertContains(response, 'value="ibs" checked')

    def test_question_templates_extend_floating_center_and_keep_next_outside_scroll_area(self):
        response = self.client.get(reverse("mealplan:question", kwargs={"number": 6}))

        self.assertTemplateUsed(response, "mealplan/question.html")
        self.assertTemplateUsed(response, "floating_center.html")
        self.assertContains(response, 'overflow-y: auto')
        self.assertContains(response, ">NEXT</button>")

    def test_question_nine_defaults_to_first_choice_for_selected_meal_count(self):
        session = self.client.session
        session["mealplan_answers"] = {"meals": "3"}
        session.save()

        response = self.client.get(reverse("mealplan:question", kwargs={"number": 9}))

        self.assertContains(response, 'id="meal1_standard"')
        self.assertContains(response, 'id="meal2_standard"')
        self.assertContains(response, 'id="meal3_standard"')
        self.assertContains(response, 'value="standard" checked', count=3)

    def test_processing_page_uses_parent_template_and_progress_bar(self):
        response = self.client.get(reverse("mealplan:processing"))

        self.assertTemplateUsed(response, "mealplan/processing.html")
        self.assertTemplateUsed(response, "floating_center.html")
        self.assertContains(response, "Creating meal plan")
        self.assertContains(response, "width: 100%")
