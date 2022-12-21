from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown

from . import util

class newPageEntry(forms.Form):
    pageTitle = forms.CharField(label = "Title")
    pageContent = forms.CharField(label= "Content")
    pageTitle.widget.attrs.update({'placeholder': 'Title'})
    pageContent.widget.attrs.update({'placeholder': 'Content'})

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
# Create form using the Django method / 1hr 19mins into the lecture...
def create_entry(request):
    if request.method == "POST":
        form = newPageEntry(request.POST)
        #Figure out how to add both Title and Content!! CONTINUE VID ON SESSIONS TIMEMARK
        if form.is_valid():
            title = form.cleaned_data["Title"]
            content = form.cleaned_data["Content"]
            # Use the util function to save
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/create-entry.html", {
                "form": form
            } )
    return render(request, "encyclopedia/create-entry.html", {
        "form": newPageEntry()
    })

def search_page(request):
    if request.method == "POST":
        searchQuery = request.POST.get('q')
        fetchEntry = util.get_entry(searchQuery)
        ######## CONTINUE HERE
        if fetchEntry == None:
            entries = util.list_entries()
            queryMatches = str for str in entries if any(sub in str for sub in searchQuery) #entries and then have some sort of a function that sort it out
            #Here the page must display all the search elements that partially match the query
            return render(request, "encyclopedia/search-page.html", {
                "entries": queryMatches
                })
        else:
            return HttpResponseRedirect(f"/{searchQuery}")
            
            #render(request, "encyclopedia/entry-page.html", {
             #   "entry": markdown.markdown(fetchEntry)
            #})
        ######## CONTINUE HERE