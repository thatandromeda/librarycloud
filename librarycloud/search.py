"""
Largely ripped off from Chad Nelson's library for DPLA requests: see
https://github.com/bibliotechy/DPyLA/blob/master/dpla/api.py
"""

from requests import get
from requests.compat import urlencode

WOMEN = ["Women's Studies", "Feminism", "Women -- Biography",
         "Women social reformers", "Women and Literature", "Women scientists",
         "Women's Rights", "Women -- civil rights",
         "Women -- legal status, laws, etc.", "Women -- suffrage",
         "Feminist theory", "Feminism -- cross-cultural studies",
         "Feminism and higher education"]

WOMEN = map(str.lower, WOMEN)

AF_AM = ["African Americans", "African American authors",
         "African American women", "African American youth", "Blacks",
         "Civil rights", "Colonization",
         "National Association for the Advancement of Colored People",
         "Race identity", "Race relations", "African American arts",
         "Black nationalism"]

AF_AM = map(str.lower, AF_AM)

LGBT = ["Bisexuality", "Bisexuals", "Gay and Lesbian Studies",
        "Gay Liberation Movement", "Homophobia", "Homosexuality", "Lesbianism",
        "Lesbians", "Queer", "Queer theory", "Transgenderism",
        "Transgender people", "Transexualism", "Transexuals", "Transvestism",
        "Transvestites"]

LGBT = map(str.lower, LGBT)

class LibraryCloud():
    """
    Makes searches of the Harvard LibraryCloud v2 API.
    """

    def search(self, query=None, **kwargs):
        """
        Builds and performs an item search.
        query -- a simple search query. Boolean Search operators allowed.

        In theory we might allow other parameters to be passed. But we don't.
        """
        if not query and not kwargs:
            raise ValueError("You have not entered any search criteria")
        if query:
            kwargs['query'] = query

        request = Request(**kwargs)
        return Results(get(request.url).json(), request)

class Request():
    def __init__(self, query=None):
        # Build individual url fragments for different search criteria
        url_parts = []
        self.base_url = 'http://api.lib.harvard.edu/v2/items.json?'
        if query:
            url_parts.append(self._singleValueFormatter('subject.topic', query))
        # Now string all the chunks together
        self.url = self._buildUrl(url_parts)



    def _singleValueFormatter(self, param_name, value):
        """
        Creates an encoded URL fragment for parameters that contain only a
        single value.
        """
        return urlencode({param_name: value})


    def _buildUrl(self, url_parts=None):
        """
        Wow, this is terrible. At some point should be generalized to make the
        search type more flexible. Et cetera.
        """
        url = self.base_url + '%s&sort.desc=stackscore' % ''.join(url_parts)
        return url


class Results():
    """
    Gets desired information from the response and stashes it in a useful
    format for later consumption.
    """
    def __init__(self, response, request):
        self.request = request
        self.count = response['pagination']['numFound']
        self.items = []
        if 'items' in response.keys():
            self.items_raw = [item for item in response['items']]
            for item in self.items_raw:
                info = {}

                # Get the title.
                try:
                    title = item['mods']['titleInfo']['title']
                except TypeError:
                    title = item['mods']['titleInfo'][0]['title']
                info['title'] = title

                # Get the stackscore.
                stackscore = \
                    item['mods']['extension']['usageData']['stackScore']
                info['stackscore'] = stackscore

                # Get the subject. Note that this is a list of dicts, where each
                # dict can have a variety of attributes; authority and topic are
                # typical, but not required.
                subjects_raw = item['mods']['subject']
                info['subjects_raw'] = subjects_raw

                # Get an actually useful list of subjects
                subjects = []
                for subject in subjects_raw:
                    if 'authority' in subject.keys():
                        if subject['authority'] == 'lcsh':
                            # Only bother with one type for now, so as to avoid
                            # duplication.
                            if 'topic' in subject.keys():
                                # The topic may be returned as a single string
                                # or as a list of strings; we want to present a
                                # string to the template in all cases.
                                topic_raw = subject['topic']
                                if isinstance(topic_raw, list):
                                    topic = '/'.join(map(str, topic_raw))
                                else:
                                    topic = topic_raw

                                if topic not in subjects:
                                    # Occasionally the lists are duplicative, so
                                    # let's de-dupe.
                                    subjects.append(topic)
                info['subjects'] = subjects

                info['ism1'] = False
                info['ism2'] = False
                info['ism3'] = False

                if any(a.lower() in WOMEN for a in subjects):
                    info['ism1'] = True

                if any(a.lower() in AF_AM for a in subjects):
                    info['ism2'] = True

                if any(a.lower() in LGBT for a in subjects):
                    info['ism3'] = True

                self.items.append(info)
