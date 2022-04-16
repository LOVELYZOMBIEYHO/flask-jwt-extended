# Usage:

## sample_template

1. Copy from : https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage/
2. python -m venv venv
3. venv\Scripts\activate.bat
4. pip install flask
5. touch app.py (or create app.py by self)
6. app.py (paste the code)
7. Postman :http://127.0.0.1:5000/login (depends on your url) (POST) to get Token

Header:
KEY - Content-type
VALUE - application/json

Body:
{
"username": "test",
"password": "test"
}

7. Postman : http://127.0.0.1:5000/protected (depends on your url) (GET)

Header:
A. KEY - Content-type
A. VALUE - application/json
B. KEY - Authorization
B. VALUE - Bearer yourSecretToken.

For example:
Bearer eyJmcmVzaCI6ZmFsc2UsIml

Body:
GET Request no body

8. To set access token to cookies:
   app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
   response = jsonify({"msg": "login successful"},{"Welcome": username_variable})
   set_access_cookies(response, access_token)

https://flask-jwt-extended.readthedocs.io/en/stable/token_locations/

\*\*\* If deployed to Heroku, the SQLite should be replaced with PostgreSQL to avoid Heroku-Dynos deleting data automatically.
