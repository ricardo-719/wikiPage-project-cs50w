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
        #Figure out how to add both Title and Content!!
        if form.is_valid():
            title = form.cleaned_data["Title"]
            content = form.cleaned_data["Content"]
            entries.append(content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/create-entry.html", {
                "form": form
            } )
    return render(request, "encyclopedia/create-entry.html", {
        "form": newPageEntry()
    })