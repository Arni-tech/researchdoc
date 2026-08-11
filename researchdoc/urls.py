from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),

    path("signup/", views.signup_view, name="signup"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("projects/", views.project_list, name="project_list"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<int:project_id>/", views.project_detail, name="project_detail"),
    path("projects/<int:project_id>/edit/", views.project_edit, name="project_edit"),
    path("projects/<int:project_id>/delete/", views.project_delete, name="project_delete"),
    path("projects/<int:project_id>/resources/new/", views.resource_create, name="resource_create"),
    path("resources/<int:resource_id>/edit/", views.resource_edit, name="resource_edit"),
    path("resources/<int:resource_id>/delete/", views.resource_delete, name="resource_delete"),
    path("projects/<int:project_id>/summaries/new/", views.summary_create, name="summary_create"),
    path("summaries/<int:summary_id>/edit/", views.summary_edit, name="summary_edit"),
    path("summaries/<int:summary_id>/delete/", views.summary_delete, name="summary_delete"),

    path("summaries/<int:summary_id>/citations/new/", views.citation_create, name="citation_create"),
    path("citations/<int:citation_id>/delete/", views.citation_delete, name="citation_delete"),
    path("projects/<int:project_id>/comparisons/new/", views.comparison_create, name="comparison_create"),
    path("comparisons/<int:comparison_id>/edit/", views.comparison_edit, name="comparison_edit"),
    path("comparisons/<int:comparison_id>/delete/", views.comparison_delete, name="comparison_delete"),
    path("search/", views.search, name="search"),
    path("subscriptions/", views.subscription_list, name="subscription_list"),
    path("subscriptions/new/", views.subscription_create, name="subscription_create"),
    path("subscriptions/<int:subscription_id>/edit/", views.subscription_edit, name="subscription_edit"),
    path("subscriptions/<int:subscription_id>/archive/", views.subscription_archive, name="subscription_archive"),
    path("comparisons/<int:comparison_id>/rows/add/", views.comparison_row_add, name="comparison_row_add"),
    path("comparison-rows/<int:row_id>/delete/", views.comparison_row_delete, name="comparison_row_delete"),
]