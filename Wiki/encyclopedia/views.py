from django.shortcuts import render
from django import forms

from . import util

import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_content(title):
    entry = util.get_entry(title)
    if entry:
        html = markdown2.markdown(entry)
        return html
    else:
        return None

def entry(request, title):
    html = get_content(title)
    if html:
        return render(request, "encyclopedia/entry.html", {
            "name": title,
            "entry": html
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "The page you requested could not be found."
        })
    
def search_results(request):
    search = request.GET.get('q', '')
    entries = util.list_entries()
    cap_entries = [item.capitalize() for item in entries]
    if search.capitalize() in cap_entries:
        html = get_content(search)
        if html:
            return render(request, "encyclopedia/entry.html", {
                "name": search,
                "entry": html
            })
    else:
        return render(request, 'encyclopedia/search.html', {
            "entries": entries,
            "search": search
        })

class NewEntryTitle(forms.Form):
    title = forms.CharField(label="Title")

def new_page(request):
    if request.method == "POST":
        form = NewEntryTitle(request.POST)
        content = request.POST.get("markup_text")
        if form.is_valid():
            title = form.cleaned_data["title"]
        entries = util.list_entries()
        cap_entries = [item.capitalize() for item in entries]
        if title.capitalize() in cap_entries:
            return render(request, "encyclopedia/error.html", {
                "error": "This entry already exists."
            })
        else:
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return render(request, "encyclopedia/newpage.html", {
            "form": NewEntryTitle()
        })

def edit(request):
    title = request.GET.get('param')
    html = get_content(title)
    context = {
        'title': title,
        'content': html
    }
    if request.method == "POST":
        title = request.POST.get('param')
        content = request.POST.get("markup_text")
        util.save_entry(title, content)
        return entry(request, title)
    else:
        return render(request, "encyclopedia/edit.html", context)
    
def random_entry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    content = get_content(title)
    return render(request, "encyclopedia/entry.html", {
        "name": title,
        "entry": content
    })