from flask.views import View, MethodView
from flask import render_template, redirect, url_for, request
from utils.utils import nocache

class Index(View):
    def __init__(self, template_name, rsession):
        self.rsession = rsession
        self.template_name = template_name
        print("===============>>>>>")
        print("From {}".format(self.template_name))
        print(self.rsession.session_is_active)
        print(self.rsession.get_obj_identifier)
        print("===============>>>>>")

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    @nocache
    def dispatch_request(self):

        context = dict()
        context['rsession'] = self.rsession

        if self.rsession.session_is_active:
            return redirect(url_for('dashboard'))

        else:
            return self.render_template(context)

class AuthBackend(MethodView):
    def __init__(self, db, rsession):
        self.rsession = rsession
        methods = ['POST']
        self.qs = db

    def post(self):

        print("===============>>>>>")
        print("From auth")
        print(self.rsession.session_is_active)
        print("===============>>>>>")

        if self.rsession.session_is_active:
            return redirect(url_for('dashboard'))

        else:

            auth_code = self.qs.auth.find_one()['code']
            req_code = request.form.get('code')

            if auth_code == req_code:
                self.rsession.set_session_active()
                return redirect(url_for('dashboard'))
            else:
                return redirect('/')



class Logout(View):
    def __init__(self, rsession):
        self.rsession = rsession

    def dispatch_request(self):

        if self.rsession.session_is_active:
            self.rsession.set_session_inactive()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
