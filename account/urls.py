from django.urls import path

from account import views

app_name = 'account'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('update/', views.update_profile_view, name='update-profile'),
    path('profile/detail/<slug:slug>/', views.ProfileDetailView.as_view(), name='detail-profile'),

    path('invitations/received/', views.invitations_received_view, name='invitation-received-profile'),
    path('invitations/forward/', views.invitations_forward_view, name='invitation-forward-profile'),
    path('invitations/accept/', views.accept_invitation, name='invitation-accept'),
    path('invitations/reject/', views.reject_invitation, name='invitation-reject'),

    path('profiles/', views.ProfileListExcludeMeView.as_view(), name='profiles'),
    path('invitation/send/', views.send_invitation, name='invitation-send'),
    path('invitation/remove/', views.remove_from_friends, name='invitation-remove'),

    path('invitation/profiles/', views.invitation_profile_list_exclude_me_view, name='invitation-profiles'),
]
