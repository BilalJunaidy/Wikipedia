from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
import random

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


def newpage(request):
    if request.method == "POST":
        
        entries = util.list_entries()
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)

        if title in entries:
            return HttpResponse(f"A page with the title {title} already existed. We have overridden the previous Wiki entry content with the new content")

        url = f"http://localhost:8000/encyclopedia/wiki/{title}"
        return HttpResponseRedirect(url)
    
    
    return render(request, "encyclopedia/newpage.html")


def randompage(request):
    entries = util.list_entries()
    length = len(entries)

    index = random.randrange(0, length)

    title = entries[index]

    url = f"http://localhost:8000/encyclopedia/wiki/{title}"
    return HttpResponseRedirect(url)


def editpage(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content) 

        url = f"http://localhost:8000/encyclopedia/wiki/{title}"
        return HttpResponseRedirect(url)
        
        ##return HttpResponse(f"""You have just made a POST request. 
        ##The content you have submitted is {content}
        ##""")

    title = request.GET['title']
    content = util.get_entry(title)
    ##return HttpResponse(f"""
    ##You have just made a GET request
    ##The title of the page is {title}
    ##The content of the page are {content}
    ##""")

    return render(request, "encyclopedia/editpage.html", {
            "content":content, "title": title
        })
    

        







