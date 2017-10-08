from flask.views import View
from flask import render_template, redirect, url_for
from utils.utils import nocache

class DashboardView(View):

    def __init__(self, template_name, db, rsession):
        self.rsession = rsession
        self.template_name = template_name
        self.qs = db
        print("===============>>>>>")
        print("From {}".format(self.template_name))
        print(self.rsession.session_is_active)
        print("===============>>>>>")

    def get_template_name(self):
        return self.template_name

    def render_template(self, context):
        return render_template(self.get_template_name(), **context)

    @nocache
    def dispatch_request(self):

        if self.rsession.session_is_active:
            context = [item for item in self.qs.credentials.find()][0]
            context['title'] = 'Index'
            context['rsession'] = self.rsession
            return self.render_template(context)

        else:
            return redirect('/')
