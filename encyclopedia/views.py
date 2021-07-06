import markdown2
import secrets
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse

from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title=forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={
       'class': 'form-control col-md-8 col-lg-8 ' 
    }))
    content=forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control col-md-8 col-lg-8 '
    }))
    edit=forms.BooleanField(initial=False,widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markdowner = Markdown()
    entrypage = util.get_entry(entry)
    if entrypage is not None:
        return render(request, "encyclopedia/entry.html",{
            "title_entry": entry,
            "entry":markdowner.convert(entrypage)
        }) 
    else:
        return render(request, "encyclopedia/noexistingEntry.html",{
            "title_entry" : entry
        })      


def random(request):
    entries =util.list_entries()
    entry_random = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={
        'entry':entry_random
        })) 


def search(request):
    value = request.GET.get('q',"")
    if(util.get_entry(value) is None):
        sub_entries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                sub_entries.append(entry)


        return render(request,"encyclopedia/index.html",{
            "entries": sub_entries,
            "search": True,
            "value": value
        }) 
    else:
        return HttpResponseRedirect(reverse("entry",kwargs={
            'entry': value
        }))           

def edit(request, entry):
    entrypage = util.get_entry(entry)
    if entrypage is not None:
        form = NewEntryForm()
        form.fields['title'].initial = entry
        form.fields['title'].widget = forms.HiddenInput()
        form.fields['content'].initial = entrypage
        form.fields['edit'].initial = True
        return render(request, "encyclopedia/newEntry.html",{
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle":form.fields['title'].initial
        })
    else:
        return render(request, "encyclopedia/noexistingEntry.html",{
            "entryTitle": entry
        }) 
def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title'] 
            content = form.cleaned_data['content']
            if (util.get_entry(title)) is None or form.cleaned_data['edit'] is True:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('entry', kwargs = {
                    'entry': title
                }))       
            else:
                return render(request, "encyclopedia/newEntry.html",{
                    'form': form,
                    'existing': True,
                    'entry': title
                }) 
        else:
            return render(request, "encyclopedia/newEntry.html",{
              'form': form,
              'existing': False,
            })                           
    else:
        return render(request, "encyclopedia/newEntry.html",{
            "form": NewEntryForm(),
            "existing": False
        })            

