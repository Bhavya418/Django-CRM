from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()
    # Check to see if loggin in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate 
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged In!")
            return redirect('home')
        else: 
            messages.error(request, " There was an error Logging In. Please try again...")
            return redirect('home')
    else:    
        return render(request,'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out... ")
    return redirect('home')

def register_user(request):
        if request.method =="POST":
             form = SignUpForm(request.POST)
             if form.is_valid():
                  form.save()
                  #Authenticate and Login
                  username = form.cleaned_data['username']
                  password = form.cleaned_data['password1']
                  user = authenticate(username=username, password=password)
                  login(request,user)
                  messages.success(request,"You have successfully registered!")
                  return redirect('home')
        else:
             form = SignUpForm()     
             return render(request,'register.html',{'form':form})   
        return render(request,'register.html',{'form':form}) 

def customer_record(request,pk):
    if request.user.is_authenticated:
         #Lookup record
         customer_record= Record.objects.get(id=pk)
         return render(request,'record.html',{'customer_record':customer_record})
    else:
         messages.error(request,"You must have logged In to view the record")
         return redirect('home')
