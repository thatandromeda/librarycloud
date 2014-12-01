from django.views.generic import TemplateView

from search import LibraryCloud

class StackView(TemplateView):
    template_name = 'stackview.html'

    def get_context_data(self, **kwargs):
        context = super(StackView, self).get_context_data(**kwargs)
        _ = LibraryCloud()
        results = _.search('women')
        context['results'] = results.items
        return context
