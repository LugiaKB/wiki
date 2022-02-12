from logging import PlaceHolder
from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
from random import choice


from . import util

class NewEntry(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Title'}), label='')
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Content'}), label="")

class EditEntry(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Content'}), label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    page = util.get_entry(name)
    if not page:
        return render(request, "encyclopedia/invalid.html",{
            "message" : 'Invalid entry.'
        })

    return render(request, "encyclopedia/entry.html", {
        "entry": name,
        "content": markdown(page)
    })

def new(request):
    if request.method == 'POST':
        new_entry = NewEntry(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data['title']
            content = new_entry.cleaned_data['content']
            entries = util.list_entries()
            if title in entries:
                return render(request, 'encyclopedia/invalid.html',{
                    'message': 'Entry already exists. Edit current entry instead of creating a new one.'
                })
            util.save_entry(title, content)
            return HttpResponseRedirect('/')
    return render(request, 'encyclopedia/new.html', {
        'form': NewEntry()
    })

def edit(request, name):
    if request.method == 'POST':
        edited = EditEntry(request.POST)
        if edited.is_valid():
            content = edited.cleaned_data['content']
            util.save_entry(name, content)
            return HttpResponseRedirect('/wiki/' + name)
    page = util.get_entry(name)
    if not page:
        return render(request, "encyclopedia/invalid.html",{
            "message" : 'Invalid entry.'
        })
    
    return render(request, 'encyclopedia/edit.html', {
        'form': EditEntry({'content': page}),
        'title': name
    })

def randompage():
    page = choice(util.list_entries())
    return HttpResponseRedirect('/wiki/' + page)

def search(request):
    item = request.POST.get('q')
    entries = util.list_entries()
    results = []
    for entry in entries:
        if item.casefold() == entry.casefold():
            return HttpResponseRedirect('/wiki/' + item)
        elif item.casefold() in entry.casefold():
            print(item)
            results.append(entry)
    if not results:
        return render(request, 'encyclopedia/invalid.html', {
            'message': "Query not found."
        })
    return render(request, 'encyclopedia/search.html', {
        'query': item,
        'results': results
    })
        
