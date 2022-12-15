from django.shortcuts import render
import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    #Experimenting with the code
def read_page(request, name):
    entry = util.get_entry(name)
    return render(request, "encyclopedia/entry-page.html", {
        "name": name.capitalize(),
        "entry": markdown.markdown(entry)
        })