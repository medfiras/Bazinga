from django.views.generic import TemplateView
from django import forms
from projects.models import *
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import Http404
from django.template import *
from django.template import RequestContext


# def home(request):
# 	return render_to_response('userena/profile_form.html', {}, context_instance=RequestContext(request))



class HomeView(TemplateView):
    template_name = "index.html"

class ProjectsView(TemplateView):
    template_name = "projects.html"

def details(request, template_name="index.html"):
	return render_to_response(template_name, context, context_instance=RequestContext(request))