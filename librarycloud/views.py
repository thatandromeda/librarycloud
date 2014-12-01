from django.http import HttpResponse
from django.views.generic import TemplateView

import requests

from search import LibraryCloud

class StackView(TemplateView):
    template_name = 'stackview.html'

    def get_context_data(self, **kwargs):
        context = super(StackView, self).get_context_data(**kwargs)
        lc = LibraryCloud()
        results = lc.search('women')
        context['results'] = results.items
        return context

