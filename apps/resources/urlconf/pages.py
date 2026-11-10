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
    video_guide_view,
    topics_tree_view,
    menu_fragment_view,
    search_view,
    search_suggest_view,
    grade_page_view,
    pricing_view,
    feedback_view,
    teacher_comments_view,
    page_reaction_view,
    test_maker_view,
    test_maker_result_view,
    test_maker_pdf_view,
)
from apps.resources.views.tours import tour_seen_view

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
    path('video-koldonmo/', video_guide_view, name='video_guide'),
    path('topics/', topics_tree_view, name='topics_tree'),
    path('menu/', menu_fragment_view, name='menu_fragment'),
    path('pricing/', pricing_view, name='pricing'),
    path('search/', search_view, name='search'),
    path('search/suggest/', search_suggest_view, name='search_suggest'),
    # One page per class, linked from the footer (not the menu).
    path('<int:grade>-klass/', grade_page_view, name='grade_page'),

    path('tour-seen/', tour_seen_view, name='tour_seen'),
    path('test-tuzuu/', test_maker_view, name='test_maker'),
    path('test-tuzuu/<int:pk>/pdf/', test_maker_pdf_view, name='test_maker_pdf'),
    path('test-tuzuu/<int:pk>/', test_maker_result_view, name='test_maker_result'),

    path('pikir/', feedback_view, name='feedback'),
    path('pikirler/', teacher_comments_view, name='teacher_comments'),
    path('page-reaction/', page_reaction_view, name='page_reaction'),
]
