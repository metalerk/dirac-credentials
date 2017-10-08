from flask.views import View
from flask import render_template, session, redirect, url_for
from utils.utils import nocache

class DashboardView(View):

    def __init__(self, template_name, db, rsession):
        self.template_name = template_name
        self.qs = db
        print("===============>>>>>")
        print("From {}".format(self.template_name))
        print(dict(rsession.get('app:active')))
        print("===============>>>>>")

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    @nocache
    def dispatch_request(self):

        if 'active' in session:

            if session['active']:
                context = [item for item in self.qs.credentials.find()][0]
                context['title'] = 'Index'

                return self.render_template(context)

        return redirect('/')
