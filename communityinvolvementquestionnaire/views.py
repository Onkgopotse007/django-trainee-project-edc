from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, ListView, DetailView

from communityinvolvementquestionnaire.models import CommunityInvolvement


class CommunityInvolvementCreateView(CreateView):
    model = CommunityInvolvement
    fields = '__all__'
    success_url = reverse_lazy('community_involvement_list')


class CommunityInvolvementUpdateView(UpdateView):
    model = CommunityInvolvement
    fields = '__all__'
    success_url = reverse_lazy('community_involvement_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class CommunityInvolvementDeleteView(DeleteView):
    model = CommunityInvolvement
    success_url = reverse_lazy('community_involvement_list')
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'


class CommunityInvolvementListView(ListView):
    model = CommunityInvolvement


class CommunityInvolvementDetailView(DetailView):
    model = CommunityInvolvement
    slug_field = 'subject_id'
    slug_url_kwarg = 'subject_id'
