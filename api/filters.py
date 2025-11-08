from __future__ import annotations

import django_filters

from affectations.models import Affectation
from candidatures.models import Candidature
from entreprises.models import Entreprise
from offres.models import Campagne, OffreStage
from suivis.models import Livrable


class OffreStageFilterSet(django_filters.FilterSet):
    campagne = django_filters.ModelChoiceFilter(queryset=Campagne.objects.all())
    entreprise = django_filters.ModelChoiceFilter(queryset=Entreprise.objects.all())
    status = django_filters.ChoiceFilter(choices=OffreStage.Status.choices)

    class Meta:
        model = OffreStage
        fields = ["campagne", "entreprise", "status"]


class CandidatureFilterSet(django_filters.FilterSet):
    campagne = django_filters.ModelChoiceFilter(
        field_name="offer__campagne", queryset=Campagne.objects.all()
    )
    entreprise = django_filters.ModelChoiceFilter(
        field_name="offer__entreprise", queryset=Entreprise.objects.all()
    )
    status = django_filters.ChoiceFilter(choices=Candidature.Status.choices)

    class Meta:
        model = Candidature
        fields = ["campagne", "entreprise", "status"]


class AffectationFilterSet(django_filters.FilterSet):
    campagne = django_filters.ModelChoiceFilter(
        field_name="offer__campagne", queryset=Campagne.objects.all()
    )
    entreprise = django_filters.ModelChoiceFilter(queryset=Entreprise.objects.all())
    status = django_filters.ChoiceFilter(choices=Affectation.Status.choices)

    class Meta:
        model = Affectation
        fields = ["campagne", "entreprise", "status"]


class LivrableFilterSet(django_filters.FilterSet):
    campagne = django_filters.ModelChoiceFilter(
        field_name="affectation__offer__campagne", queryset=Campagne.objects.all()
    )
    entreprise = django_filters.ModelChoiceFilter(
        field_name="affectation__entreprise", queryset=Entreprise.objects.all()
    )
    status = django_filters.ChoiceFilter(choices=Livrable.Status.choices)

    class Meta:
        model = Livrable
        fields = ["campagne", "entreprise", "status"]
