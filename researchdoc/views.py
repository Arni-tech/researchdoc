from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden

from .forms import (
    CitationForm,
    ComparisonTableForm,
    ResearchProjectForm,
    ResourceForm,
    SignUpForm,
    SummaryForm,
    SubscriptionForm,
)
from .models import ResearchProject, Resource, Summary, Citation, ComparisonTable, ComparisonRow, Subscription
from .forms import ResearchProjectForm, ResourceForm, SummaryForm, CitationForm, ComparisonTableForm, ComparisonRowForm, SubscriptionForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator


def staff_required(user):
    return user.is_authenticated and user.is_staff

def landing(request):
    return render(request, "researchdoc/landing.html")

def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("project_list")
    else:
        form = SignUpForm()

    context = {
        "form": form
    }

    return render(request, "researchdoc/signup.html", context)


class CustomLoginView(LoginView):
    template_name = "researchdoc/login.html"

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("landing")


@login_required
def project_list(request):
    projects = ResearchProject.objects.filter(user=request.user).order_by("-updated_at")

    context = {
        "projects": projects
    }

    return render(request, "researchdoc/project_list.html", context)


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id, user=request.user)
    resources = Resource.objects.filter(project=project).order_by("-updated_at")
    summaries = Summary.objects.filter(project=project).order_by("-updated_at")
    comparison_tables = ComparisonTable.objects.filter(project=project).order_by("-updated_at")

    context = {
        "project": project,
        "resources": resources,
        "summaries": summaries,
        "comparison_tables": comparison_tables,
    }

    return render(request, "researchdoc/project_detail.html", context)
@login_required
def resource_create(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id, user=request.user)

    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)

        if form.is_valid():
            resource = form.save(commit=False)
            resource.project = project
            resource.save()

            messages.success(request, "Resource added successfully.")
            return redirect("project_detail", project_id=project.id)
    else:
        form = ResourceForm()

    context = {
        "form": form,
        "project": project,
        "page_title": "Add Resource",
        "button_text": "Save Resource",
    }

    return render(request, "researchdoc/resource_form.html", context)


@login_required
def resource_edit(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, project__user=request.user)
    project = resource.project

    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES, instance=resource)

        if form.is_valid():
            form.save()
            messages.success(request, "Resource updated successfully.")
            return redirect("project_detail", project_id=project.id)
    else:
        form = ResourceForm(instance=resource)

    context = {
        "form": form,
        "project": project,
        "resource": resource,
        "page_title": "Edit Resource",
        "button_text": "Update Resource",
    }

    return render(request, "researchdoc/resource_form.html", context)


@login_required
def resource_delete(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id, project__user=request.user)
    project = resource.project

    if request.method == "POST":
        resource.delete()
        messages.success(request, "Resource deleted successfully.")
        return redirect("project_detail", project_id=project.id)

    context = {
        "resource": resource,
        "project": project,
    }

    return render(request, "researchdoc/resource_confirm_delete.html", context)

@login_required
def summary_create(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id, user=request.user)

    if request.method == "POST":
        form = SummaryForm(request.POST)

        if form.is_valid():
            summary = form.save(commit=False)
            summary.project = project
            summary.save()

            messages.success(request, "Summary created successfully. You can now add citations.")
            return redirect("summary_edit", summary_id=summary.id)

    else:
        form = SummaryForm()

    context = {
        "form": form,
        "project": project,
        "page_title": "Create Summary",
        "button_text": "Create Summary",
        "summary": None,
        "citations": [],
        "citation_form": None,
    }

    return render(request, "researchdoc/summary_form.html", context)


@login_required
def summary_edit(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id, project__user=request.user)
    project = summary.project
    citations = Citation.objects.filter(summary=summary).order_by("-created_at")

    if request.method == "POST":
        form = SummaryForm(request.POST, instance=summary)

        if form.is_valid():
            form.save()
            messages.success(request, "Summary updated successfully.")

            if "save_and_back" in request.POST:
                return redirect("project_detail", project_id=project.id)

            return redirect("summary_edit", summary_id=summary.id)
    else:
        form = SummaryForm(instance=summary)

    context = {
        "form": form,
        "project": project,
        "summary": summary,
        "citations": citations,
        "citation_form": CitationForm(),
        "page_title": "Edit Summary",
        "button_text": "Update Summary",
    }

    return render(request, "researchdoc/summary_form.html", context)


@login_required
def summary_delete(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id, project__user=request.user)
    project = summary.project

    if request.method == "POST":
        summary.delete()
        messages.success(request, "Summary deleted successfully.")
        return redirect("project_detail", project_id=project.id)

    context = {
        "summary": summary,
        "project": project,
    }

    return render(request, "researchdoc/summary_confirm_delete.html", context)


@login_required
def citation_create(request, summary_id):
    summary = get_object_or_404(Summary, id=summary_id, project__user=request.user)

    if request.method == "POST":
        form = CitationForm(request.POST)

        if form.is_valid():
            citation = form.save(commit=False)
            citation.summary = summary
            citation.save()

            messages.success(request, "Citation added successfully.")
            return redirect("summary_edit", summary_id=summary.id)

    messages.error(request, "Citation could not be added.")
    return redirect("summary_edit", summary_id=summary.id)


@login_required
def citation_delete(request, citation_id):
    citation = get_object_or_404(Citation, id=citation_id, summary__project__user=request.user)
    summary = citation.summary

    if request.method == "POST":
        citation.delete()
        messages.success(request, "Citation deleted successfully.")

    return redirect("summary_edit", summary_id=summary.id)

@login_required
def comparison_create(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id, user=request.user)

    if request.method == "POST":
        form = ComparisonTableForm(request.POST)
        if form.is_valid():
            comparison_table = form.save(commit=False)
            comparison_table.project = project
            comparison_table.save()

            # Create default starter rows
            default_rows = ["Pricing", "Features", "Strengths", "Weaknesses"]
            for index, criterion in enumerate(default_rows, start=1):
                ComparisonRow.objects.create(
                    table=comparison_table,
                    criterion=criterion,
                    order=index
                )

            messages.success(request, "Comparison table created successfully.")
            return redirect("comparison_edit", comparison_id=comparison_table.id)
    else:
        form = ComparisonTableForm()

    return render(request, "researchdoc/comparison_form.html", {
        "form": form,
        "project": project,
        "comparison_table": None,
        "rows": [],
        "page_title": "Create Comparison Table",
        "button_text": "Create Comparison Table",
    })

@login_required
def comparison_edit(request, comparison_id):
    comparison_table = get_object_or_404(
        ComparisonTable,
        id=comparison_id,
        project__user=request.user
    )
    project = comparison_table.project
    rows = comparison_table.rows.all()

    if request.method == "POST":
        form = ComparisonTableForm(request.POST, instance=comparison_table)

        if form.is_valid():
            form.save()

            for row in rows:
                row.criterion = request.POST.get(f"criterion_{row.id}", row.criterion)
                row.item_one_value = request.POST.get(f"item_one_value_{row.id}", row.item_one_value)
                row.item_two_value = request.POST.get(f"item_two_value_{row.id}", row.item_two_value)

                order_value = request.POST.get(f"order_{row.id}", row.order)
                try:
                    row.order = int(order_value)
                except ValueError:
                    pass

                row.save()

            messages.success(request, "Comparison table updated successfully.")
            return redirect("comparison_edit", comparison_id=comparison_table.id)
    else:
        form = ComparisonTableForm(instance=comparison_table)

    return render(request, "researchdoc/comparison_form.html", {
        "form": form,
        "project": project,
        "comparison_table": comparison_table,
        "rows": rows,
        "page_title": "Edit Comparison Table",
        "button_text": "Update Comparison Table",
    })
@login_required
def comparison_row_add(request, comparison_id):
    comparison_table = get_object_or_404(
        ComparisonTable,
        id=comparison_id,
        project__user=request.user
    )

    if request.method == "POST":
        next_order = comparison_table.rows.count() + 1
        ComparisonRow.objects.create(
            table=comparison_table,
            criterion="New criterion",
            order=next_order
        )
        messages.success(request, "Row added successfully.")

    return redirect("comparison_edit", comparison_id=comparison_table.id)


@login_required
def comparison_row_delete(request, row_id):
    row = get_object_or_404(
        ComparisonRow,
        id=row_id,
        table__project__user=request.user
    )
    comparison_table = row.table

    if request.method == "POST":
        row.delete()
        messages.success(request, "Row deleted successfully.")

    return redirect("comparison_edit", comparison_id=comparison_table.id)


@login_required
def comparison_delete(request, comparison_id):
    comparison_table = get_object_or_404(
        ComparisonTable,
        id=comparison_id,
        project__user=request.user
    )
    project = comparison_table.project

    if request.method == "POST":
        comparison_table.delete()
        messages.success(request, "Comparison table deleted successfully.")
        return redirect("project_detail", project_id=project.id)

    context = {
        "comparison_table": comparison_table,
        "project": project,
    }

    return render(request, "researchdoc/comparison_confirm_delete.html", context)

@login_required
def project_create(request):
    if request.method == "POST":
        form = ResearchProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            messages.success(request, "Research project created successfully.")
            return redirect("project_detail", project_id=project.id)
    else:
        form = ResearchProjectForm()

    context = {
        "form": form,
        "page_title": "Create Research Project",
        "button_text": "Save Project",
    }

    return render(request, "researchdoc/project_form.html", context)


@login_required
def project_edit(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id, user=request.user)

    if request.method == "POST":
        form = ResearchProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            messages.success(request, "Research project updated successfully.")
            return redirect("project_detail", project_id=project.id)
    else:
        form = ResearchProjectForm(instance=project)

    context = {
        "form": form,
        "project": project,
        "page_title": "Edit Research Project",
        "button_text": "Update Project",
    }

    return render(request, "researchdoc/project_form.html", context)


@login_required
def project_delete(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id, user=request.user)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Research project deleted successfully.")
        return redirect("project_list")

    context = {
        "project": project
    }

    return render(request, "researchdoc/project_confirm_delete.html", context)

@login_required
def search(request):
    query = request.GET.get("q", "").strip()

    resource_results = []
    summary_results = []

    if query:
        resource_results = Resource.objects.filter(
            project__user=request.user
        ).filter(
            Q(title__icontains=query) |
            Q(notes__icontains=query) |
            Q(full_text__icontains=query)
        ).order_by("-updated_at")

        summary_results = Summary.objects.filter(
            project__user=request.user
        ).filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).order_by("-updated_at")

    context = {
        "query": query,
        "resource_results": resource_results,
        "summary_results": summary_results,
    }

    return render(request, "researchdoc/search.html", context)

@login_required
def subscription_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    subscriptions = Subscription.objects.select_related("user").order_by("-updated_at")

    paginator = Paginator(subscriptions, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }

    return render(request, "researchdoc/subscription_list.html", context)

@login_required
def subscription_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    if request.method == "POST":
        form = SubscriptionForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Subscription created successfully.")
            return redirect("subscription_list")
    else:
        form = SubscriptionForm()

    context = {
        "form": form,
        "page_title": "Create Subscription",
        "button_text": "Save Subscription",
    }

    return render(request, "researchdoc/subscription_form.html", context)


@login_required
def subscription_edit(request, subscription_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    subscription = get_object_or_404(Subscription, id=subscription_id)

    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription)

        if form.is_valid():
            form.save()
            messages.success(request, "Subscription updated successfully.")
            return redirect("subscription_list")
    else:
        form = SubscriptionForm(instance=subscription)

    context = {
        "form": form,
        "subscription": subscription,
        "page_title": "Edit Subscription",
        "button_text": "Update Subscription",
    }

    return render(request, "researchdoc/subscription_form.html", context)


@login_required
def subscription_archive(request, subscription_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to access this page.")

    subscription = get_object_or_404(Subscription, id=subscription_id)

    if request.method == "POST":
        subscription.status = "archived"
        subscription.is_archived = True
        subscription.save()

        messages.success(request, "Subscription archived successfully.")
        return redirect("subscription_list")

    context = {
        "subscription": subscription
    }

    return render(request, "researchdoc/subscription_confirm_archive.html", context)