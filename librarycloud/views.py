import random 

from django.views.generic.edit import FormView

from forms import SubjectsForm
from search import LibraryCloud

# Provides a list of searches we can use to populate the page when
# users first visit. StackView will choose randomly.
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
            # Use the user's search term, if available.
            querystring = self.request.session.pop('querystring')
            results = _.search(querystring)
            context['topic'] = querystring
        else:
            # Otherwise select randomly from our list of common subjects.
            topic = random.choice(TOPICS)
            results = _.search(topic)
            context['topic'] = topic
        context['results'] = results.items
        return context

    def form_valid(self, form):
        # Save the querystring for when we redisplay the page. Using sessions
        # rather than URL parameters to discourage URL hacking, to avoid having
        # to think about sanitizing user input - the form's CharField at least
        # does some rudimentary validation.
        self.request.session['querystring'] = form.cleaned_data['querystring']
        return super(StackView, self).form_valid(form)
