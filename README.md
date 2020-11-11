# Werewolf Game
### to run the server:
* run command prompt and use command "cd <project's folder directory>"
* use the command "python manage.py runserver"

### views.py file:
* it contains the player superclass and roles classes as well global variables to control the game
* it contains functions that renders html templates according to the URLs

### settings.py file:
Django settings for werewolf project.

### urls.py file:

The `urlpatterns` list routes URLs to views functions that renders the templates.
1- it has an import:  from werewolf import views
2- use it to add a URL to urlpatterns: example path('', views.home, name='home')

### there are two test classes inside the folder tests.

### test_views.py:
tests all view functions and rendered values and created and modified objects. check comments for detailed info

### test_urls.py:
tests all the mapping between the URLs and view function.

### templates folder:

contains html templates that are used for rendering the data to the user.
views functions use them to render the pages

### static folder:

contains static frontend files such as photos and scripts
and css styling
