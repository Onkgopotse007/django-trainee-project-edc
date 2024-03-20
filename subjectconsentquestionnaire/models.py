from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_consent.field_mixins import SampleCollectionFieldsMixin, IdentityFieldsMixin, \
    ReviewFieldsMixin, \
    PersonalFieldsMixin, CitizenFieldsMixin
from edc_consent.model_mixins import ConsentModelMixin
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierModelMixin
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_visit_schedule import site_visit_schedules

from enrollmentquestionnaire.models import EnrollmentChecklist
from traineeproject.models import onschedule
from traineeproject.models.model_mixins.search_slug_model_mixin import \
    SearchSlugModelMixin
from traineeproject.models.onschedule import OnSchedule
from traineeproject.subject_identifier import SubjectIdentifier
from traineeproject.choices import GENDER_CHOICES, MARITAL_CHOICES, HOUSE_MATE_CHOICES, \
    IDENTITY_TYPE, YES_NO_BOOLEAN_CHOICES, CONSENT_INVALID
from edc_consent.managers import ConsentManager as SubjectConsentManager
from edc_search.model_mixins import SearchSlugManager
from edc_base.model_managers import HistoricalRecords
from django.apps import apps as django_apps


class ConsentManager(SubjectConsentManager, SearchSlugManager):
    def get_by_natural(self, subject_identifier, version):
        return self.get(
            subject_identifier=subject_identifier, version=version)

    class Meta:
        abstract = True


class SubjectConsent(ConsentModelMixin, SiteModelMixin, SampleCollectionFieldsMixin,
                     UpdatesOrCreatesRegistrationModelMixin,
                     NonUniqueSubjectIdentifierModelMixin,
                     IdentityFieldsMixin, ReviewFieldsMixin, PersonalFieldsMixin,
                     CitizenFieldsMixin, SearchSlugModelMixin, BaseUuidModel):
    subject_screening_model = 'enrollmentquestionnaire.EnrollmentChecklist'

    identity_type = models.CharField(
        verbose_name='What type of identity number is this?',
        max_length=25,
        choices=IDENTITY_TYPE)

    screening_identifier = models.CharField(
        verbose_name='Screening identifier',
        max_length=50)
    gender = models.CharField(
        verbose_name=f'Gender',
        choices=GENDER_CHOICES,
        max_length=150
    )
    has_understood_purpose_of_the_study = models.BooleanField(
        verbose_name=f'Subject has understood purpose of the study',
        choices=YES_NO_BOOLEAN_CHOICES,
        max_length=150,
        help_text=CONSENT_INVALID
    )
    has_understood_risks = models.BooleanField(
        verbose_name=f'Subject ha understood the risks of participating in this study',
        choices=YES_NO_BOOLEAN_CHOICES,
        max_length=150,
        help_text=CONSENT_INVALID
    )
    has_understood_potential_benefits = models.BooleanField(
        verbose_name=f'Subject has understood potential benefits of participating in the study',
        choices=YES_NO_BOOLEAN_CHOICES,
        max_length=150,
        help_text=CONSENT_INVALID
    )
    marital_status = models.CharField(
        verbose_name=f'Subject\'s marital status',
        choices=MARITAL_CHOICES,
        max_length=150
    )
    number_of_wives = models.PositiveIntegerField(
        verbose_name=f'Number of Wives',
    )

    currently_live_with = models.CharField(
        verbose_name=f'Who do you currently live with',
        choices=HOUSE_MATE_CHOICES,
        max_length=150
    )

    eligible = models.BooleanField(
        default=False,
        choices=YES_NO_BOOLEAN_CHOICES,
        editable=False)

    objects = SubjectConsentManager()

    consent = ConsentManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.subject_identifier}  V{self.version}'

    def natural_key(self):
        return (self.subject_identifier, self.version,)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.extend(['identity', 'screening_identifier',
                       'first_name', 'last_name'])
        return fields

    def save(self, *args, **kwargs):
        self.version = '1'
        super().save(*args, **kwargs)

    def make_new_identifier(self):
        """Returns a new and unique identifier.
        Override this if needed. Can be inherited from NonUniqueSubjectIdentifierModelMixin
        """
        subject_identifier = SubjectIdentifier(
            identifier_type='subject',
            requesting_model=self._meta.label_lower,
            site=self.site)
        return subject_identifier.identifier

    @property
    def consent_version(self):
        return self.version

    class Meta(ConsentModelMixin.Meta):
        app_label = 'subjectconsentquestionnaire'
        verbose_name = 'Participation Consent'
        verbose_name_plural = 'Participation Consent'
        unique_together = (('subject_identifier', 'version'),
                           ('screening_identifier', 'version'),
                           ('subject_identifier', 'screening_identifier', 'version'),
                           ('first_name', 'dob', 'initials', 'version'))


def update_model_fields(instance=None, model_cls=None, fields=None):
    try:
        model_obj = model_cls.objects.get(
            screening_identifier=instance.screening_identifier)
    except model_cls.DoesNotExist:
        raise ValidationError(f'{model_cls} object does not exist!')
    else:
        for field, value in fields:
            setattr(model_obj, field, value)
        model_obj.save_base(update_fields=[field[0] for field in fields])


@receiver(post_save, weak=False, sender=SubjectConsent,
          dispatch_uid='subject_screening_on_post_save')
def subject_screening_on_post_save(sender, instance, raw, created, **kwargs):
    """Creates an onschedule instance for this enrolled subject, if
    it does not exist.
    """
    if instance.eligible:
        if not raw:
            if not created:
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=OnSchedule,
                    name=instance.schedule_name)
                schedule.refresh_schedule(
                    subject_identifier=instance.subject_identifier)
            else:
                # put subject on schedule
                _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
                    onschedule_model=OnSchedule,
                    name=instance.schedule_name)
                schedule.put_on_schedule(
                    subject_identifier=instance.subject_identifier,
                    onschedule_datetime=instance.report_datetime)

                # Update subject consent with screening identifier
                try:
                    subject_consent = SubjectConsent.objects.get(
                        subject_identifier=instance.subject_identifier)
                except SubjectConsent.DoesNotExist:
                    raise ValidationError(
                        'Subject Consent for subject '
                        f'{instance.subject_identifier} must exist.')
                else:
                    subject_consent.screening_identifier = instance.screening_identifier
                    subject_consent.save()
