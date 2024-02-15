from django.shortcuts import render, redirect
from django.urls import reverse
from App_House.models import HouseOwner
from App_House.forms import CreateOwnerForm, LockOpenForm, ChangePasswordForm

from django.contrib import messages


# Create your views here.

def index(request):
    return redirect('App_House:outsideHouse')

def createOwner(request):
    all_owner = HouseOwner.objects.all()
    if all_owner.exists():
        if all_owner[0].attempt <= 0:
            return redirect('App_House:alert')
        if len(all_owner) >= 1:
            messages.info(request,"Only 1 Profile can be create!")
            return redirect('App_House:outsideHouse')
    else:
        form = CreateOwnerForm()
        if request.method == 'POST':
            form = CreateOwnerForm(request.POST)
            if form.is_valid():
                if request.POST['password_1'] != request.POST['password_2']:
                    messages.warning(request,"Passwords did not match!")
                    form = CreateOwnerForm(request.POST)
                    return render(request, 'App_House/createOwner.html', context={'form': form})
                form.save()
                messages.success(request,"Lock Created Successfully!")
                return redirect('App_House:outsideHouse')
    return render(request, 'App_House/createOwner.html', context={'form': form})

def lockOpen(request):
    all_owner = HouseOwner.objects.all()
    
    if len(all_owner) == 0:
        messages.info(request,"Create a lock profile first!")
        return redirect('App_House:createOwner')
    if all_owner[0].attempt <= 0:
        messages.warning(request,"Your chance is finished!")
        return redirect('App_House:alert')
    owner = all_owner[0]
    if owner.unlock == True:
        messages.info(request,"Already unlocked!")
        return redirect('App_House:insideHouse')
    form = LockOpenForm()
    if request.method == 'POST':
        form = LockOpenForm(request.POST)
        if form.is_valid():
            if owner.password_1 == request.POST['password_1']:
                owner.unlock = True
                owner.attempt = 3
                owner.save()
                messages.success(request,"House unlocked successfull!")
                return redirect('App_House:insideHouse')
            else:
                messages.warning(request,"Wrong password!")
                form = LockOpenForm()
                owner.attempt -= 1
                owner.save()
            if owner.attempt <= 0:
                messages.warning(request,"Your chance has been finished!")
                return redirect('App_House:alert')
    attempt = owner.attempt
    return render(request, 'App_House/lockOpen.html', context={'form': form, 'attempt': attempt})


def lockClose(request):
    all_owner = HouseOwner.objects.all()
    if len(all_owner) == 0:
        messages.info(request,"Create a lock profile first!")
        return redirect('App_House:createOwner')
    if all_owner[0].attempt <= 0:
        return redirect('App_House:alert')
    owner = all_owner[0]
    owner.unlock = False
    owner.save()
    messages.success(request,"House has been locked!")
    return redirect('App_House:outsideHouse')


def insideHouse(request):
    all_owner = HouseOwner.objects.all()
    if len(all_owner) == 0:
        messages.info(request,"Create a lock profile first!")
        return redirect('App_House:createOwner')
    if all_owner[0].attempt <= 0:
        messages.success(request,"Can't enter to house!")
        return redirect('App_House:alert')
    if all_owner[0].unlock == False:
        messages.success(request,"House is lock!")
        return redirect('App_House:outsideHouse')
    return render(request, 'App_House/insideHouse.html')

def outsideHouse(request):
    all_owner = HouseOwner.objects.all()
    if len(all_owner) == 0:
        return redirect('App_House:createOwner')
    if all_owner[0].attempt <= 0:
        messages.warning(request,"You can't move right now!")
        return redirect('App_House:alert')
    if all_owner[0].unlock == True:
        messages.success(request,"Lock first to go outside!")
        return redirect('App_House:insideHouse')
    return render(request, 'App_House/outsideHouse.html')

def alert(request):
    all_owner = HouseOwner.objects.all()
    form = LockOpenForm()
    if len(all_owner) == 0:
        messages.info(request,"Create a lock profile first!")
        return redirect('App_House:createOwner')
    if all_owner[0].attempt != 0:
        messages.info(request,"You have chance to unlock!")
        return redirect('App_House:lockOpen')
    if request.method == 'POST':
        form = LockOpenForm(request.POST)
        if form.is_valid():
            if all_owner[0].password_1 == request.POST['password_1']:
                all_owner[0].attempt = 3
                all_owner[0].save()
                messages.success(request,"Alarm stopped!")
                return redirect('App_House:outsideHouse')
            form = LockOpenForm()
            messages.warning(request,"Wrong password!")
    return render(request, 'App_House/alert.html', context={'form': form})


def change_password(request):
    all_owner = HouseOwner.objects.all()
    if len(all_owner) == 0:
        messages.info(request,"Create a lock profile first!")
        return redirect('App_House:createOwner')
    if all_owner[0].attempt <= 0:
        messages.warning(request,"You can't move right now!")
        return redirect('App_House:alert')
    if all_owner[0].unlock == False:
        messages.warning(request,"Unlock first to change password!")
        return redirect('App_House:lockOpen')
    form = ChangePasswordForm()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.POST['password_1'] != request.POST['password_2']:
                messages.warning(request,"Password did not match!")
            else:
                messages.success(request,"Password changed!")
                all_owner[0].password_1 = request.POST['password_1']
                all_owner[0].password_2 = request.POST['password_2']
                all_owner[0].save()
                return redirect('App_House:lockClose')
    return render(request, 'App_House/changepass.html', context={'form': form})

