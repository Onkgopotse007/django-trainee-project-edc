from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView, DetailView, UpdateView, CreateView

from educationquestionnaire.models import SubjectEmployment


class SubjectEmploymentCreateView(CreateView):
    model = SubjectEmployment
    fields = '__all__'
    success_url = reverse_lazy('subject_employment_list')


class SubjectEmploymentUpdateView(UpdateView):
    model = SubjectEmployment
    fields = '__all__'
    success_url = reverse_lazy('subject_employment_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class SubjectEmploymentDeleteView(DeleteView):
    model = SubjectEmployment
    success_url = reverse_lazy('subject_employment_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class SubjectEmploymentListView(ListView):
    model = SubjectEmployment


class SubjectEmploymentDetailView(DetailView):
    model = SubjectEmployment
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'
