from django.urls import path

from .views import SubjectConsentCreateView, SubjectConsentUpdateView, \
    SubjectConsentDeleteView, SubjectConsentDetailView, SubjectConsentListView

app_name = 'subject_consent'

urlpatterns = [
    path('create/', SubjectConsentCreateView.as_view(), name='subject_consent_create'),
    path('<str:subject_id>/update/', SubjectConsentUpdateView.as_view(), name='subject_consent_update'),
    path('<str:subject_id>/delete/', SubjectConsentDeleteView.as_view(), name='subject_consent_delete'),
    path('<str:subject_id>/', SubjectConsentDetailView.as_view(), name='subject_consent_detail'),
    path('', SubjectConsentListView.as_view(), name='subject_consent_list'),
]