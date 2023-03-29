# Crowd-Fundraising-App

[![PyPi Version](https://img.shields.io/pypi/v/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![PyPi Version Alt](https://badge.fury.io/py/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)  
[![PyPi Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)
[![PyPi Downloads](http://pepy.tech/badge/yt2mp3)](http://pepy.tech/project/yt2mp3)
[![Python Versions](https://img.shields.io/pypi/pyversions/yt2mp3.svg)](https://pypi.python.org/pypi/yt2mp3/)

> Create a web platform for starting fundraise projects.


### About the Project :open_book:

Crowdfunding is the practice of funding a project or venture by
raising small amounts of money from a large number of people,
typically via the Internet.

## Landing Page Content:
- A slider to show `top rated`  running projects to encourage users to donate
- List of the latest 5 projects
- List of latest 5 featured projects (which are selected by the
admin)
- A list of the categories. User can open each category to view its projects
- Projects Filtered by tags section

## About the Header 
Header: contains Login/Register. If the user is already logged in, then the link will be Logout. And If the logged-in user is an admin, 
then there will be another link called Manage Blog that will redirect the admin to the administration page to make the admin CRUD Operations.

### How to run the project  :horse_racing:

 ##### To run locally 
```sh
* Clone the repository 
 git clone git@github.com:Rowida46/Crowd-Fundraising-App.git

* Enter directory 
 cd Crowd-Fundraising-App

* Activate virtual environment
  source venv/bin/activate

* Install packages
  pip install -r requirements.txt

* Set environment variables
 cp .env.example .env

* Fill the parameters

  CLIENT_ID= {Github Client Id}
  CILENT_SECRET= {Github Client Secret}
  STRIPE_API= {Stripe token}
  MAIL_USERNAME = {Email Id }
  MAIL_PASSWORD = {Email Password}
  
* Remove and reset _migrations_ to start from fresh database
 find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
 find . -path "*/migrations/*.pyc"  -delete

* Start app
  python manage.py runserver

* Head over to http://localhost:8000



## DataBase Architecture :desktop_computer:
```sh

There are mainly four schemas 

* Users - which contains details about the users
* Project - which contains details about the projects
* Tags - that contains tags captions
* Categories - taht hold project categories name and image
* Like - that hold useres's reactions 
* Comments - that hold user comments on projects
* Reply - that hold useres' reply on comment
* Report Project : that is for report project
* Report Comment : that is for report comment

### DataBase Architecture

- project and category : one to many 
- project and tags: many to many 

```
