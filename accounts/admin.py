from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.admin_mixins import AdminPageDescriptionMixin

from .models import User, UserProfile


@admin.register(User)
class CustomUserAdmin(AdminPageDescriptionMixin, UserAdmin):
    page_description = (
        "Gestion des comptes utilisateurs : identifiants, rôles, organisation et droits."
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Profil",
            {
                "fields": ("role", "phone_number", "organisation"),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(UserProfile)
class UserProfileAdmin(AdminPageDescriptionMixin, admin.ModelAdmin):
    page_description = (
        "Profils détaillés associés aux utilisateurs avec liens externes et coordonnées."
    )
    list_display = ("user", "linkedin_url", "portfolio_url")
    search_fields = ("user__username", "user__email")

