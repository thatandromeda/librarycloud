from django.http import HttpResponse
from django.views.generic import TemplateView

import requests

class StackView(TemplateView):
    template_name = 'stackview.html'

    def get_context_data(self, **kwargs):
        context = super(StackView, self).get_context_data(**kwargs)
        url = 'http://api.lib.harvard.edu/v2/items.json?subject.topic=women&sort.desc=stackscore'
        response = requests.get(url).json()
        context['response'] = response
        return context

