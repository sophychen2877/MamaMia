from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime as dt

def home(request):
    #return HttpResponse('Hello')
    return render(request, 'home.html')
def count(request):
    fulltext = request.GET['fulltext']
    textlist = fulltext.split()
    worddic = {}
    for word in textlist:
        count=1
        if word in worddic:
            count+=1
        worddic[word] = count
    return render(request, 'count.html', {'fulltext': fulltext, 'counter': worddic.items()})

def about(request):
    time = dt.now()
    return render(request,'about.html', {'dt':time})
