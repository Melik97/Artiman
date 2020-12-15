from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views import View
from .bot_perform import main



def home(request):
    main()
    return render(request, 'home.html')
    # return HttpResponse(template.render(context,request))
