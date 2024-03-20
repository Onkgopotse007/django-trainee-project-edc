from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from datetime import datetime
from dateutil.tz import gettz
from edc_visit_tracking.constants import (SCHEDULED, UNSCHEDULED, LOST_VISIT,
                                          MISSED_VISIT, COMPLETED_PROTOCOL_VISIT)
from edc_constants.constants import FAILED_ELIGIBILITY


class AppConfig(DjangoAppConfig):
    app_label = 'traineeproject'
    name = 'traineeproject'
    verbose_name = 'Trainee Subject CRFs'
    admin_site_name = 'traineeproject_admin'

    form_versions = {
        'traineeproject.subjectvisit': 1.0,
        'traineeproject.subjectrequisition': 1.0,
        'traineeproject.subjectpersonalcontractinfo': 1.0,
        'traineeproject.subjecteducation': 1.0,
        'traineeproject.subjectdemographic': 1.0,
        'traineeproject.subjectcommunityengagement': 1.0,
        'traineeproject.screeningeligibility': 1.0,
        'traineeproject.subjectconsent': 1.0,
    }


if settings.APP_NAME == 'traineeproject':
    from edc_appointment.appointment_config import AppointmentConfig
    from edc_appointment.apps import AppConfig as BaseEdcAppointmentAppConfig
    from edc_appointment.constants import COMPLETE_APPT
    from edc_metadata.apps import AppConfig as BaseEdcMetadataAppConfig
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig
    from edc_timepoint.apps import AppConfig as BaseEdcTimepointAppConfig
    from edc_timepoint.timepoint import Timepoint
    from edc_timepoint.timepoint_collection import TimepointCollection
    from edc_visit_tracking.apps import AppConfig as BaseEdcVisitTrackingAppConfig
    from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
    from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU


    def ready(self):
        from subjectconsentquestionnaire.models import subject_consent_on_post_save


    class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
        country = 'botswana'
        definitions = {
            '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                                 slots=[100, 100, 100, 100, 100, 100, 100]),
            '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                                 slots=[100, 100, 100, 100, 100])}


    class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
        protocol = 'AZD100'
        protocol_number = '150'
        protocol_name = 'Trainee Project'
        protocol_title = ''
        study_open_datetime = datetime(
            2016, 4, 1, 0, 0, 0, tzinfo=gettz('UTC'))
        study_close_datetime = datetime(
            2025, 12, 1, 0, 0, 0, tzinfo=gettz('UTC'))


    class EdcAppointmentAppConfig(BaseEdcAppointmentAppConfig):
        configurations = [
            AppointmentConfig(
                model='edc_appointment.appointment',
                related_visit_model='traineeproject_subject.subjectvisit',
                appt_type='clinic'),
        ]


    class EdcTimepointAppConfig(BaseEdcTimepointAppConfig):
        timepoints = TimepointCollection(
            timepoints=[
                Timepoint(
                    model='edc_appointment.appointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT),
                Timepoint(
                    model='edc_appointment.historicalappointment',
                    datetime_field='appt_datetime',
                    status_field='appt_status',
                    closed_status=COMPLETE_APPT)
            ])


    class EdcVisitTrackingAppConfig(BaseEdcVisitTrackingAppConfig):
        # report_datetime_allowance = -1
        visit_models = {
            'traineeproject_subject': (
                'subject_visit', 'traineeproject_subject.subjectvisit')}


    class EdcMetadataAppConfig(BaseEdcMetadataAppConfig):
        reason_field = {'traineeproject_subject.subjectvisit': 'reason'}
        create_on_reasons = [SCHEDULED, UNSCHEDULED, COMPLETED_PROTOCOL_VISIT]
        delete_on_reasons = [LOST_VISIT, MISSED_VISIT, FAILED_ELIGIBILITY]
