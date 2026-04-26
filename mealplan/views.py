from django.shortcuts import redirect, render
from django.urls import reverse


PRIMARY_COLOR = "#00d1b2"
BACKGROUND_COLOR = "#f5f7fb"
PLACEHOLDER_IMAGE = "/static/mealplan/placeholder.svg"


PROTEIN_CHOICES = [
    ("chicken", "Chicken"),
    ("turkey", "Turkey"),
    ("beef", "Beef"),
    ("pork", "Pork"),
    ("lamb", "Lamb"),
    ("whitefish", "White fish"),
    ("oilyfish", "Oily fish"),
    ("shellfish", "Shellfish"),
    ("eggs", "Eggs"),
    ("tofu", "Tofu"),
    ("tempeh", "Tempeh"),
    ("beans", "Beans"),
    ("lentils", "Lentils"),
    ("chickpeas", "Chickpeas"),
    ("yogurt", "Yogurt"),
]


QUESTIONS = {
    1: {
        "key": "diet",
        "title": "Special diets",
        "kind": "single",
        "choices": [
            ("none", "None"),
            ("vegan", "Vegan"),
            ("vegetarian", "Vegetarian"),
            ("pescatarian", "Pescatarian"),
            ("paleo", "Paleo"),
        ],
    },
    2: {
        "key": "medical",
        "title": "Medical Issues",
        "help_text": "Please check if you have one of the following",
        "kind": "medical",
        "choices": [
            ("diabetes", "Diabetes"),
            ("pcos", "Polycystic Overy Syndrome"),
            ("hypertension", "Hypertension"),
            ("cardiovascular", "Cardiovascular Disease"),
            ("ibs", "IBS"),
            ("celiac", "Celiac Disease"),
            ("kidney", "Chronic Kidney Disease"),
            ("statins", "Taking statins"),
            ("calcium", "Taking Calcium Channel Blockers"),
            ("immunosuppressant", "Taking Immunosuppressant"),
            ("bloodthinners", "Taking blood thinners"),
            ("anxiety", "Taking Anit-Anxiety/anit-depression medications"),
            ("tyramine", "Blood pressure, headaches and/or migrates caused by Tryamine"),
            ("potassium", "Taking medications effected by high potassium"),
        ],
    },
    3: {
        "key": "allergies",
        "title": "Allergies",
        "kind": "multi_image",
        "choices": [
            ("nuts", "nuts"),
            ("peanuts", "peanuts"),
            ("seafood", "seafood"),
            ("fish", "fish"),
            ("gluten", "gluten"),
            ("milk", "milk"),
            ("soy", "soy"),
            ("celery", "celery"),
            ("mustard", "mustard"),
        ],
    },
    4: {
        "key": "meals",
        "title": "Number of meals per day",
        "help_text": "Not including snacks",
        "kind": "single",
        "choices": [
            ("2", "2"),
            ("3", "3"),
            ("4", "4"),
            ("5", "5"),
        ],
    },
    5: {
        "key": "training",
        "title": "Training time",
        "kind": "single",
        "choices": [
            ("early", "Early morning before eating"),
            ("late", "Late morning after eating"),
            ("midday", "Mid Day"),
            ("afternoon", "Afternoon"),
            ("evening", "Evening"),
        ],
    },
    6: {
        "key": "preferred_protein",
        "title": "protein",
        "help_text": "Select your preferred protein sources.",
        "kind": "multi_image",
        "choices": PROTEIN_CHOICES,
    },
    7: {
        "key": "excluded_protein",
        "title": "Protein",
        "help_text": "Select Proteins you don't want included.",
        "kind": "multi_image",
        "choices": PROTEIN_CHOICES,
    },
    8: {
        "key": "avoided_ingredients",
        "title": "Ingredients You want to avoid",
        "help_text": "Select 0 or more items in the list to be excluded from meals.",
        "kind": "multi_image",
        "choices": [
            ("cabbage", "cabbage"),
            ("brusselsprouts", "brussel sprouts"),
            ("beef", "beef"),
            ("chicken", "chicken"),
            ("lamb", "lamb"),
            ("pork", "pork"),
            ("whitefish", "white fish"),
            ("oilyfish", "oily fish"),
            ("veryspicy", "Very spicy"),
            ("spicy", "any Spicy"),
            ("tomatoes", "tomatoes"),
            ("peppers", "bell peppers (sweet)"),
            ("onions", "onions"),
        ],
    },
    9: {
        "key": "meal_types",
        "title": "Meal Types",
        "help_text": "For each meal, click on your preferred meal type.",
        "kind": "meal_types",
        "choices": [
            ("standard", "Standard"),
            ("portable", "Portable"),
        ],
    },
}


def _answers(request):
    return request.session.setdefault("mealplan_answers", {})


def _question_url(number):
    return reverse("mealplan:question", kwargs={"number": number})


def start(request):
    return redirect(_question_url(1))


def question(request, number):
    if number not in QUESTIONS:
        return redirect("mealplan:processing")

    answers = _answers(request)
    question_data = QUESTIONS[number]

    if request.method == "POST":
        _save_answer(request, answers, question_data)
        request.session.modified = True
        return redirect("mealplan:processing" if number == 9 else _question_url(number + 1))

    selected = _selected_value(answers, question_data)
    context = _context_for_question(number, question_data, answers, selected)
    return render(request, "mealplan/question.html", context)


def processing(request):
    return render(
        request,
        "mealplan/processing.html",
        {
            "back_url": _question_url(9),
            "progress": 100,
            "primary_color": PRIMARY_COLOR,
            "background_color": BACKGROUND_COLOR,
            "placeholder_image": PLACEHOLDER_IMAGE,
        },
    )


def _save_answer(request, answers, question_data):
    key = question_data["key"]
    kind = question_data["kind"]

    if kind == "single":
        answers[key] = request.POST.get(key, "")
        return

    if kind in {"multi_image", "medical"}:
        answers[key] = request.POST.getlist(key)
        return

    if kind == "meal_types":
        meal_count = _meal_count(answers)
        answers[key] = {
            f"meal{index}": request.POST.get(f"meal{index}", question_data["choices"][0][0])
            for index in range(1, meal_count + 1)
        }


def _selected_value(answers, question_data):
    key = question_data["key"]

    if question_data["kind"] in {"multi_image", "medical"}:
        return answers.get(key, [])

    return answers.get(key, "")


def _context_for_question(number, question_data, answers, selected):
    meal_groups = []

    if question_data["kind"] == "meal_types":
        saved_meal_types = answers.get(question_data["key"], {})
        for index in range(1, _meal_count(answers) + 1):
            field_name = f"meal{index}"
            meal_groups.append(
                {
                    "field_name": field_name,
                    "label": f"Meal {index}",
                    "selected": saved_meal_types.get(field_name, question_data["choices"][0][0]),
                }
            )

    return {
        "question_number": number,
        "question": question_data,
        "choices": question_data["choices"],
        "selected": selected,
        "meal_groups": meal_groups,
        "back_url": _question_url(number - 1) if number > 1 else None,
        "progress": round((number / len(QUESTIONS)) * 100),
        "primary_color": PRIMARY_COLOR,
        "background_color": BACKGROUND_COLOR,
        "placeholder_image": PLACEHOLDER_IMAGE,
    }


def _meal_count(answers):
    try:
        return int(answers.get("meals", "2"))
    except (TypeError, ValueError):
        return 2
