from django.urls import path

from communityinvolvementquestionnaire.views import CommunityInvolvementCreateView, CommunityInvolvementUpdateView, \
    CommunityInvolvementDeleteView, CommunityInvolvementDetailView, CommunityInvolvementListView

app_name = 'community_involvement'
urlpatterns = [
    path('create/', CommunityInvolvementCreateView.as_view(), name='community_involvement_create'),
    path('<str:subject_id>/update/', CommunityInvolvementUpdateView.as_view(), name='community_involvement_update'),
    path('<str:subject_id>/delete/', CommunityInvolvementDeleteView.as_view(), name='community_involvement_delete'),
    path('<str:subject_id>/', CommunityInvolvementDetailView.as_view(), name='community_involvement_detail'),
    path('', CommunityInvolvementListView.as_view(), name='community_involvement_list')
]
