from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    PLAN_CHOICES = [
        ("Free", "Free"),
        ("Standard", "Standard"),
        ("Premium", "Premium"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("archived", "Archived"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=50, choices=PLAN_CHOICES, default="Free")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def archive(self):
        self.status = "archived"
        self.is_archived = True
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.plan_name}"


class ResearchProject(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("archived", "Archived"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    topic = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Resource(models.Model):
    RESOURCE_TYPES = [
        ("paper", "Paper"),
        ("link", "External Link"),
    ]

    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file = models.FileField(upload_to="papers/", blank=True, null=True)
    external_url = models.URLField(max_length=500, blank=True)
    notes = models.TextField(blank=True)
    full_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Summary(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name="summaries")
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Citation(models.Model):
    summary = models.ForeignKey(Summary, on_delete=models.CASCADE, related_name="citations")
    citation_text = models.TextField()
    source_title = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source_title or self.citation_text[:50]


class ComparisonTable(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name="comparison_tables")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    item_one = models.CharField(max_length=100, default="Item A")
    item_two = models.CharField(max_length=100, default="Item B")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ComparisonRow(models.Model):
    table = models.ForeignKey(ComparisonTable, on_delete=models.CASCADE, related_name="rows")
    criterion = models.CharField(max_length=100)
    item_one_value = models.TextField(blank=True)
    item_two_value = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.criterion