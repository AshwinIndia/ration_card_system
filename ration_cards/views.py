from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RationCard, FamilyMember, Distribution, Complaint
from .forms import RationCardForm, FamilyMemberForm, ComplaintForm

def home(request):
    return render(request, 'ration_cards/home.html')

#@login_required
def apply_for_card(request):
    if request.method == 'POST':
        form = RationCardForm(request.POST)
        if form.is_valid():
            ration_card = form.save(commit=False)
            ration_card.user = request.user
            ration_card.save()
            messages.success(request, 'Ration card application submitted successfully.')
            return redirect('ration_card_detail', pk=ration_card.pk)
    else:
        form = RationCardForm()
    return render(request, 'ration_cards/apply.html', {'form': form})

#@login_required
def ration_card_detail(request, pk):
    ration_card = get_object_or_404(RationCard, pk=pk, user=request.user)
    family_members = ration_card.family_members.all()
    return render(request, 'ration_cards/ration_card_detail.html', {
        'ration_card': ration_card,
        'family_members': family_members
    })

#@login_required
def add_family_member(request, ration_card_pk):
    ration_card = get_object_or_404(RationCard, pk=ration_card_pk, user=request.user)
    if request.method == 'POST':
        form = FamilyMemberForm(request.POST)
        if form.is_valid():
            family_member = form.save(commit=False)
            family_member.ration_card = ration_card
            family_member.save()
            messages.success(request, 'Family member added successfully.')
            return redirect('ration_card_detail', pk=ration_card.pk)
    else:
        form = FamilyMemberForm()
    return render(request, 'ration_cards/add_family_member.html', {'form': form, 'ration_card': ration_card})

#@login_required
def check_status(request):
    ration_cards = RationCard.objects.filter(user=request.user)
    return render(request, 'ration_cards/check_status.html', {'ration_cards': ration_cards})

#@login_required
def distribution_history(request):
    ration_cards = RationCard.objects.filter(user=request.user)
    distributions = Distribution.objects.filter(ration_card__in=ration_cards).order_by('-distribution_date')
    return render(request, 'ration_cards/distribution_history.html', {'distributions': distributions})

#@login_required
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            messages.success(request, 'Complaint filed successfully.')
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'ration_cards/file_complaint.html', {'form': form})

#@login_required
def complaint_list(request):
    complaints = Complaint.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ration_cards/complaint_list.html', {'complaints': complaints})