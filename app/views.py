from django.shortcuts import render, redirect
from app.forms import UserForm, AssignMembershipForm, MembershipForm
from django.utils import timezone
from app.models import User, UserMembership, MembershipType
from datetime import timedelta


def main(request):
    return render(request, 'main.html')


def manage_user_memberships(request):
    user_data = None
    user_memberships = None
    all_user_memberships = None
    form = UserForm(request.POST or None)
    assign_membership_form = AssignMembershipForm()

    # Перевірка, чи є 'user_id' в сесії
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_data = User.objects.filter(id=user_id).first()
        if user_data:
            user_memberships = user_data.usermembership_set.filter(end_date__gte=timezone.now()).all()
            all_user_memberships = user_data.usermembership_set.all()
        else:
            request.session.pop('user_id', None)

    if request.method == 'POST':
        if 'assign_membership' in request.POST and 'user_id' in request.session:
            assign_membership_form = AssignMembershipForm(request.POST)
            if assign_membership_form.is_valid():
                membership_type = assign_membership_form.cleaned_data['membership_type']

                if 'user_id' in request.session:
                    user_id = request.session['user_id']
                    user = User.objects.get(id=user_id)

                    existing_membership = user.usermembership_set.filter(end_date__gte=timezone.now()).first()
                    if not existing_membership:
                        start_date = timezone.now()
                        end_date = start_date + timedelta(days=membership_type.duration)

                        UserMembership.objects.create(
                            user=user,
                            membership_type=membership_type,
                            start_date=start_date,
                            end_date=end_date
                        )

                    user_memberships = user.usermembership_set.filter(end_date__gte=timezone.now()).all()
        elif 'delete_membership' in request.POST:
            membership_id = request.POST.get('membership_id')
            if membership_id:
                try:
                    membership_to_delete = UserMembership.objects.get(id=membership_id)
                    if membership_to_delete.user_id == user_id:
                        membership_to_delete.delete()
                except UserMembership.DoesNotExist:
                    pass
        elif form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            user_data = User.objects.filter(id=user_id).first()
            if user_data:
                request.session['user_id'] = user_id
                user_memberships = user_data.usermembership_set.filter(end_date__gte=timezone.now()).all()
                all_user_memberships = user_data.usermembership_set.all()
            else:
                request.session.pop('user_id', None)

    context = {
        'form': form,
        'assign_membership_form': assign_membership_form,
        'user_data': user_data,
        'user_memberships': user_memberships,
        'all_user_memberships': all_user_memberships
    }
    return render(request, 'manage_user_memberships.html', context)


def manage_memberships(request):
    if request.method == 'POST':
        if 'delete_membership_id' in request.POST:
            membership_id = request.POST.get('delete_membership_id')
            membership = MembershipType.objects.get(id=membership_id)
            membership.delete()
            return redirect('manage-memberships')
        
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-memberships')
    else:
        form = MembershipForm()

    memberships = MembershipType.objects.all()
    return render(request, 'manage_memberships.html', {
        'form': form,
        'memberships': memberships
    })
