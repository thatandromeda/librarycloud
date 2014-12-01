from django.views.generic.edit import FormView

from forms import SubjectsForm
from search import LibraryCloud

class StackView(FormView):
    template_name = 'stackview.html'
    form_class = SubjectsForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(StackView, self).get_context_data(**kwargs)
        _ = LibraryCloud()
        if 'querystring' in self.request.session.keys():
            querystring = self.request.session.pop('querystring')
            results = _.search(querystring)
        else:
            results = _.search('women')
        context['results'] = results.items
        return context

    def form_valid(self, form):
        self.request.session['querystring'] = form.cleaned_data['querystring']
        return super(StackView, self).form_valid(form)
