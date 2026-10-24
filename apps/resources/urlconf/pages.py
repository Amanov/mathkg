"""Dashboard, resource list, and the public site pages."""

from django.urls import path

from apps.resources.views import (
    dashboard_view,
    analytics_dashboard_view,
    resources_view,
    download_resource_view,
    track_click_view,
    news_list_view,
    about_view,
    topics_tree_view,
    search_view,
    search_suggest_view,
    pricing_view,
)

urlpatterns = [
    # Dashboard
    path('dashboard/', dashboard_view, name='dashboard'),
    path('analytics/', analytics_dashboard_view, name='analytics_dashboard'),
    path('track-click/', track_click_view, name='track_click'),

    # Resources
    path('resources/download/<int:pk>/', download_resource_view, name='download_resource'),
    path('resources/', resources_view, name='resources'),

    # Pages
    path('news/', news_list_view, name='news_list'),
    path('about/', about_view, name='about'),
    path('topics/', topics_tree_view, name='topics_tree'),
    path('pricing/', pricing_view, name='pricing'),
    path('search/', search_view, name='search'),
    path('search/suggest/', search_suggest_view, name='search_suggest'),
]
