Example of logging in with Okta using the [Flask-Dance](https://github.com/singingwolfboy/flask-dance) library.

```
git clone https://github.com/mdorn/flask-dance-okta.git
cd flask-dance-okta
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
cp .env.example .env  # modify your .env file with values for your Okta environment
flask run
```
