from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'todolist.views.list_lists', name="todo-lists"),
    url(r'^mine/$', 'todolist.views.view_list', {'list_slug': 'mine'}, name="todo-mine"),
    url(r'^(?P<list_id>\d{1,4})/(?P<list_slug>[\w-]+)/delete$', 'todolist.views.del_list', name="todo-del_list"),
    url(r'^(?P<list_id>\d{1,6})/edit$', 'todolist.views.edit_list', name="todo-edit_list"),
    url(r'^task/(?P<task_id>\d{1,6})$', 'todolist.views.view_task', name='todo-task_detail'),
    url(r'^(?P<list_id>\d{1,4})/(?P<list_slug>[\w-]+)$', 'todolist.views.view_list', name='todo-incomplete_tasks'),
    url(r'^(?P<list_id>\d{1,4})/(?P<list_slug>[\w-]+)/completed$', 'todolist.views.view_list', {'view_completed': 1},
        name='todo-completed_tasks'),
    url(r'^add_list/$', 'todolist.views.add_list', name="todo-add_list"),
    url(r'^search-post/$', 'todolist.views.search_post', name="todo-search-post"),
    url(r'^search/$', 'todolist.views.search', name="todo-search"),

    # View reorder_tasks is only called by JQuery for drag/drop task ordering
    url(r'^reorder_tasks/$', 'todolist.views.reorder_tasks', name="todo-reorder_tasks"),

    url(r'^ticket/add/$', 'todolist.views.external_add', name="todo-external-add"),
    url(r'^recent/added/$', 'todolist.views.view_list', {'list_slug': 'recent-add'}, name="todo-recently_added"),
    url(r'^recent/completed/$', 'todolist.views.view_list', {'list_slug': 'recent-complete'},
        name="todo-recently_completed"),
)
