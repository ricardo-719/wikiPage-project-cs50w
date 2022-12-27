from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
import markdown
import random

from . import util

class newPageEntry(forms.Form):
    pageTitle = forms.CharField(label = "Title")
    pageContent = forms.CharField(widget=forms.Textarea(attrs={"rows":"4"}), label="Content")
    pageTitle.widget.attrs.update({'placeholder': 'Title'})
    pageContent.widget.attrs.update({'placeholder': 'Content'})

def index(request):
    # Importing random for the random functionality
    randomEntryList = random.sample(util.list_entries(), 1)
    randomEntry=""
    for e in randomEntryList:
        randomEntry += e
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "randomEntry": randomEntry
    })

# Fetch the requested page, redirects users to error page if not found
def read_page(request, name):
    entry = util.get_entry(name)
    if entry == None:
        return render(request, "encyclopedia/404PageNotFound.html")
    else:
        return render(request, "encyclopedia/entry-page.html", {
            "name": name.capitalize(),
            "entry": markdown.markdown(entry)
        })

# Allow user to input a new entry
def create_entry(request):
    if request.method == "POST":
        form = newPageEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["pageTitle"]
            content = form.cleaned_data["pageContent"]
            fetchEntry = util.get_entry(title)
            if fetchEntry == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))
            else:
                messages.add_message(request, messages.INFO, 'Oops! This entry already exist.')    
                return render(request, "encyclopedia/create-entry.html", {
                    "form":form
                })
        else:
            return render(request, "encyclopedia/create-entry.html", {
                "form": form
            } )
    return render(request, "encyclopedia/create-entry.html", {
        "form": newPageEntry()
    })

def edit_entry(request):
    if request.method == "POST":
        # Edit has two "POST" access points, the first conditional if helps distinguish the source
        edit = {"Edit": ["Edit"]}
        if request.POST["editBtn"] == edit["Edit"][0]:
            title = request.POST["Edit"]
            content = util.get_entry(title)
            return render(request, "encyclopedia/edit-entry.html", {
                    "title": title,
                    "content": content
                })
        else:
            form = request.POST
            title = form['entryTitle']
            content = form['entryContent']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "encyclopedia/404PageNotFound.html") 

def search_page(request):
    if request.method == "POST":
        searchQuery = request.POST.get('q')
        fetchEntry = util.get_entry(searchQuery)
        if fetchEntry == None:
            entries = util.list_entries()
            #queryMatches = []
            #for i in searchQuery:
                #for j in entries:
                    #if(j.find(i) != -1 and j not in queryMatches):
                        #queryMatches.append(j)
            queryMatches = [str for str in entries if any(sub in str for sub in searchQuery)]
            if len(queryMatches) >= 1:
                return render(request, "encyclopedia/search-page.html", {
                    "entries": queryMatches
                    })
            else:
                return render(request, "encyclopedia/404PageNotFound.html")
        else:
            return HttpResponseRedirect(f"/{searchQuery}")
            
            #render(request, "encyclopedia/entry-page.html", {
             #   "entry": markdown.markdown(fetchEntry)
            #})