from bugreport.models import Ticket
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bugreport.forms import AddTicket, Login_Form, Change_Status_Form


@login_required
def index(req):
    html = 'index.html'
    data = Ticket.objects.all().order_by("time")
    new = Ticket.objects.filter(status='New').order_by("time")
    in_progress = Ticket.objects.filter(status='In-Progress').order_by('time')
    done = Ticket.objects.filter(status='Done').order_by('time')
    invalid = Ticket.objects.filter(status='Invalid').order_by('time')
    return render(req, html, {
        'data': data,
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'invalid': invalid
    })


@login_required
def submit_ticket(req):
    html = 'submit_ticket.html'
    if req.method == 'POST':
        form = AddTicket(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            Ticket.objects.create(
                creator=req.user,
                title=data['title'],
                body=data['body']
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = AddTicket()
    return render(req, html, {'form': form})


@login_required
def single_ticket(req, id):
    html = 'ticket.html'
    data = Ticket.objects.filter(id=id)
    return render(req, html, {'data': data})


def login_view(req):
    html = "submit_ticket.html"
    if req.method == "POST":
        form = Login_Form(req.POST)
        if form.is_valid():
            res = form.cleaned_data
            u = authenticate(
                username=res['username'],
                password=res['password']
            )
            if u:
                login(req, u)
                return HttpResponseRedirect(
                    req.GET.get('next', reverse('homepage'))
                )
    form = Login_Form()
    return render(req, html, {'form': form})


def logout_view(req):
    logout(req)
    return HttpResponseRedirect(reverse('homepage'))


def user_tickets(req, id):
    html = "user.html"
    user = User.objects.get(pk=id)
    created_by = Ticket.objects.filter(creator_id=id)
    assigned_user = Ticket.objects.filter(assigned_user=id)
    completed_by = Ticket.objects.filter(completed_by=id)
    return render(req, html, {
        "created_by": created_by,
        "completed_by": completed_by,
        "assigned_user": assigned_user,
    })


@login_required
def change_status(req, id):
    html = "status.html"
    ticket = Ticket.objects.get(id=id)
    if req.method == "POST":
        form = Change_Status_Form(req.POST, initial={
            'status': ticket.status,
        })
    if ticket.status == "New":
        ticket.assigned_user = None
    if ticket.status == "In-Progress":
        ticket.assigned_user = req.user
        ticket.completed_by = None
    if ticket.status == "Done":
        ticket.assigned_user = None
        ticket.completed_by = req.user
    if ticket.status == "Invalid":
        ticket.assigned_user = None
        ticket.completed_by = None
    if form.is_valid():
        ticket.status = form.cleaned_data["status"]
        ticket.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = Change_Status_Form(req.POST, initial={
        "status": ticket.status
    })
    return render(req, html, {'form': form})


def edit_ticket(req, id):
    html = "edit.html"
