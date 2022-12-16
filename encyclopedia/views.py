from django.shortcuts import render
import markdown

from . import util


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
def create_entry(request):
    return render(request, "encyclopedia/create-entry.html")