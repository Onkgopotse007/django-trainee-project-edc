from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from subjectconsentquestionnaire.models import SubjectConsent


class SubjectConsentCreateView(CreateView):
    model = SubjectConsent
    fields = '__all__'
    success_url = reverse_lazy('subject_consent_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class SubjectConsentUpdateView(UpdateView):
    model = SubjectConsent
    fields = '__all__'
    success_url = reverse_lazy('subject_consent_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class SubjectConsentDeleteView(DeleteView):
    model = SubjectConsent
    fields = '__all__'
    success_url = reverse_lazy('subject_consent_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class SubjectConsentListView(ListView):
    model = SubjectConsent


class SubjectConsentDetailView(DetailView):
    model = SubjectConsent
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'
