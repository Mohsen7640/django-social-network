from django.shortcuts import get_object_or_404

from account.models import Profile, Relationship


def profile_avatar(request):
    if request.user.is_authenticated:
        profile_obj = get_object_or_404(Profile, user=request.user)
        avatar = profile_obj.avatar
        return {'avatar': avatar}
    return {}


def invitations_received_no(request):
    if request.user.is_authenticated:
        profile_obj = get_object_or_404(Profile, user=request.user)
        relationship_qs = Relationship.objects.invitations_received(receiver=profile_obj)
        return {'invitations_received_no': relationship_qs.count()}
    return {}


def invitations_forward_no(request):
    if request.user.is_authenticated:
        profile_obj = get_object_or_404(Profile, user=request.user)
        relationship_qs = Relationship.objects.invitations_forward(sender=profile_obj)
        return {'invitations_forward_no': relationship_qs.count()}
    return {}
