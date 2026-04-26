# Set of Question Pages for a Django Project

Upwork task number: `38749017`

## Job Description

This project needs a set of basic Django views and HTML templates for a question flow. The pages do not require complex calculations and should not connect to the database at this time.

The work is primarily HTML template development, with only the backend view and URL wiring needed to render the pages and move through the question sequence. Full page details, question text, options, and any ordering requirements are listed in [attachments/mealpan_questionnaire.md](attachments/mealpan_questionnaire.md).

The implementation must follow the requirements exactly.

## Project Context

- Django project: `config`
- Django app: `mealplan`
- Current view file: `mealplan/views.py`
- Current URL file: `config/urls.py`
- Templates should be added under the app template directory, for example `mealplan/templates/mealplan/`.
- No database-backed models are required for this work.

## Application Stack

- Python 3.14.0
- Django 6.0.4
- SQLite, used only for Django's built-in session table
- Django template engine
- Bulma CSS, loaded by the base template
- Function-based Django views
- Session-backed questionnaire state through `request.session`

This project does not use Django Forms, Django Generic Views, or custom database-backed models for the questionnaire flow.

## Client Local Setup

From the project root, create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install Django:

```bash
python -m pip install "Django==6.0.4"
```

Apply Django's built-in migrations. This creates the SQLite tables needed for sessions:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open the questionnaire in a browser:

```text
http://127.0.0.1:8000/
```

If the development server has trouble with the auto-reloader in the local environment, run it without reload:

```bash
python manage.py runserver --noreload
```

## Useful Local Commands

Run Django system checks:

```bash
python manage.py check
```

Run the test suite:

```bash
python manage.py test
```

## Required Implementation

- Build the question pages as standard Django function-based views.
- Add URL routes for each question page.
- Add HTML templates for each question page.
- Use plain template context dictionaries for page data.
- Persist entered answers between pages without using Django Forms or database models.
- Preserve answers when users navigate backward and forward through the flow.

## Critical Acceptance Criteria

- Uses `floating_center.html` as the parent template for every question page.
- Includes a back button on every page that returns to the previous question and preserves previously entered data.
- Places the full-width `NEXT` button outside of the scrollable content area on all multi-select questions.
- Implements single-choice questions 1, 4, and 5 so that clicking an option immediately advances to the next page.
- Displays all multi-select choices as square images with default placeholder images and attached input IDs.
- Renders Question 9 as multiple grouped meal-type selections with the first choice in each group selected by default.
- Adds a progress bar at the bottom of every page styled with the project's primary color.
- Ensures all templates avoid Django Forms and Django Generic Views.

## Optional Acceptance Criteria

- Layouts with many choices should scroll inside the element without overflowing the screen.

## Template Requirements

Every question template must extend the shared parent template:

```django
{% extends "floating_center.html" %}
```

Question pages should keep the main choices inside a scrollable content region when the option list is long. For multi-select pages, the `NEXT` button must sit outside that scrollable region so it remains visible and full width.

Single-choice questions 1, 4, and 5 should submit or navigate immediately when an option is selected. These pages should not require a separate `NEXT` click.

Multi-select choices must render as square image options. Each option must include:

- A default placeholder image.
- A stable input `id`.
- A matching label connected to the input.
- A selected state based on previously entered data.

Question 9 must render grouped meal-type selections. The first choice in each group should be selected by default when the user has not already made a selection.

## Backend Requirements

Use function-based views only. Do not use Django Generic Views.

Do not use Django Forms. Inputs can be regular HTML form controls, and validation can be simple request/session handling inside function-based views.

Suggested state handling:

- Store answers in `request.session`.
- On `POST`, update the session for the current question.
- Redirect to the next question after saving.
- Back buttons should route to the previous question and rely on session data to repopulate inputs.

## Verification Checklist

- Every question page renders without server errors.
- Every question template extends `floating_center.html`.
- Back navigation works from every page.
- Previously entered answers remain selected after using back navigation.
- Questions 1, 4, and 5 advance immediately after clicking an option.
- Multi-select pages show square image choices with placeholder images.
- Multi-select `NEXT` buttons remain outside scrollable content.
- Question 9 displays grouped meal-type selections and defaults each group to its first choice.
- A bottom progress bar appears on every page and uses the project's primary color.
- No Django Forms are used.
- No Django Generic Views are used.
