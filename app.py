from flask import Flask, session
from credentials.views import DashboardView
from auth.views import Index, AuthBackend, Logout
from pymongo import MongoClient
import redis

import random, os, string

app = Flask(__name__)

app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))

conn = MongoClient(os.environ['MONGODB_URI'])
db = conn[os.environ['MONGODB_DB']]

r = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'], db=os.environ['REDIS_DB'], password=os.environ['REDIS_PASSWORD'])

app.add_url_rule('/', view_func=Index.as_view('index', template_name='index.html'))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard', template_name='dashboard.html', db=db))
app.add_url_rule('/auth', view_func=AuthBackend.as_view('auth', db=db))
app.add_url_rule('/logout', view_func=Logout.as_view('logout'))

def main():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
