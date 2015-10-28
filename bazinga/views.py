from django.views.generic import TemplateView
from django import forms
from projects.models import *
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import Http404
from .models import Todo
from django.template import *
from django.template import RequestContext


# def home(request):
# 	return render_to_response('userena/profile_form.html', {}, context_instance=RequestContext(request))



class HomeView(TemplateView):
    template_name = "index.html"

class ProjectsView(TemplateView):
    template_name = "projects.html"



def todolist(request):
	user = User.objects.get(username=request.user.username)
	todolist = Todo.objects.filter(flag=1,user_id=user)
	finishtodos = Todo.objects.filter(flag=0,user_id=user)
	return render_to_response('simpleTodo.html',
		{'todolist': todolist, 'finishtodos': finishtodos},
		context_instance=RequestContext(request))

def todofinish(request, id=''):
	todo = Todo.objects.get(id=id)
	if todo.flag == '1':
		todo.flag = '0'
		todo.save()
		return HttpResponseRedirect('/todo/')
	user = User.objects.get(username=request.user.username)
	todolist = Todo.objects.filter(flag=1, user_id=user)
	return render_to_response('simpleTodo.html', {'todolist': todolist},
		context_instance=RequestContext(request))


def todoback(request, id=''):
	todo = Todo.objects.get(id=id)
	user = User.objects.get(username=request.user.username)
	if todo.flag == '0':
		todo.flag = '1'
		todo.save()
		return HttpResponseRedirect('/todo/')
		todolist = Todo.objects.filter(flag=1, user_id=user)
	return render_to_response('simpleTodo.html', {'todolist': todolist},
		context_instance=RequestContext(request))


def tododelete(request, id=''):
	try:
		todo = Todo.objects.get(id=id)
	except Exception:
		raise Http404
	if todo:
		todo.delete()
		return HttpResponseRedirect('/todo/')
	user = User.objects.get(username=request.user.username)
	todolist = Todo.objects.filter(flag=1, user_id=user)
	return render_to_response('simpleTodo.html', {'todolist': todolist},
		context_instance=RequestContext(request))


def addTodo(request):
	if request.method == 'POST':
		atodo = request.POST['todo']
		priority = request.POST['priority']
		user = User.objects.get(username=request.user.username)
		todo = Todo(user=user, todo=atodo, priority=priority, flag='1')
		todo.save()
		user = User.objects.get(username=request.user.username)
		todolist = Todo.objects.filter(flag=1, user_id=user)
		finishtodos = Todo.objects.filter(flag=0, user_id=user)
		return render_to_response('simpleTodo.html',
			{'todolist': todolist, 'finishtodos': finishtodos},
			context_instance=RequestContext(request))
	else:
		user = User.objects.get(username=request.user.username)
		todolist = Todo.objects.filter(flag=1, user_id=user)
		finishtodos = Todo.objects.filter(flag=0, user_id=user)
		return render_to_response('simpleTodo.html',
			{'todolist': todolist, 'finishtodos': finishtodos})


def updatetodo(request, id=''):
	if request.method == 'POST':
		print 'ddd'
		atodo = request.POST['todo']
		priority = request.POST['priority']
		user = User.objects.get(username=request.user.username)
		todo = Todo(user=user, todo=atodo, priority=priority, flag='1')
		todo.save()
		todolist = Todo.objects.filter(flag=1, user_id=user)
		finishtodos = Todo.objects.filter(flag=0, user_id=user)
		return render_to_response('simpleTodo.html',
			{'todolist': todolist, 'finishtodos': finishtodos},
			context_instance=RequestContext(request))
	else:
		try:
			todo = Todo.objects.get(id=id)
		except Exception:
			raise Http404
		return render_to_response('updatatodo.html', {'todo': todo},
			context_instance=RequestContext(request))


# def site_info(request, template_name='django_messages/inbox.html'):

# 	site_info = RequestContext(request)
# 	# return render_to_response(template_name, site_info)
# 	print "======================================================="
# 	print "ok"
# 	print "======================================================="
# 	return render_to_response(template_name, context, context_instance=RequestContext(request))

def details(request, template_name="index.html"):
	return render_to_response(template_name, context, context_instance=RequestContext(request))