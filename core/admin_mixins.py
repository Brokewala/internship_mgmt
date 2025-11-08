from __future__ import annotations

import json
from typing import Any, Iterable

from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.utils.translation import gettext_lazy as _

from .models import AuditLog


class AuditLogAdminMixin:
    """Mixin to persist admin changes in :class:`core.models.AuditLog`."""

    audit_log_fields: Iterable[str] | None = None
    audit_log_model_label: str | None = None

    def _serialize_for_audit(self, obj: Any) -> dict[str, Any] | None:
        if obj is None:
            return None
        fields = tuple(self.audit_log_fields) if self.audit_log_fields else None
        data = model_to_dict(obj, fields=fields)
        data["id"] = obj.pk
        return json.loads(json.dumps(data, cls=DjangoJSONEncoder))

    def _log_audit_event(
        self,
        request,
        *,
        action: str,
        obj=None,
        before: dict[str, Any] | None = None,
        after: dict[str, Any] | None = None,
        object_id: Any | None = None,
        object_repr: str | None = None,
    ) -> None:
        metadata = {
            "model": obj._meta.label if obj else self.audit_log_model_label,
            "object_id": object_id if object_id is not None else getattr(obj, "pk", None),
            "object_repr": object_repr if object_repr is not None and object_repr != "" else str(obj) if obj else None,
            "before": before,
            "after": after,
        }
        AuditLog.objects.create(
            action=action,
            actor=request.user if request.user.is_authenticated else None,
            description=object_repr or str(obj) if obj else "",
            metadata=metadata,
        )

    def _get_audit_action_label(self, obj, change: bool) -> str:
        label = self.audit_log_model_label or obj._meta.verbose_name.title()
        if change:
            return _("Modification %s") % label
        return _("Création %s") % label

    def save_model(self, request, obj, form, change):
        before = None
        if change and obj.pk:
            try:
                original = self.model.objects.get(pk=obj.pk)
            except self.model.DoesNotExist:  # pragma: no cover - defensive
                original = None
            if original:
                before = self._serialize_for_audit(original)
        super().save_model(request, obj, form, change)
        after = self._serialize_for_audit(obj)
        action = self._get_audit_action_label(obj, change)
        self._log_audit_event(
            request,
            action=action,
            obj=obj,
            before=before,
            after=after,
        )

    def delete_model(self, request, obj):
        before = self._serialize_for_audit(obj)
        object_id = obj.pk
        object_repr = str(obj)
        super().delete_model(request, obj)
        label = self.audit_log_model_label or obj._meta.verbose_name.title()
        action = _("Suppression %s") % label
        self._log_audit_event(
            request,
            action=action,
            obj=obj,
            before=before,
            after=None,
            object_id=object_id,
            object_repr=object_repr,
        )

    def delete_queryset(self, request, queryset):
        serialized = [
            (
                obj.pk,
                str(obj),
                self._serialize_for_audit(obj),
            )
            for obj in queryset
        ]
        super().delete_queryset(request, queryset)
        label = self.audit_log_model_label or queryset.model._meta.verbose_name_plural.title()
        action_label = _("Suppression %s") % label
        for object_id, object_repr, before in serialized:
            self._log_audit_event(
                request,
                action=action_label,
                obj=queryset.model,
                before=before,
                after=None,
                object_id=object_id,
                object_repr=object_repr,
            )
