from flask import Flask
from credentials.views import DashboardView
from auth.views import Index, AuthBackend, Logout
from pymongo import MongoClient
from utils.utils import RedisSession

import random, os, string

app = Flask(__name__)

#app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))

conn = MongoClient(os.environ['MONGODB_URI'])
db = conn[os.environ['MONGODB_DB']]

rsession = RedisSession()

app.add_url_rule('/', view_func=Index.as_view('index', template_name='index.html', rsession=rsession))
app.add_url_rule('/dashboard', view_func=DashboardView.as_view('dashboard', template_name='dashboard.html', db=db, rsession=rsession))
app.add_url_rule('/auth', view_func=AuthBackend.as_view('auth', db=db, rsession=rsession))
app.add_url_rule('/logout', view_func=Logout.as_view('logout', rsession=rsession))

def main():
    app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()
