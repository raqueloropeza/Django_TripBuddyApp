from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, Trips
import bcrypt
import re
from datetime import date, datetime
from time import strftime, strptime

#main route that displays login and registration template
def index(request):
    return render(request, "index.html")

#register route creates new user record in database
def register(request):
    #Retrieve any errors from validations in models
    errors = Users.objects.basic_validator(request.POST)
    #If there are errors from model, redirect to main route and display error messages. 
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    #If there are no errors found, retrieve password from POST data and encrypt.
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        #Retrieve encrypted password and input fields from POST data to create new user record in database.
        this_user = Users.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password= pw_hash)
        #Put new user id in session
        request.session['user_id'] = this_user.id
        print(this_user.id)
        #redirect to dashboard route
        return redirect('/dashboard')

#Login route takes email from POST data and filters through user object to try to find matching email
def login(request):
    user =  Users.objects.filter(email=request.POST['email'])
    #If matching email in user object is found, check to see if password from POST data matches password from user object
    if user:
        logged_user = user[0]
        if  bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            #if passwords match, put user id in session and redirect to success route
            request.session['user_id'] = logged_user.id
        return redirect('/dashboard')
    #if passwords don't match, redirect to main route and display message error.
    else:
        messages.error(request, "invalid login")
        return redirect('/')
#Logout route clears user id in session and redirects to main route
def logout(request):
    del request.session['user_id']
    return redirect('/')

#Get for route /dashboard
def dashboardPage(request):
    #Check if user id is in session.  If not redirect to main route with login/reg
    if "user_id" not in request.session:
        return redirect('/')
    #If user id is is in session, get all trips created by user in session, get all trips joined by user in session, and all trips not joined by user in session.
    else: 
        context = {
            "all_users": Users.objects.all(),
            "this_user": Users.objects.get(id=request.session['user_id']),
            "user_trips": Users.objects.get(id=request.session['user_id']).trips_uploaded.all(),
            "other_trips":Trips.objects.exclude(uploaded_by= request.session['user_id']),
            "joined_trips":Trips.objects.filter(users_who_joined = request.session['user_id']),
            "notjoined": Trips.objects.exclude(users_who_joined = request.session['user_id'])
        }
        return render(request, "dashboard.html", context)

#Get for route /new/trips that displays form template to create new trip.
def newPage(request):
    #Checks that user id is in session.  If not in session, redirect to main route
    if "user_id" not in request.session:
        return redirect('/')
    #If user id is in session, retrieve user object.
    context = {
        "this_user": Users.objects.get(id=request.session['user_id']),
    }
    return render(request, "newtrip.html", context)

#POST route to create new trip in database
def createtrip(request):
    print(request.POST)
    #checks that user id is in session.  If not in session, redirect to main route
    if "user_id" not in request.session:
        return redirect('/')
    #if user id is in session. Check validation errors in trip model
    else:
        errors = Trips.objects.basic_validator(request.POST)
        #if errors are found, redirect back to /trips/new and display error messages
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/trips/new')
        #if no errors are found, retrieve user id from session.  
        else: 
            user= request.session['user_id']
            #Take POST data and user id from session to create new trip record in database and redirect to dashboard
            Trips.objects.create(destination=request.POST['destination'], start_date=request.POST['startdate'], end_date=request.POST['enddate'], uploaded_by= Users.objects.get(id= user), plan=request.POST['plan'])
            return redirect('/dashboard')

#Get route to display trip from route trips/id
def tripPage(request, id):
    #check if user id is in session. If not, redirect to main login/reg page
    if "user_id" not in request.session:
        return redirect('/')
    #if user is in session, get trip object using id from route trips/id, get user object from id in session, and all users who have joined trip using trip id from route trips/id
    else:
    context = {
        "this_trip": Trips.objects.get(id=id),
        "this_user": Users.objects.get(id=request.session['user_id']),
        "joined_users":Trips.objects.get(id=id).users_who_joined.all(),
    }
    return render(request, "tripinfo.html", context)

#POST route to join trip
def joinTrip(request, id):
    #check if user id is in session.  If not, then redirect to main route
    if "user_id" not in request.session:
        return redirect('/')
    #if user id is in session, get trip object from id in route join/id, and get user object from id in session
    else: 
        this_trip = Trips.objects.get(id=id)
        this_user = Users.objects.get(id=request.session['user_id'])
        #if user has already joined trip, then destroy record from object to remove user from trip
        if this_user in this_trip.users_who_joined.all():
            this_trip.users_who_joined.remove(this_user)
        #if user has not joined trip, then create record and redirect to dashboard page
        else:
            this_trip.users_who_joined.add(this_user)
        print(this_trip.users_who_joined.all())
        return redirect('/dashboard')

#Get method to display edit form to update trip using id from route trips/edit/id
def editTrip (request, id):
    #check if user id is in session.  If not, redirect to main route and display login/reg page
    if "user_id" not in request.session:
        return redirect('/')
    else:
        #if user id is in session, get trip object using id from route trips/edit/id
        trip = Trips.objects.get(id=id)
        #reformat start_date and end_date to display dates as MM/DD/YYYY
        start_date_format = trip.start_date.strftime('%m/%d/%Y')
        end_date_format = trip.end_date.strftime('%m/%d/%Y')
        #get user id from session
        context = {
            "this_trip": trip,
            "this_user": Users.objects.get(id=request.session['user_id']),
            "formatted_startdate" : start_date_format,
            "formatted_enddate" : end_date_format,
        }
        return render(request, "edittrip.html", context)
#PUT route to update trip using id from trips/id/update
def updatetrip(request, id):
    #check for any validation errors from models 
    errors = Trips.objects.basic_validator(request.POST)
    #if errors found, redirect back to edit form and display error messages
    if len(errors)> 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trips/edit/{id}")
    #if no errors found update record using POST data from edit form 
    else:
        #reformat start date back to YYYY-MM-D
        input_startdate= request.POST['startdate']
        current_startdate= datetime.strptime(input_startdate, '%m/%d/%Y')
        formatted_startdate= current_startdate.strftime('%Y-%m-%d')

        #reformat end date back to YYYY-MM-D
        input_enddate= request.POST['enddate']
        current_enddate= datetime.strptime(input_enddate, '%m/%d/%Y')
        formatted_enddate= current_enddate.strftime('%Y-%m-%d')

        update = Trips.objects.get(id=id)
        update.destination = request.POST['destination']
        update.start_date = formatted_startdate
        update.end_date = formatted_enddate
        update.plan = request.POST['plan']
        update.save()
        return redirect("/dashboard")

#Delete route using trip id from trips/delete/id
def deletetrip(request, id):
    #if user id is not in session, redirect to main route and display login/reg
    if "user_id" not in request.session:
        return redirect('/')
    #if user id is in session, get trip object using id from route trips/delete/id
    else: 
        this_trip = Trips.objects.get(id= id)
        #check to make sure user id from session matches the same user id as the user that created the trip record
        #if user id does not match, redirect to main route
        if this_trip.uploaded_by.id != request.session['user_id']:
            return redirect('/')
        #if user id does match, delete record 
        else:
            this_trip.delete()
        return redirect("/dashboard")
    
    
