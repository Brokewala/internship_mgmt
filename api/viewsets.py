from __future__ import annotations

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from affectations.models import Affectation
from candidatures.models import Candidature
from entreprises.models import Entreprise
from offres.models import OffreStage
from suivis.models import Livrable

from .filters import (
    AffectationFilterSet,
    CandidatureFilterSet,
    LivrableFilterSet,
    OffreStageFilterSet,
)
from .serializers import (
    AffectationSerializer,
    CandidatureSerializer,
    EntrepriseSerializer,
    LivrableSerializer,
    OffreStageSerializer,
)


class BaseManagedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def _user_role(self) -> str | None:
        return getattr(self.request.user, "role", None)

    def _is_responsable(self) -> bool:
        user = self.request.user
        return bool(
            user.is_superuser
            or user.is_staff
            or self._user_role() in {User.Roles.ADMIN, User.Roles.STAFF}
        )

    def _is_supervisor(self) -> bool:
        return self._user_role() == User.Roles.SUPERVISOR

    def _is_student(self) -> bool:
        return self._user_role() == User.Roles.STUDENT

    def _supervisor_filters(self, queryset, prefix: str | None):
        user = self.request.user
        organisation = (getattr(user, "organisation", "") or "").strip()
        email = (getattr(user, "email", "") or "").strip()

        if not organisation and not email:
            return queryset.none()

        filters = Q()
        if prefix is None:
            if organisation:
                filters |= Q(name__iexact=organisation)
            if email:
                filters |= Q(contact_email__iexact=email) | Q(contacts__email__iexact=email)
        else:
            if organisation:
                filters |= Q(**{f"{prefix}name__iexact": organisation})
            if email:
                filters |= Q(**{f"{prefix}contact_email__iexact": email})
                filters |= Q(**{f"{prefix}contacts__email__iexact": email})

        return queryset.filter(filters).distinct()

    # Hooks -----------------------------------------------------------------
    def _ensure_responsable(self) -> None:
        if not self._is_responsable():
            raise PermissionDenied("Action non autorisée pour votre profil.")


class EntrepriseViewSet(BaseManagedModelViewSet):
    serializer_class = EntrepriseSerializer
    queryset = Entreprise.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self._is_responsable():
            return queryset
        if self._is_supervisor():
            return self._supervisor_filters(queryset, prefix=None)
        if self._is_student():
            return queryset.filter(
                Q(affectations__student=user) | Q(offres__applications__student=user)
            ).distinct()
        return queryset.none()

    def perform_create(self, serializer):
        self._ensure_responsable()
        serializer.save()

    def perform_update(self, serializer):
        self._ensure_responsable()
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_responsable()
        instance.delete()


class OffreStageViewSet(BaseManagedModelViewSet):
    serializer_class = OffreStageSerializer
    queryset = OffreStage.objects.select_related("entreprise", "campagne")
    filterset_class = OffreStageFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self._is_responsable():
            return queryset
        if self._is_supervisor():
            return self._supervisor_filters(queryset, prefix="entreprise__")
        if self._is_student():
            return queryset.filter(
                Q(applications__student=user) | Q(affectations__student=user)
            ).distinct()
        return queryset.none()

    def perform_create(self, serializer):
        self._ensure_responsable()
        serializer.save()

    def perform_update(self, serializer):
        if not (self._is_responsable() or self._is_supervisor()):
            raise PermissionDenied("Action non autorisée pour votre profil.")
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_responsable()
        instance.delete()


class CandidatureViewSet(BaseManagedModelViewSet):
    serializer_class = CandidatureSerializer
    queryset = Candidature.objects.select_related("student", "offer", "offer__entreprise")
    filterset_class = CandidatureFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self._is_responsable():
            return queryset
        if self._is_supervisor():
            return self._supervisor_filters(queryset, prefix="offer__entreprise__")
        if self._is_student():
            return queryset.filter(student=user)
        return queryset.none()

    def perform_create(self, serializer):
        if self._is_student():
            serializer.save(student=self.request.user)
            return
        if self._is_responsable() or self._is_supervisor():
            serializer.save()
            return
        raise PermissionDenied("Action non autorisée pour votre profil.")

    def perform_update(self, serializer):
        if self._is_student():
            if "status" in serializer.validated_data:
                raise PermissionDenied("Modification de statut non autorisée pour l'étudiant.")
            serializer.save()
            return
        if self._is_responsable() or self._is_supervisor():
            serializer.save()
            return
        raise PermissionDenied("Action non autorisée pour votre profil.")

    def perform_destroy(self, instance):
        if self._is_student() and instance.student == self.request.user:
            instance.delete()
            return
        if self._is_responsable() or self._is_supervisor():
            instance.delete()
            return
        raise PermissionDenied("Action non autorisée pour votre profil.")


class AffectationViewSet(BaseManagedModelViewSet):
    serializer_class = AffectationSerializer
    queryset = Affectation.objects.select_related("student", "offer", "entreprise")
    filterset_class = AffectationFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self._is_responsable():
            return queryset
        if self._is_supervisor():
            return self._supervisor_filters(queryset, prefix="entreprise__")
        if self._is_student():
            return queryset.filter(student=user)
        return queryset.none()

    def perform_create(self, serializer):
        self._ensure_responsable()
        serializer.save()

    def perform_update(self, serializer):
        if not (self._is_responsable() or self._is_supervisor()):
            raise PermissionDenied("Action non autorisée pour votre profil.")
        serializer.save()

    def perform_destroy(self, instance):
        self._ensure_responsable()
        instance.delete()


class LivrableViewSet(BaseManagedModelViewSet):
    serializer_class = LivrableSerializer
    queryset = Livrable.objects.select_related("affectation", "affectation__student", "affectation__entreprise")
    filterset_class = LivrableFilterSet

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if self._is_responsable():
            return queryset
        if self._is_supervisor():
            return self._supervisor_filters(queryset, prefix="affectation__entreprise__")
        if self._is_student():
            return queryset.filter(affectation__student=user)
        return queryset.none()

    def _ensure_student_affectation(self, serializer):
        affectation = serializer.validated_data.get("affectation")
        if affectation and affectation.student != self.request.user:
            raise PermissionDenied("Affectation non autorisée pour cet utilisateur.")

    def perform_create(self, serializer):
        if self._is_student():
            self._ensure_student_affectation(serializer)
            serializer.save()
            return
        if self._is_responsable() or self._is_supervisor():
            serializer.save()
            return
        raise PermissionDenied("Action non autorisée pour votre profil.")

    def perform_update(self, serializer):
        if self._is_student():
            self._ensure_student_affectation(serializer)
            serializer.save()
            return
        if self._is_responsable() or self._is_supervisor():
            serializer.save()
            return
        raise PermissionDenied("Action non autorisée pour votre profil.")

    def perform_destroy(self, instance):
        if self._is_student():
            if instance.affectation.student != self.request.user:
                raise PermissionDenied("Action non autorisée pour votre profil.")
            instance.delete()
            return
        if self._is_responsable() or self._is_supervisor():
            instance.delete()
            return
        raise PermissionDenied("Action non autorisée pour votre profil.")
