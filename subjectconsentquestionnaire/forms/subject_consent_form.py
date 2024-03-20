from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_form_validators import FormValidatorMixin
from edc_consent.modelform_mixins import ConsentModelFormMixin


from ..models import SubjectConsent


class SubjectConsentForm(SiteModelFormMixin,
                         FormValidatorMixin,
                         ConsentModelFormMixin,
                         forms.ModelForm):

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput())

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    class Meta:
        model = SubjectConsent
        fields = '__all__'
