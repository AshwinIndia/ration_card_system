from django import forms
from .models import RationCard, FamilyMember, Complaint

class RationCardForm(forms.ModelForm):
    class Meta:
        model = RationCard
        fields = ['card_type', 'fair_price_shop']

class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ['name', 'age', 'gender', 'relationship', 'aadhar_number']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description', 'ration_card']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ration_card'].required = False