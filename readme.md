# PASEVAL
## Password tester and generator 

Paseval is a web app that runs on local server using Django that let's the user test the strength of a given password, as well generate a password through two means (randomly or personalized)

The app has three sections:

- Password testing: Evaluates composition of the password (length, variety of chars, existence of words), as well as whether it has been found to be Pwned in the past. From these two factors it returns a general score
- Personalized Password generator: The user can create a password by filling the form with the input they desire. This can make the end result more easy to remember
- Random Password generator: The user can pick the length and types of characters they want in a randomized password

# How to run
You can run the django server using the following command:
<< The application will run in the port 8001 >>
```sh
python3 manage.py runserver
```

### Dependencies
THIS APP RUNS ON DJANGO, SO HAVING IT INSTALLED IS A MUST

you will need the following libraries from python:
- english_words
- hashlib
- requests
- random
