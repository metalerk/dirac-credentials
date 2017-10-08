from flask.views import View, MethodView
from flask import render_template, session, redirect, url_for, request
from utils.utils import nocache

class Index(View):
    def __init__(self, template_name):
        self.template_name = template_name

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    @nocache
    def dispatch_request(self):

        if 'active' in session:
            print("===============>>>>>")
            print(session['active'])
            print("===============>>>>>")
            if session['active']:
                return redirect(url_for('dashboard'))

        context = dict()
        context['title'] = 'Index'

        return self.render_template(context)

class AuthBackend(MethodView):
    def __init__(self, db):
        methods = ['POST']
        self.qs = db

    def post(self):

        if 'active' in session:
            if session['active']:
                return redirect(url_for('dashboard'))

        auth_code = self.qs.auth.find_one()['code']
        req_code = request.form.get('code')

        if auth_code == req_code:
            session['active'] = True
            return redirect(url_for('dashboard'))
        else:
            return redirect('/')



class Logout(View):

    def dispatch_request(self):

        if 'active' in session:
            if session['active']:
                session['active'] = False
                return redirect(url_for('index'))
            else:
                return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
