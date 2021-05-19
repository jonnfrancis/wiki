import markdown2
import secrets
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.urls import reverse

from . import util
from markdown2 import Markdown


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


def random(request):
    entries =util.list_entries()
    entry_random = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={
        'entry':entry_random
        }))

