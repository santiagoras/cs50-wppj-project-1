#Momentarily HttpResponse imported to test views
from django.http import HttpResponse
from django.shortcuts import render


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Function to render wiki/entry view
def read_entry(request, entry):
    return render(request, "encyclopedia/wiki.html",{
        "entry": util.md2html(util.get_entry(entry))
    })

def write_entry(request):
    return render(request, "encyclopedia/contribution.html")

