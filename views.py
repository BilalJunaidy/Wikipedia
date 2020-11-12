from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    content = util.get_entry(title)

    if content is not None:

        content = Markdown().convert(f"{content}")
        return render(request, "encyclopedia/entry.html" ,{
            "title":title, "content": content
        })
        
    else:
        return HttpResponse("No such page was found")



def search(request):
    if request.method == "POST":

        entries = util.list_entries()
        query = request.POST['q']
        substring_match_list = []

        for entry in entries:
            if query == entry:
                url = f"http://localhost:8000/encyclopedia/wiki/{query}"
                return HttpResponseRedirect(url)

            elif not entry.find(query) == - 1:
                substring_match_list.append(entry)

        if len(substring_match_list) == 0:
            return HttpResponse("No such page was found")

        return render(request, "encyclopedia/search.html", {
            "lists":substring_match_list,"query":query
        })


        







