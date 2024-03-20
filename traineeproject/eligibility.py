from .constants import SCREENING_MIN_AGE


class Eligibility:
    def __init__(self, age_in_years=None, **kwargs):

        self.reason_for_ineligibility = []
        self.age_in_years = age_in_years

        if self.age_in_years < SCREENING_MIN_AGE:
            self.reason_for_ineligibility.append(f'Participant is under {SCREENING_MIN_AGE}')


        self.is_eligible = False if self.reason_for_ineligibility else True

    def __str__(self):
        return f'Screened age {self.age_in_years}'

