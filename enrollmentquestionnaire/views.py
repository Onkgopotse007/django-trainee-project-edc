from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from enrollmentquestionnaire.models import EnrollmentChecklist


class EnrollmentChecklistCreateView(CreateView):
    model = EnrollmentChecklist
    fields = '__all__'
    success_url = reverse_lazy('enrollment_checklist_list')


class EnrollmentChecklistUpdateView(UpdateView):
    model = EnrollmentChecklist
    fields = '__all__'
    success_url = reverse_lazy('enrollment_checklist_list')


class EnrollmentChecklistDeleteView(DeleteView):
    model = EnrollmentChecklist
    success_url = reverse_lazy('enrollment_checklist_list')


class EnrollmentChecklistListView(ListView):
    model = EnrollmentChecklist


class EnrollmentChecklistDetailView(DetailView):
    model = EnrollmentChecklist
