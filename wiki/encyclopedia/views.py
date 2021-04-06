#Momentarily HttpResponse imported to test views
from django import forms
from django.http import HttpResponse
from django.shortcuts import render


from . import util

class WikiArticleForm(forms.Form):
    title = forms.CharField(label="Article's title")
    content = forms.CharField(label="Article's content", widget=forms.Textarea)


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
        "entry": util.md2html(util.get_entry(title))
    })

        else:
            return render(request, "encyclopedia/contribution.html", {
                'form': form,
                'alert': 'this entry already Exist! You may want to edit it.'
            })

    return render(request, "encyclopedia/contribution.html", {
        "form": WikiArticleForm()
    })

