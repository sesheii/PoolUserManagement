from django.shortcuts import render, redirect
from app.forms import UserForm, AssignMembershipForm, MembershipForm
from django.utils import timezone
from app.models import User, UserMembership, MembershipType, CheckInCheckOut
from datetime import timedelta


def main(request):
    return render(request, 'main.html')


def manage_user_memberships(request):
    user_data = None
    user_memberships = None
    all_user_memberships = None
    user_id = request.session.get('user_id', None)

    if request.method == 'POST':
        form = UserForm(request.POST)
    else:
        form = UserForm(initial={'user_id': user_id})

    assign_membership_form = AssignMembershipForm()

    if user_id:
        user_data = User.objects.filter(id=user_id).first()
        if user_data:
            user_memberships = user_data.usermembership_set.filter(end_date__gte=timezone.now()).all()
            all_user_memberships = user_data.usermembership_set.all()
        else:
            request.session.pop('user_id', None)

    if request.method == 'POST':
        if 'assign_membership' in request.POST:
            assign_membership_form = AssignMembershipForm(request.POST)
            if assign_membership_form.is_valid() and user_id:
                user = User.objects.get(id=user_id)
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

from django.shortcuts import redirect

def check_in_check_out(request):
    user_data = None
    all_sessions = None
    active_sessions = None
    alert_message = None
    alert_class = None

    # Retrieve or set user_id from/in the session
    user_id = request.POST.get('user_id') or request.session.get('user_id')
    if user_id:
        request.session['user_id'] = user_id  # Store/update user_id in the session
        user_data = User.objects.filter(id=user_id).first()

        if user_data:
            all_sessions = CheckInCheckOut.objects.filter(user=user_data).order_by('-check_in_time')
            active_sessions = all_sessions.filter(check_out_time__isnull=True)

            if 'check_in' in request.POST:
                if user_data.is_blocked or not user_data.usermembership_set.filter(end_date__gte=timezone.now()).exists():
                    alert_message = "Доступ заборонено"
                    alert_class = "danger"
                else:
                    CheckInCheckOut.objects.create(user=user_data, check_in_time=timezone.now())
                    alert_message = "Check-in session created successfully"
                    alert_class = "success"

            if 'check_out_session' in request.POST:
                session_id = request.POST.get('session_id')
                session = CheckInCheckOut.objects.get(id=session_id)
                session.check_out_time = timezone.now()
                session.save()

    return render(request, 'check_in_check_out.html', {
        'user_id': user_id,  # Pass the user_id to the template
        'user_data': user_data,
        'all_sessions': all_sessions,
        'active_sessions': active_sessions,
        'alert_message': alert_message,
        'alert_class': alert_class
    })

