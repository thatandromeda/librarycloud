import random 

from django.views.generic.edit import FormView

from forms import SubjectsForm
from search import LibraryCloud

TOPICS = ["Political science", "Computer science", "Economics",
          "Philology, Modern", "Ethics", "Biotechnology", "Philosophy",
          "Religion", "American history", "Art", "English language",
          "Education", "World history", "International relations"]

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
            context['topic'] = querystring
        else:
            topic = random.choice(TOPICS)
            results = _.search(topic)
            context['topic'] = topic
        context['results'] = results.items
        return context

    def form_valid(self, form):
        self.request.session['querystring'] = form.cleaned_data['querystring']
        return super(StackView, self).form_valid(form)
