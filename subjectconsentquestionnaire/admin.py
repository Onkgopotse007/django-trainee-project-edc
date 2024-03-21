from collections import OrderedDict

from django.contrib import admin
from django.contrib.admin import site
from django.urls import reverse, NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_consent.actions import flag_as_verified_against_paper, \
    unflag_as_verified_against_paper
from edc_model_admin import ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin, \
    ModelAdminReplaceLabelTextMixin, ModelAdminInstitutionMixin, ModelAdminReadOnlyMixin, \
    ModelAdminFormInstructionsMixin, ModelAdminAuditFieldsMixin, \
    ModelAdminNextUrlRedirectError, ModelAdminBasicMixin, audit_fields, \
    audit_fieldset_tuple
from simple_history.admin import SimpleHistoryAdmin

from subjectconsentquestionnaire.forms.subject_consent_form import SubjectConsentForm
from subjectconsentquestionnaire.models import SubjectConsent
from traineeproject.admin_site import traineeproject_admin
from traineeproject.modeladmin_mixins import VersionControlMixin


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormAutoNumberMixin,
                      ModelAdminRevisionMixin, ModelAdminReplaceLabelTextMixin,
                      ModelAdminInstitutionMixin, ModelAdminReadOnlyMixin,
                      VersionControlMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminAuditFieldsMixin
                      ):
    def redirect_url(self, request, obj, post_url_continue=None):
        redirect_url = super().redirect_url(
            request, obj, post_url_continue=post_url_continue)
        if request.GET.dict().get('next'):
            url_name = request.GET.dict().get('next').split(',')[0]
            attrs = request.GET.dict().get('next').split(',')[1:]
            options = {k: request.GET.dict().get(k)
                       for k in attrs if request.GET.dict().get(k)}
            try:
                redirect_url = reverse(url_name, kwargs=options)
            except NoReverseMatch as e:
                raise ModelAdminNextUrlRedirectError(
                    f'{e}. Got url_name={url_name}, kwargs={options}.')
        return redirect_url


@admin.register(SubjectConsent, site=site)
class SubjectConsentAdmin(ModelAdminBasicMixin, ModelAdminMixin,
                          SimpleHistoryAdmin,
                          admin.ModelAdmin):
    form = SubjectConsentForm
    fieldsets = (
        (None, {
            'fields': (
                'screening_identifier',
                'subject_identifier',
                'consent_datetime',
                'first_name',
                'last_name',
                'initials',
                'gender',
                'dob',
                'identity',
                'confirm_identity',
                'identity_type',
                'has_understood_purpose_of_the_study',
                'has_understood_risks',
                'has_understood_potential_benefits',
                'marital_status',
                'currently_live_with',
                'number_of_wives',
            ),
        }), audit_fieldset_tuple
    )

    radio_fields = {
        'gender': admin.VERTICAL,
        'is_dob_estimated': admin.VERTICAL,
        'identity_type': admin.VERTICAL,
        'has_understood_purpose_of_the_study': admin.HORIZONTAL,
        'has_understood_risks': admin.HORIZONTAL,
        'has_understood_potential_benefits': admin.HORIZONTAL,
        'marital_status': admin.HORIZONTAL,
        'currently_live_with': admin.HORIZONTAL,
        # 'consent_to_participate': admin.VERTICAL,
        # 'consent_to_optional_sample_collection': admin.VERTICAL,
    }

    list_display = ('subject_identifier',
                    'verified_by',
                    'is_verified',
                    'is_verified_datetime',
                    'first_name',
                    'initials',
                    'gender',
                    'dob',
                    'consent_datetime',
                    'created',
                    'modified',
                    'user_created',
                    'user_modified')

    search_fields = ('subject_identifier', 'dob')
    readonly_fields = ('subject_identifier',)

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj=obj) + audit_fields
