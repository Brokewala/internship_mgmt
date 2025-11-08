from django.contrib import admin

from .models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ("affectation", "evaluator", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("affectation__student__username", "evaluator__username")

