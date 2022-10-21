from turtle import title
import markdown
import random
from django.shortcuts import render
from django.shortcuts import redirect
from . import util
from difflib import SequenceMatcher


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) != None:
        f = open("entries/" + title + ".md","r")
        f = f.read()
        html = markdown.markdown(f)
        return render(request, "encyclopedia/item.html",{
            "content": html,
            "entry": "true",
            "title": title
        })
    else:
        return render(request,"encyclopedia/apology.html",{
            "top":"400",
            "bottom":"Page not found!"
        })

def rand(request):
    entries = util.list_entries()
    selected_page = random.choice(entries)
    return redirect(f"wiki/{selected_page}")


def newpage(request):
    if request.method == "POST":
        pagename = request.POST["pagename"]
        content = request.POST["content"]
        for entry in util.list_entries():
            if entry == pagename:
                return render(request,"encyclopedia/apology.html",{
                "top":"400",
                "bottom":"Page already exists"
                })
        util.save_entry(pagename, content)
        return redirect(f"wiki/{pagename}")
    else:
        return render(request, "encyclopedia/newpage.html")

def editpage(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        open("entries/" + title + ".md", 'w').close()
        f = open("entries/" + title + ".md","a")
        f.write(content)
        return redirect(f"../wiki/{title}")
    else:
        f = open("entries/" + title + ".md","r")
        f = f.read()
        return render(request, "encyclopedia/editpage.html",{
            "content": f,
            "title": title
        })

def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        for entry in util.list_entries():
            if entry == title:
                return redirect(f"../wiki/{title}")
        search = []
        for entry in util.list_entries():
            if SequenceMatcher(a=entry,b=title).ratio() > 0.1:
                search.append(entry)
        return render(request, "encyclopedia/search.html",{
            "search": search
        })
    else:
        return redirect("/")
