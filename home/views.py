from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponse
from .models import Person
from .models import complainant
from .models import women
from django.contrib.auth.models import  User
from .resources import PersonResource
from django.core.mail import send_mail
from tablib import Dataset
import speech_recognition as sr
import pyttsx3  
import os
import random
from django.db.models import Q
from EFIR.settings import EMAIL_HOST_USER
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login 
from .keywordname import predictCrimeName
   
# Create your views here.
def index(request):
    context = {
        'variable' : "This is var"
    }

    return render(request,'index.html',context)

def register(request):
    if request.POST.get('speech'):
        data = request.POST.get('record')

        # get audio from the microphone

        r = sr.Recognizer()
    
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2) 
                print("Speak:")
                audio = r.listen(source)
                output = " " + r.recognize_google(audio)
        except sr.UnknownValueError:
            output = "Could not understand audio"
        except sr.RequestError as e:
            output = "Could not request results; {0}".format(e)
        data =output
        return render(request,'register.html',{'data':data})
    if request.POST.get('recordFir'):
        # get thhe post parameters
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mobileNo = request.POST['mobileNo']
        address = request.POST['incidentAddress']
        print(fname+lname)
        return render(request,'register.html')
    return render(request,'register.html')

def loginhandle(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['inputUserName']
        loginpassword=request.POST['inputPassword']

        user = complainant.objects.filter(email = loginusername).first()
        
        if user:
            flag = check_password(loginpassword,user.password)
            if flag:
                messages.success(request, "Successfully Logged In")
                return redirect("register")
            else:
                messages.error(request, "Invalid credentials! Please try again")
                return redirect("home")
            
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")
    return render(request,'login.html')

def simple_upload(request):
    if request.method == 'POST':
        # Person_resource = PersonResource()
        dataset = Dataset()
        new_person = request.Files['myfile']

        if not new_person.name.endswith('xlxs'):
            messages.info(request,'wrong format')
            return render(request,'upload.html')
        
        imported_data = dataset.load(new_person.read(),format='xlxs')
        for data in imported_data:
            value = Person(
                data[0],
                data[1],
                data[2],
                data[3]
            )
            value.save()
    return render(request,'upload.html')

def userregister(request):
    if request.method == 'POST':
        # get thhe post parameters
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mobileNo = request.POST['mobileNo']
        address = request.POST['address']
        password = random.randint(1000,9999)
        
        if fname and lname and email and mobileNo and address:
            
            subject = 'Welcome to E-POLICE'
            message = 'Hello, ' + fname +" "+ lname + ' you are now successfully reistered on E-POLICE\n' + 'You can now login to your account using crendentials given below\n'+ 'username: ' + str(email)  +  '\npassword: ' + str(password)

            recepient = str(email)
            send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            password_hash = make_password(str(password))
            user = complainant(fname = fname,lname=lname,email=email,mobileNo=mobileNo,address=address,password=password_hash)
            user.save()
            messages.success(request,"Your account has been successfully created, you can now login using username and password sent to your email id")
            return redirect('home')
        # create user
        else:
            messages.error(request,"fill all details")
            return redirect('userregister')

   
    return render(request,'user_register.html')

def predictor(request):
    if request.method == 'POST':
        # get thhe post parameters
        tableName = request.POST['category']
        if tableName == 'Crime against women':
            tableName = 'women'

        marritalStatus = request.POST['married']
        suspectNo = request.POST['suspectNo'] 
        victimage = request.POST['age']
        gender = request.POST['gender']
        desc = request.POST['desc']
        crimeName = predictCrimeName(desc,tableName); 
        print(crimeName)
        print(victimage,marritalStatus,suspectNo)
        if not crimeName: 
            print('Unable to find crime name')
        else:
            for crimename in crimeName:
                # crime = women.objects.filter(crimeName = crimename)
                # print(crime)
                if int(suspectNo) >=2 and crimename=='Rape':
                    crime = women.objects.filter(crimeName = crimename,maritalStatus = marritalStatus,accussedNum__gte = 2)
                else:
                    crime = women.objects.filter(crimeName = crimename)
                if not crime:
                    print('Unable to predict IPC section')
                else:
                    for crimeobject in crime:
                        if(int(victimage) >= int(crimeobject.age) and crimeobject.condition == '>=' ):
                            print(crimeobject.section)
                        elif(int(victimage) < int(crimeobject.age) and crimeobject.condition == '<'):
                            print(crimeobject.section)
       
            
                
    return render(request,'predictor.html')   