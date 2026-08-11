from django.contrib import admin
from .models import (
    Subscription,
    ResearchProject,
    Resource,
    Summary,
    Citation,
    ComparisonTable,
    ComparisonRow,
)


admin.site.register(Subscription)
admin.site.register(ResearchProject)
admin.site.register(Resource)
admin.site.register(Summary)
admin.site.register(Citation)
admin.site.register(ComparisonTable)
admin.site.register(ComparisonRow)