from __future__ import annotations

from rest_framework import serializers

from affectations.models import Affectation
from candidatures.models import Candidature
from entreprises.models import Entreprise
from offres.models import OffreStage
from suivis.models import Livrable


class TimeStampedModelSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class EntrepriseSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Entreprise
        fields = (
            "id",
            "name",
            "description",
            "address",
            "website",
            "contact_email",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class OffreStageSerializer(TimeStampedModelSerializer):
    class Meta:
        model = OffreStage
        fields = (
            "id",
            "entreprise",
            "campagne",
            "title",
            "description",
            "location",
            "start_date",
            "end_date",
            "slots",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class CandidatureSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Candidature
        fields = (
            "id",
            "student",
            "offer",
            "status",
            "motivation",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "student", "created_at", "updated_at")
        extra_kwargs = {
            "offer": {"required": True},
        }


class AffectationSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Affectation
        fields = (
            "id",
            "student",
            "offer",
            "entreprise",
            "start_date",
            "end_date",
            "status",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "student": {"required": False},
            "entreprise": {"required": True},
        }


class LivrableSerializer(TimeStampedModelSerializer):
    class Meta:
        model = Livrable
        fields = (
            "id",
            "affectation",
            "type",
            "title",
            "description",
            "due_date",
            "submitted_at",
            "status",
            "score",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
        extra_kwargs = {
            "affectation": {"required": True},
        }
