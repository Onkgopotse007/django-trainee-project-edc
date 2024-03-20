from django.core.exceptions import ValidationError
from django.db import models

from enrollmentquestionnaire.models import EnrollmentChecklist
from traineeproject.choices import *


class SubjectEmployment(models.Model):
    is_working = models.BooleanField(
        verbose_name=f'Are you currently working?',
        null=False,
        blank=False
    )
    work_type = models.CharField(
        verbose_name=f'In your main job what type of work do you do?',
        choices=EMPLOYMENT_INDUSTRY_CHOICES,
        null=True,
        blank=True, max_length=150
    )
    occupation = models.CharField(
        verbose_name=f'Describe the work that you do or did in your most recent job. If you have more than one '
                     f'profession, choose the one you spend the most time doing. ',
        choices=EMPLOYMENT_CHOICES,
        null=True,
        blank=True, max_length=150
    )
    income = models.CharField(
        verbose_name=f'In the past month, how much money did you earn from work you did or received in payment?',
        choices=MONTHLY_INCOME_CHOICES,
        null=True,
        blank=True, max_length=150
    )

    def clean(self):
        if self.is_working:
            if self.work_type is None or self.occupation is None or self.work_type is None:
                raise ValidationError(
                    'Fill in all fields if currently working'
                )