from django.db import models

from enrollmentquestionnaire.models import EnrollmentChecklist
from traineeproject.choices import *


class CommunityInvolvement(models.Model):
    subject_id = models.ForeignKey(EnrollmentChecklist, on_delete=models.CASCADE, verbose_name=f'Subject identifier')
    involvement_rate = models.CharField(
        verbose_name=f'How active are you in community activities such as burial society, Motshelo, Syndicate, PTA, '
                     f'VDC(Village Development Committee), Mophato and development of the community that surrounds you?',
        null=False,
        blank=False,
        choices=COMMUNITY_INVOLVEMENT_CHOICES,
        max_length=150
    )

    previously_voted = models.CharField(
        verbose_name=f'Did you vote in the last local government election?',
        null=False,
        blank=False,
        choices=ELECTION_PARTICIPATION_CHOICES,
        max_length=150
    )

    major_problems = models.CharField(
        verbose_name=f'What are the major problems in this neighborhood?',
        null=False,
        blank=False,
        choices=NEIGHBOURHOOD_PROBLEMS_CHOICES,
        max_length=150
    )

    adults_solving_problems = models.CharField(
        verbose_name=f'If there is a problem in this neighborhood, do the adults work together in solving it?',
        null=False,
        blank=False,
        choices=ADULTS_PROBLEM_SOLVING_CHOICES,
        max_length=150
    )
