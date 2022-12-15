from django.shortcuts import render
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    #Experimenting with the code
def read_page(request, name):
    entry = util.get_entry(name)
    entryHtml = mdConverter(entry)
    return render(request, "encyclopedia/entry-page.html", {
        "name": name,
        "entry": entryHtml
        })

def mdConverter(md):
    print (re.sub('^#{1} (.+)$', '<h1>\\1</h1>', md))
    return re.sub('^#{1} (.+)$', '<h1>\\1</h1>', md)
