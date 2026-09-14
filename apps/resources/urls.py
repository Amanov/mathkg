# apps/resources/urls.py
from django.urls import path
from . import views

# urlpatterns = [
#     path('<slug:topic_slug>/', views.topic_detail, name='topic_detail'),
#     path('<slug:topic_slug>/<slug:subtopic_slug>/', views.subtopic_detail, name='subtopic_detail'),
#     path('<slug:topic_slug>/<slug:subtopic_slug>/<slug:subsubtopic_slug>/', views.subsubtopic_detail, name='subsubtopic_detail'),
    

    
# ]

urlpatterns = [

    path(
        'topic/<slug:topic_slug>/',
        views.topic_detail,
        name='topic_detail'
    ),

    path(
        'topic/<slug:topic_slug>/<slug:subtopic_slug>/',
        views.subtopic_detail,
        name='subtopic_detail'
    ),

    path(
        'topic/<slug:topic_slug>/<slug:subtopic_slug>/<slug:subsubtopic_slug>/',
        views.subsubtopic_detail,
        name='subsubtopic_detail'
    ),
]
