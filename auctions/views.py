from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from . import forms

from .models import *


def index(request):
    listings = Auction_listings.objects.all()
    return render(request, "auctions/index.html", {
        "amounts": Bid.objects.all(),
        "listings": listings,
        "categories": Category.objects.all(),
    })
    
def list_page(request, list_id):
    if request.user.is_authenticated:
        list_auction = Auction_listings.objects.get(pk=list_id)
        #comment_form = forms.Create_comment()
        #comments = Comment.objects.get(pk = list_id)
        categories = Category.objects.get(pk = list_id)
        #categories.auctions.add(list_auction)
        return render(request, "auctions/auc_details.html", {
            "detail": list_auction,
            "cats":categories,
            "user": request.user,
            "comments": list_auction.comment.all(),
            #"commentForm": comment_form,
            #"non_passenger": Passenger.objects.exclude(flights=flight).all()
        })
    else:
        list_auction = Auction_listings.objects.get(pk=list_id)
        return render(request, "auctions/auc_details.html", {
            "detail": list_auction,
            #"form": comment_form()
            #"": list_auction..all(),
            #"non_passenger": Passenger.objects.exclude(flights=flight).all()
        })

#@login_required(REDIRECT_FIELD_NAME= "login")
def create_listing(request):
    form = forms.Create_listing(request.POST,request.FILES)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = form
            if form.is_valid():
                text = form.data["auc_created_by"]
                #text = text.request.user
                form.save()
                #listing = Auction_listings.objects(form)
                #listing.save()
            else:
                return render(request, "auctions/newListing.html",{
                    "form":form,
                })        
        return render (request,"auctions/newListing.html", {
            "form": forms.Create_listing()
        })
        
def comment(request, list_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            list_auction = Auction_listings.objects.get(pk=list_id)
            comment_form = forms.Create_comment(request.POST)
            comment_form = comment_form
            if comment_form.is_valid():
                comment = comment_form["text"]
                last_id = Comment.id[-1]
                new_id = last_id + 1
                comment_detail = Comment(id = new_id, comment_by=request.user, comment_on=list_auction, comment=comment, comment_date_published=datetime.now())
                comment_detail.save()
                categories = Category.objects.get(pk = list_id)
                return render(request, "auctions/auc_details.html", {
                    "detail": list_auction,
                    "cats":categories,
                    "user": request.user,
                    "comments": list_auction.comment.all(),
                    #"commentForm": comment_form,
                    #"non_passenger": Passenger.objects.exclude(flights=flight).all()
                })  
                #return HttpResponseRedirect(reverse("auctions_list", args=(list_auction.id,)))
            else:
                #pass
                return render(request, "auctions/auc_details.html",{
                    "form":comment_form,
                })
        return render (request, "auctions/auc_details.html",{
            "form": forms.Create_comment()
                })

       


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
