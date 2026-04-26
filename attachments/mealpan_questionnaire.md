# Mealplan Questionnaire

The following Questions are to be used to design meal plans. 

## IMAGES

I am not expecting final images to be supplied but the tags to display and format the images should all be present
so that I can add the images in just by updating the src attribute. 

## Details for all pages

There should be a back button, allowing the user to return to the previous question. Any data added in the
previous question should be displayed.

Questions 1, 4, and 5 are single choices and so when the user clicks on a choice they should be taken to the
next question

All other questions will have a full Width "NEXT" button to submit results. The Submit button must be outside of
the scrollable area, so its always visible

Question Number 9 will have Choices for each of the meals. The first option should be selected by default. As such
this is not a single question, but a group of multiple choice questions.

All other questions are multiple select questions that should be defined as checkboxes. Each Choice will be displayed
as a square image. Place a default image in each and they will be replaced later. The results should be returned
as a checkbox choices list.

All inputs MUST have an id attached.

There must be a progress bar at the bottom of the page

Buttons, progress bars and selected items should use the Primary color

## Coding Requirements

* These are to be Django templates and will use floating_center.html in templates/ as the parent element. 
* Items with a lot of choices should allow for scrolling within the element and not go offscreen
* Unselected buttons should have a background colour, the same as the html background image (the color not image)
* Bulma.io CSS will be used and has been customized. Any CSS changes should be done in Style attributes
* Django FORMS must NOT be used.
* Django Generic view must NOT be used.
* Results will be saved in a dictionary in requests.session.
* All values must be single number, single words or a list of single words. No sentences
* Questions with a lot of choices, not only need to be scrollable, but be ready for items to be added or removed, thus need to be responsive, NOT hard coded
* No calculations will be expected. The project is just to create the set of pages needed



Question 1: Special diets

Full width buttons stacked vertically

* None
* Vegan
* Vegetarian
* Pescatarian
* Paleo


Question 2: Medical Issues

Please check if you have one of the following

Table with a button to select on the right, must be scrollable

* Diabetes
* Polycystic Overy Syndrome
* Hypertension
* Cardiovascular Disease
* IBS
* Celiac Disease
* Chronic Kidney Disease
* Taking any of the following
  * statins
  * Calcium Channel Blockers
  * Immunosuppressant
  * blood thinners
  * Anit-Anxiety/anit-depression medications
* Have blood pressure, headaches and/or migrates caused by Tryamine (Aged Cheese, chocolate , red wine)
* Are taking medications effected by high potassium, such as selected blood pressure medications


Question 3: Allergies

The layout should be the same as proteins

* nuts
* peanuts
* seafood
* fish
* gluten
* milk
* soy
* celery
* mustard

Question 4: Number of meals per day

* 2
* 3
* 4
* 5

(Not including snacks)


Question 5: Training time

* Early morning before eating
* Late morning after eating
* Mid Day
* Afternoon
* Evening

Question 6: protein

Select your preferred protein sources. This will contain a lot of choices so scrolling within the element
will be required. There should be 5 choices in each row. Each Image will have a text label under it as well

Question 7 Protein

Select Proteins you don't want included. Same as above


Question 8 Ingredients You want to avoid

Select 0 or more items in the list to be excluded from meals. Same layout as for protein choices

* cabbage
* brussel sprouts
* beef
* chicken
* lamb
* pork
* white fish
* oily fish
* Very spicy
* any Spicy
* tomatoes
* bell peppers (sweet)
* onions


Question 9 Meal Types

For each meal, click on your preferred meal type.

Two choices for each of the number of meals selected.


Last Page: processing to create meal plan.

An Image to be displayed with a progress bar, showing the meal plan is being created. Placeholder page 
only at this time. No actions are needed
