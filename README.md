# tour-e-blog

- It's a web based application.
- Developer can add his blogs to web app which viewers can visit.
- Viewers can login/logout from the app.
- After logging in viewers can contact to Author also.
- It is deveolped as:
  - Frontend:- HTML/CSS/JS
  - Backend:- Flask-Python
  - DB:- MySQL
- Deployment is not possible in my case as I have used RDBMS (MySQL) which will not be able to deploy on Heroku as it supports PostgreSQL.
- Steps to run:-
  - ```git clone  https://github.com/thesilentcoderr/tour_e_blog.git```
  - Create empty db and exit from db promt
  - ```mysql -u <your_uname> -p <db_name> < tour_e_blog.sql```
  - Update vars.json with your credentials
  - ```pip install -r requirements.txt```
  - ```python app.py
