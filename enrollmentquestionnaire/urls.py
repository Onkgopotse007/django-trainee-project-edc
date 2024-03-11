from django.urls import path
from .views import EnrollmentChecklistCreateView, EnrollmentChecklistUpdateView, EnrollmentChecklistDeleteView, EnrollmentChecklistListView, EnrollmentChecklistDetailView

app_name = 'enrollment'

urlpatterns = [
    path('create/', EnrollmentChecklistCreateView.as_view(), name='enrollment_create'),
    path('<str:subject_id>/update/', EnrollmentChecklistUpdateView.as_view(), name='enrollment_update'),
    path('<str:subject_id>/delete/', EnrollmentChecklistDeleteView.as_view(), name='enrollment_delete'),
    path('<str:subject_id>/', EnrollmentChecklistDetailView.as_view(), name='enrollment_detail'),
    path('', EnrollmentChecklistListView.as_view(), name='enrollment_list'),
]
