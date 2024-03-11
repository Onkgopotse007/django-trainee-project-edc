from django.urls import path

from educationquestionnaire.views import SubjectEmploymentCreateView, SubjectEmploymentUpdateView, \
    SubjectEmploymentDeleteView, SubjectEmploymentDetailView, SubjectEmploymentListView

app_name = 'education'

urlpatterns = [
    path('create/', SubjectEmploymentCreateView.as_view(), name='subject_employment_create'),
    path('<str:subject_id>/update/', SubjectEmploymentUpdateView.as_view(), name='subject_employment_update'),
    path('<str:subject_id>/delete/', SubjectEmploymentDeleteView.as_view(), name='subject_employment_delete'),
    path('<str:subject_id>/', SubjectEmploymentDetailView.as_view(), name='subject_employment_detail'),
    path('', SubjectEmploymentListView.as_view(), name='subject_employment_list')
]
