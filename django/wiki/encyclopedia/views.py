import random
import markdown2

from django import forms
from django.shortcuts import render
from django.http import QueryDict, HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    entry = request.GET.get('q', '')
    entries =  util.list_entries()

    if not entry:
        return render(request, "encyclopedia/index.html", {
            "entries": entries,
            "title": 'All pages'
        })
    
    content = util.get_entry(entry)

    if (content):
        return render(request, 'encyclopedia/wiki.html', {
            "entry": content,
            "entryTitle": entry
        })
    else:
        entries_searchable = []

        for entry_searchable in entries:
            if entry.lower() in entry_searchable.lower():
                entries_searchable.append(entry_searchable)

        return render(request, 'encyclopedia/index.html', {
            "entries": entries_searchable,
            "title": 'Results:'
        })   

def wiki(request, title):
    content = util.get_entry(title)
    html_content = markdown2.markdown(content, extras=["code-friendly"])

    if content:
        return render(request, 'encyclopedia/wiki.html', {
            "entry": html_content,
            "entryTitle": title
        })

    return render(request, 'encyclopedia/404.html')

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(), label='Title', required=True, )
    content = forms.CharField(widget=forms.Textarea(attrs={ "cols": "100", "rows": "10", "style": "width: auto; height: auto;" }), label='Content', required=True)

# the way which was teach in the class
def new_page(request):
    if not request.method == 'POST':
        return render(request, 'encyclopedia/new-page.html', { "form": NewPageForm() })
    print(request.POST)
    form = NewPageForm(request.POST)

    if not form.is_valid():
        return render(request, 'encyclopedia/new-page.html', {
            "form": NewPageForm(),
            'error_massage': 'Please, fill all of fields'
        })

    entry_title = form.cleaned_data['title']
    entry_content = form.cleaned_data['content']

    if util.get_entry(entry_title):
        return render(request, 'encyclopedia/new-page.html', {
            "form": NewPageForm(),
            'error_massage': 'This content already exist'
        })
    
    # util.save_entry(entry_title, entry_content)

    return HttpResponseRedirect(reverse('encyclopedia:wiki', args=[entry_title]))

def edit_entry(request, title):
    if request.method == 'POST':
        new_content_form = NewPageForm(request.POST)

        if not new_content_form.is_valid():
            return render(request, 'encyclopedia/edit-page.html', {
                "form": new_content_form,
                "title": title,
                "error_message": 'Please, fill all of fields!'
            })

        entry_title = new_content_form.cleaned_data['title']
        entry_content = new_content_form.cleaned_data['content']
        
        util.save_entry(entry_title, entry_content)
        
        return HttpResponseRedirect(reverse('encyclopedia:wiki', args=[entry_title]))


    entry_content = util.get_entry(title)
    form_content = QueryDict(mutable=True)
    form_content.__setitem__('title', title)
    form_content.__setitem__('content', entry_content)
    form = NewPageForm(form_content)

    return render(request, 'encyclopedia/edit-page.html', {
        "form": form,
        "title": title,
    })

def random_entry(request):
    entries = util.list_entries()
    entry_title = entries[random.randrange(len(entries))]

    return HttpResponseRedirect(reverse('encyclopedia:wiki', args=[entry_title]))

# I did on my own
# def new_page(request):
#     if not request.method == 'POST':
#         return render(request, 'encyclopedia/new-page.html', {
#             "form": NewPageForm()
#         })

#     request_body = QueryDict(request.body)
#     entry_title = QueryDict.get(request_body, 'title')
#     entry_content = QueryDict.get(request_body, 'content')

#     if util.get_entry(entry_title):
#         return render(request, 'encyclopedia/new-page.html', {
#             "form": NewPageForm(),
#             "error_massage": 'This Entry already exist',
#         })

#     util.save_entry(entry_title, entry_content)
    
#     return render(request, 'encyclopedia/wiki.html', {
#         "entry": entry_content,
#         "entryTitle": entry_title
#     })
