from django.core.exceptions import ValidationError
from django.db import models

from traineeproject.choices import GENDER_CHOICES


class EnrollmentChecklist(models.Model):
    subject_id = models.CharField(max_length=150, primary_key=True, verbose_name='Subject identifier')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name=f'Gender')
    is_botswana_citizen = models.BooleanField(default=False, verbose_name=f'Are you a Botswana citizen?', max_length=150)
    is_married_to_botswana_citizen = models.BooleanField(default=False, verbose_name=f'If not a citizen, are you '
                                                                                     f'legally married to a Botswana '
                                                                                     f'Citizen?',  blank=True, null=True, max_length=150)
    has_marriage_certificate = models.BooleanField(default=False, verbose_name=f'Has the participant produced the '
                                                                               f'marriage certificate, as proof?', blank=True, null=True,max_length=150)
    is_literate = models.BooleanField(default=False, verbose_name=f'Is the participant LITERATE?')
    has_literate_witness = models.BooleanField(default=False, verbose_name= f'If ILLITERATE, is there a LITERATE '
                                                                            f'witness available? ', blank=True, null=True, max_length=150)
    is_minor = models.BooleanField(default=False, verbose_name=f'Is the participant a minor?')
    guardian_available = models.BooleanField(default=False, verbose_name=f'If the participant is a minor, is their '
                                                                         f'guardian available',  blank=True, null=True, max_length=150)

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

