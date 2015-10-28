from django import forms
from projects.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
import urllib2
import json


class Project(forms.ModelForm):
	"""docstring for Project"""
	class Meta:
		model = Projects
		exclude = ['created_on', 'updated_on']
		widgets = {
			'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
			'name': forms.TextInput(attrs = {'autofocus':"autofocus"})
			}
	
	@staticmethod    
	@csrf_exempt
	def List_all_project(request):
		prject_list = Projects.objects.all()
		paginator = Paginator(prject_list, 10) # Show 25 contacts per page
		page_range = paginator.page_range
		page = request.GET.get('page')
		try:
			projects = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			projects = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			projects = paginator.page(paginator.num_pages, page_range=1)    
		return render_to_response('projects.html', {'resource':'projects', 'project_list' : projects, 'page_range' : page_range}, context_instance=RequestContext(request))

	@staticmethod
	@csrf_exempt
	def get_repo_info(request):
		response = urllib2.urlopen('https://api.github.com/users/moztn/repos')
		data = json.load(response)
		
		paginator = Paginator(data, 10) # Show 25 contacts per page
		page_range = paginator.page_range
		page = request.GET.get('page')
		try:
			projects = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			projects = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			projects = paginator.page(paginator.num_pages, page_range=1)    
		return render_to_response('projects.html', {'data':projects}, context_instance=RequestContext(request))

	@staticmethod	
	@csrf_exempt
	def get_repo_details(request):
		repo_name = request.GET.get('repo')
		repo_url = 'https://api.github.com/repos/moztn/'+repo_name
		response = urllib2.urlopen(repo_url)
		data = json.load(response)

		contrib_url = data['contributors_url']
		contrib_response = urllib2.urlopen(contrib_url)
		contrib_data = json.load(contrib_response)

		language_url = data['languages_url']
		language_response = urllib2.urlopen(language_url)
		language_data = json.load(language_response)

		activity_url = data['events_url']
		activity_response = urllib2.urlopen(activity_url)
		act_data = json.load(activity_response)

		paginator = Paginator(act_data, 10) # Show 25 contacts per page
		page_range = paginator.page_range
		page = request.GET.get('page')
		try:
			activity_data = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			activity_data = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			activity_data = paginator.page(paginator.num_pages, page_range=1)

		return render_to_response('projects_details.html', {'data':data, 'contrib_data':contrib_data, 'language_data':language_data, 'activity_data':activity_data}, context_instance=RequestContext(request))
