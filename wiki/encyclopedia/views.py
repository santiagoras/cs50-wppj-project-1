#Momentarily HttpResponse imported to test views
from django import forms
from django.http import HttpResponse
from django.shortcuts import render
import random



from . import util

class WikiArticleForm(forms.Form):
    title = forms.CharField(label=False, widget=forms.TextInput(attrs={"placeholder":"Article's title"}))
    content = forms.CharField(label=False, widget=forms.Textarea(attrs={"placeholder":"Article's content"}))
    
class WikiEditForm(forms.Form):
    content = forms.CharField(label=False, widget=forms.Textarea(attrs={"placeholder":"Article's content"}))


def index(request):
    if request.method == "POST":
        if request.POST['q'] in util.list_entries():
            return render(request, "encyclopedia/wiki.html", {
                "entry": util.md2html(util.get_entry(request.POST['q'])),
                "title": request.POST['q']
            })
        s_results=[]
        for entry in util.list_entries():
            if entry.casefold().find(request.POST['q'].casefold()) != -1:
                s_results.append(entry)
                print(s_results)
        if s_results:
            return render(request, "encyclopedia/index.html", {
                "entries": s_results,
                "l_type": "Search results"
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": s_results,
                "l_type": "Search results",
                "alert": "your search didn't match any articles"
            })

        
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "l_type": "All pages"
    })

# Function to render wiki/entry view
def read_entry(request, entry):
    return render(request, "encyclopedia/wiki.html", {
        "entry": util.md2html(util.get_entry(entry)),
        "title": entry
    })

def random_entry(request):
    entryList = util.list_entries()
    random.seed()
    ranen = entryList[random.randint(0, len(entryList)-1)]
    return render(request, "encyclopedia/wiki.html",{
        "entry": util.md2html(util.get_entry(ranen)),
        "title": ranen
    })


def write_entry(request):
    if request.method == "POST":
        form = WikiArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title in util.list_entries():
                return render(request, "encyclopedia/contribution.html", {
                'form': form,
                'alert': 'this entry already Exist! You may want to edit it.'
            })
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/wiki.html",{
            "entry": util.md2html(util.get_entry(title)),
            "title": title
            })

        else:
            return render(request, "encyclopedia/contribution.html", {
                'form': form,
                'alert': 'this entry already Exist! You may want to edit it.'
            })

    return render(request, "encyclopedia/contribution.html", {
        "form": WikiArticleForm()
    })

def edit_entry(request, entry):

    if request.method == "POST":
        form = WikiEditForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['content'] == "":
                return render(request, "encyclopedia/contribution.html", {
                'form': form,
                'alert': 'You shoud write something, not delete it!'
            })
            content = form.cleaned_data['content']
            util.save_entry(entry, content)
            return render(request, "encyclopedia/wiki.html", {
            "entry": util.md2html(util.get_entry(entry)),
            "title": entry
            })


    return render(request, "encyclopedia/edit.html", {
        "form": WikiEditForm(initial={'content':util.get_entry(entry)}),
        "title": entry
    })


