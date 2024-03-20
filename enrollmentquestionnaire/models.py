from django.core.exceptions import ValidationError
from django.db import models
from edc_base import get_utcnow
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager
from traineeproject.choices import GENDER_CHOICES
from traineeproject.eligibility import Eligibility
from traineeproject.identifiers import ScreeningIdentifier
from traineeproject.models.model_mixins.search_slug_model_mixin import SearchSlugModelMixin


class ScreeningEligibilityManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class EnrollmentChecklist(NonUniqueSubjectIdentifierFieldMixin,
                          SiteModelMixin,
                          SearchSlugModelMixin, BaseUuidModel):
    identifier_cls = ScreeningIdentifier

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        help_text='Date and time of report.')

    screening_identifier = models.CharField(
        editable=False,
        verbose_name='Eligibility Identifier',
        max_length=36,
        blank=True,
        unique=True, )

    age_in_years = models.PositiveIntegerField(
        verbose_name='Age',
        help_text='Age in years.')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              verbose_name=f'Gender')
    is_botswana_citizen = models.BooleanField(default=False, verbose_name=f'Are you a '
                                                                          f'Botswana '
                                                                          f'citizen?',
                                              max_length=150)
    is_married_to_botswana_citizen = models.BooleanField(default=False,
                                                         verbose_name=f'If not a citizen, are you'
                                                                      f'legally married to a Botswana'
                                                                      f'Citizen?',
                                                         blank=True, null=True,
                                                         max_length=150)
    has_marriage_certificate = models.BooleanField(default=False,
                                                   verbose_name=f'Has the participant produced the '
                                                                f'marriage certificate, as proof?',
                                                   blank=True, null=True, max_length=150)
    is_literate = models.BooleanField(default=False,
                                      verbose_name=f'Is the participant LITERATE?')
    has_literate_witness = models.BooleanField(default=False,
                                               verbose_name=f'If ILLITERATE, is there a LITERATE '
                                                            f'witness available? ',
                                               blank=True,
                                               null=True, max_length=150)
    is_minor = models.BooleanField(default=False,
                                   verbose_name=f'Is the participant a minor?')
    guardian_available = models.BooleanField(default=False,
                                             verbose_name=f'If the participant is a minor, is their '
                                                          f'guardian available',
                                             blank=True, null=True,
                                             max_length=150)
    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    reason_for_ineligibility = models.TextField(
        max_length=150,
        verbose_name="Reason for ineligibility",
        null=True,
        editable=False)

    is_consented = models.BooleanField(
        default=False,
        editable=False)

    objects = ScreeningEligibilityManager()

    def __str__(self):
        return f'{self.screening_identifier}'

    def natural_key(self):
        return (self.screening_identifier,)

    natural_key.dependencies = ['sites.Site']

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        return fields

    def save(self, *args, **kwargs):
        eligibility_criteria = Eligibility(self.age_in_years)

        self.is_eligible = eligibility_criteria.is_eligible
        self.reason_for_ineligibility = eligibility_criteria.reason_for_ineligibility

        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'enrollmentquestionnaire'
        verbose_name = 'Screening Eligibility'
        verbose_name_plural = 'Screening Eligibility'


    def clean(self):
        if not self.is_botswana_citizen and self.is_married_to_botswana_citizen is None:
            raise ValidationError(
                'If you are not a Botswana citizen, you must specify if you are married to a Botswana citizen.')
        if self.is_married_to_botswana_citizen and self.has_marriage_certificate is None:
            raise ValidationError(
                f'If married to a Botswana, you must specify if participant has produced a marriage certificate as proof'
            )
        if not self.is_literate and self.has_literate_witness is None:
            raise ValidationError(
                f'If Participant is not literate, you must specify if participant has a literate representative'
            )
        if self.is_minor and self.guardian_available is None:
            raise ValidationError(
                f'If participant is a minor you must specify if the guardian is available'
            )

        super().clean()
