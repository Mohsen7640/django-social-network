from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.db.models import Q

from account.models import Profile, Relationship
from account.forms import UpdateProfileForm


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = UpdateProfileForm(instance=profile)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'account/profile/profile.html', context)


@login_required
@require_POST
def update_profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = UpdateProfileForm(data=request.POST or None, files=request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()

    return redirect('account:profile')


@login_required
def invitations_received_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    qs = Relationship.objects.invitations_received(receiver=profile)

    sender = []
    for relation in qs:
        sender.append(relation.sender)
    
    is_empty = not bool(sender)
    context = {
        'qs': sender,
        'is_empty': is_empty
    }
    return render(request, 'account/profile/invitation_received.html', context)


def invitations_forward_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    qs = Relationship.objects.invitations_forward(sender=profile)

    receiver = []
    for relation in qs:
        receiver.append(relation.receiver)

    is_empty = not bool(receiver)

    context = {
        'qs': receiver,
        'is_empty': is_empty
    }
    return render(request, 'account/profile/invitation_forward.html', context)


@login_required
@require_POST
def accept_invitation(request):
    pk = request.POST.get('profile_pk')
    user = request.user

    sender = get_object_or_404(Profile, pk=pk)
    receiver = get_object_or_404(Profile, user=user)

    relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
    relationship.status = Relationship.ACCEPTED
    relationship.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def reject_invitation(request):
    pk = request.POST.get('profile_pk')
    user = request.user

    sender = get_object_or_404(Profile, pk=pk)
    receiver = get_object_or_404(Profile, user=user)
    
    relationship = get_object_or_404(Relationship, sender=sender, receiver=receiver)
    relationship.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def invitation_profile_list_exclude_me_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invitation(sender=user)

    context = {
        'qs': qs
    }
    return render(request, 'account/profile/invitation_profile_list.html', context)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'account/profile/profile_detail.html'
    model = Profile

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Profile, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(Profile, user=self.request.user)
        relationship_receiver_qs = Relationship.objects.filter(sender=profile)
        relationship_sender_qs = Relationship.objects.filter(receiver=profile)

        user_receiver = []
        user_sender = []

        for relation in relationship_receiver_qs:
            user_receiver.append(relation.receiver.user)

        for relation in relationship_sender_qs:
            user_sender.append(relation.sender.user)

        context['user_receiver'] = user_receiver
        context['user_sender'] = user_sender
        context['posts'] = self.get_object().get_posts()
        context['posts_no'] = bool(self.get_object().get_posts_no())

        return context


class ProfileListExcludeMeView(LoginRequiredMixin, ListView):
    template_name = 'account/profile/profile_list.html'
    model = Profile

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(me=self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = get_object_or_404(Profile, user=self.request.user)
        relationship_receiver_qs = Relationship.objects.filter(sender=profile)
        relationship_sender_qs = Relationship.objects.filter(receiver=profile)

        user_receiver = []
        user_sender = []

        for relation in relationship_receiver_qs:
            user_receiver.append(relation.receiver.user)

        for relation in relationship_sender_qs:
            user_sender.append(relation.sender.user)

        context['user_receiver'] = user_receiver
        context['user_sender'] = user_sender
        context['is_empty'] = not bool(self.get_queryset())
        return context


@login_required
@require_POST
def send_invitation(request):
    pk = request.POST.get('profile_pk')
    user = request.user

    sender = get_object_or_404(Profile, user=user)
    receiver = get_object_or_404(Profile, pk=pk)

    Relationship.objects.create(sender=sender, receiver=receiver, status=Relationship.SEND)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
@require_POST
def remove_from_friends(request):
    pk = request.POST.get('profile_pk')
    user = request.user

    sender = get_object_or_404(Profile, user=user)
    receiver = get_object_or_404(Profile, pk=pk)

    relationship = Relationship.objects.get(
        (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
    )
    relationship.delete()

    return redirect(request.META.get('HTTP_REFERER'))