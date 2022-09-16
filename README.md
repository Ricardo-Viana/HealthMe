# HealthMe
#### Description: Web-based aplication that you can keep track of your workout activities.
#### This program was made with the idea of create healthy habits.
#### The project contains 3 important areas:
#### 1. Login area where you can login into your account that you have registered.
#### 2. Exercises area where you can add the workout you have already done.
#### 3. Done area where you can look to all of your activies in a list form.
#### These areas are distributed in 3 files:
#### -Static, that contains the style part like the css file, this file help with the colors, size and disposal:
####   Contains two logo photos and the style.css.
#### -Templates, all of html files are here, the texts and the layout are all in this group:
####   Apresentation.html - Create the welcome message once the user log in.
####   Change.html - Create the change password area.
####   Done.html - All exercises the list that show the exercises are here.
####   Error.html - If the user cause some error, the message are show in this html.
####   Exercises.html - The page that the user are going to use to put the exercises (Aerobic and Anaerobic)
####   Layout.html - Create the principal layout for the whole program, here is where all the "extends" parts come from.
####   Login.html - Login area where the user enter on his page once its registered, without this page the user cant use most part of the project.
####   Register.html - First part of the program, all things start here.
#### -Back-End, python, data-base and this README are in this area, this contains the informations of the users, the connection with the web managed by Flask.
####   Application.py - Usage of python, flask and SQL are here. On application.py are several functions:
####    Login function - Manage the login of the user
####    Register function - Manage the registration of the user, creating for him space on the data-base
####    Logout function - Manage the logout of the user, clearing the session.
####    Exercises function - Manage all of the entry the user put on the exercises tab, if something is wrong will provide some error.
####    Done function - Display the list for the user see, associating html with data-base.
####    Change Password function - Manage the password of the user, trading the old one for the new.
####    Delete function - All that the delete button does is managed here, going to the data-base deleting the list.
####    Search function - Open a new google tab searching about the exercise that the user put.
####   Project.db - Data-base using SQL that contains all the information that is disposal on the list and the user's username and password(with hashcode).
####    users1 table - manage the users, store the username and the password of each user.
####    exercises table(Many columns):
####        1. users_id - Get the id from the users1 table, used to associate the platform with each user.
####        2. repsortimes - Store the reps or time, if the exercise is Aerobic time are storage (e.g 30s) and if the exercise is Anaerobic it storage the reps (e.g 1x20).
####        3. exercisesname- Store the name of the exercises, it is used to search the exercise on google for example.
####        4. type - Store the type of the exercise, Aerobic or Anaerobic.
####        5. time - Store the real time that the user put the exercise on platform, used to display on the list.
#### All of the design choices were made with the help of my cousin(an actual designer), the chosen colors give to the user an idea of lightness and they match each other.
####    Green - The psychology of green associate him to peace, rest and security. Gives the site a bit of nature.
####    White - This color is the major color when associate to peace and is a clean color. Furthermore, it matches to the color green.


