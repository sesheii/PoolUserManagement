from django import forms
from app.models import MembershipType


class UserForm(forms.Form):
    user_id = forms.IntegerField(label='User ID')


class AssignMembershipForm(forms.Form):
    membership_type = forms.ModelChoiceField(queryset=MembershipType.objects.all(), empty_label="Виберіть тип підписки")
