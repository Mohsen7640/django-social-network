from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404

import account.models as model


class RelationshipManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def invitations_received(self, receiver):
        qs = self.get_queryset().filter(receiver=receiver, status='send')
        return qs

    def invitations_forward(self, sender):
        qs = self.get_queryset().filter(sender=sender, status='send')
        return qs


class ProfileManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_all_profiles(self, me):
        """Get all profiles exclude own profile"""
        profiles = self.get_queryset().exclude(user=me)
        return profiles

    def get_all_profiles_to_invitation(self, sender):
        profiles = self.get_all_profiles(me=sender)  # Get all profile exclude sender(me)
        profile = get_object_or_404(self.get_queryset(), user=sender)  # Get sender(me) profile

        qs = model.Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = set()
        for relation in qs:
            if relation.status == 'accepted':
                accepted.add(relation.receiver)
                accepted.add(relation.sender)

        available = [profile for profile in profiles if profile not in accepted]
        return available
