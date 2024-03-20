from django.apps import apps as django_apps
from django.utils.safestring import mark_safe


class VersionControlMixin:

    def get_form_version(self, request):
        print(request)
        form_versions = django_apps.get_app_config('traineeproject').form_versions
        print('Here')
        queryset = self.get_queryset(request)
        model_name = queryset.model._meta.label_lower
        form_version = form_versions.get(model_name)

        return mark_safe(
            f' Version: {form_version} ')

    def get_timepoint(self, request):

        appt_model = django_apps.get_model('edc_appointment.appointment')

        try:
            app_obj = appt_model.objects.get(id=request.GET.get('appointment'))
        except appt_model.DoesNotExist:
            pass
        else:
            return mark_safe(
                f'Timepoint: <i>{app_obj.visits.get(app_obj.visit_code).title} '
                '</i> &emsp; ')
