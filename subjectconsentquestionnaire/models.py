from django.db import models

from enrollmentquestionnaire.models import EnrollmentChecklist
from traineeproject.choices import GENDER_CHOICES, MARITAL_CHOICES, HOUSE_MATE_CHOICES


class SubjectConsent( models.Model):
    subject_id = models.ForeignKey(EnrollmentChecklist, on_delete=models.CASCADE, verbose_name=f'Subject identifier')
    gender = models.CharField(
        verbose_name=f'Gender',
        choices=GENDER_CHOICES,
        max_length=150
    )
    has_understood_purpose_of_the_study = models.BooleanField(
        verbose_name=f'Subject has understood purpose of the study',
        max_length=150
    )
    has_understood_risks = models.BooleanField(
        verbose_name=f'Subject ha understood the risks of participating in this study',
        max_length=150
    )
    has_understood_potential_benefits = models.BooleanField(
        verbose_name=f'Subject has understood potential benefits of participating in the study',
        max_length=150
    )
    marital_status = models.CharField(
        verbose_name=f'Subject\'s marital status',
        choices=MARITAL_CHOICES,
        max_length=150
    )
    number_of_wives = models.IntegerField(
        verbose_name=f'',
    )

    currently_live_with = models.CharField(
        verbose_name=f'Who do you currently live with',
        choices=HOUSE_MATE_CHOICES,
        max_length=150
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.gender == 'MALE':
            self._meta.get_field(
                'number_of_wives').verbose_name = 'Number of wives you have including traditionally married'
        elif self.gender == 'FEMALE':
            self._meta.get_field(
                'number_of_wives').verbose_name = ('Number of wives your husband has including traditionally married '
                                                   'and yourself?')
