from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from random import choice
from markdown2 import Markdown

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)

    if entry:
        return render(request, 'encyclopedia/entry.html', {
            'title': title,
            'content': markdowner.convert(entry)
        })
    else:
        return render(request, 'encyclopedia/error.html')


def search(request):
    query = request.GET['q']
    entry = util.get_entry(query)

    if entry:
        return redirect('entry', title=query)

    entries = util.list_entries()
    matches = []

    for ent in entries:
        if query.lower() in ent.lower():
            matches.append(ent)

    if not matches:
        return render(request, 'encyclopedia/error.html', {
            'message': 'Page doesn\'t exist'
        })
    else:
        return render(request, 'encyclopedia/search.html', {
            'matches': matches
        })


def new(request):
    if request.method == 'POST':
        entries = util.list_entries()
        title = request.POST['title']
        content = request.POST['content']

        if title in entries:
            return render(request, 'encyclopedia/error.html', {
                'message': 'Page already exists'
            })
        else:
            util.save_entry(title, content)
            return redirect('entry', title=title)
    else:
        return render(request, 'encyclopedia/new.html')

def edit(request, title):
    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        util.save_entry(title, new_content)
        return redirect('entry', title=title)
    else:
        return render(request, 'encyclopedia/edit.html', {
            'title': title,
            'content': util.get_entry(title)
        })

def random(request):
    return redirect('entry', title=choice(util.list_entries()))
