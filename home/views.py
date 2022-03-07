import random
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from accounts.forms import CreateProfileForm
from accounts.serializer import ProfileSerializers
from accounts.forms import Image_VistingForm
from home.models import Image_visiting
from .serializers import VisitingSerializers,Img_visitingSerializers
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.forms import CreateProfileForm, ProfileUpdate
from django.urls import reverse
from rest_framework.decorators import api_view
from accounts.forms import ProfileUpdate
from accounts.models import *
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.forms import VistingForm
from home.models import Visiting
import os
from twilio.rest import Client
from datetime import date
from django.contrib import messages



#func to route admin and user
@api_view(['GET','POST'])
@csrf_exempt                
def homepage(request):
      if request.user.is_authenticated and request.user.is_superuser:
            return redirect('home:home')


      return redirect('home:homeuser')

#func get all profile in home admin page to do actions delete add .....
def getprofile(request):
            profile=Profile.objects.all().order_by('-created')
            Serializer=ProfileSerializers(profile,many=True)  
            data=Serializer.data
            paginator=Paginator(data,7)
            page_number=request.GET.get('page')
            return paginator.get_page(page_number)

#fun get all visiting of user by id of user
def getvisitng(request,unique_id):
            visiting=Visiting.objects.filter(profile_id=unique_id).order_by('-unique_id')
            Serializer=VisitingSerializers(visiting,many=True)  
            data=Serializer.data
            paginator=Paginator(data,7)
            page_number=request.GET.get('page')
            return paginator.get_page(page_number)

#func find user by phone number or name 
def search_user(request):
            q = request.POST.get('search_query')
            results = Profile.objects.filter(Q(name__icontains=q) | Q(mobile__icontains=q))
            Serializer=ProfileSerializers(results,many=True)  
            data=Serializer.data
            paginator=Paginator(data,7)
            page_number=request.GET.get('page')
            return paginator.get_page(page_number)  
#func get all image of one visiting by id 
def get_user_image_visiting(visiting_id):

    q=Image_visiting.objects.filter(visiting_id=visiting_id)
    serializers=Img_visitingSerializers(q,many=True)
    data=serializers.data
    return data
def sendsms(phone,password):   
    account_sid = 'AC66c89f275dac90f58ea3fd0683ee566f'
    auth_token = 'aaa769e2e8daf8c8e3f8db9061bfe454'
    client = Client(account_sid, auth_token)
    client.messages \
            .create(
                    body="مرحبا بك ف مركز اجنه الرقم السري الخاص بك هو : "+str(password)+" https://play.google.com/store/apps/details?id=com.agenna.agenna",
                    from_='+18482835968',
                    to='+2'+str(phone)
                    )
             
   
#func create profile by name , phone number and autogenrate password 
#before create profile create user contain username=phone number and password=password
#send sms that contain password and link of app in google paly


@login_required(login_url='login')
@api_view(['GET','POST'])
@csrf_exempt
def create_profile(request):
    
    '''
    #1 function to load all profile in page 
    #2 if method post and contain hidden input name='from_type' and value=adduser
    #3 take request in form 
    #4 if form valid get from form username=mobile,name=name 
    #5,6,7,8 create User with username=mobile and first_name=name ,password auto generated and return form if exception occure
    #9,10,11 create profile mobile=mobile,name=name,and return form if exception occure,
    #12,13 send sms to user contain password,load profiles to dispaly in home page
    #14 if method post and contain hidden input name='from_type' and value=search
    #15 function search profile and display result in home page 
    #16 load home page and dispaly list of profiles,and form create profile
    '''
    try:   
            profiles=getprofile(request)
                                                                 #1
            if request.method=='POST':
                if request.POST.get('form_type')=='adduser':                                #2
                                    form=CreateProfileForm(request.POST)                    #3
                                    if form.is_valid():  
                                        username = form.cleaned_data.get('mobile')          #4
                                        name= form.cleaned_data.get('name')                 #5
                                        user=User.objects.create(username=username,first_name=name) #6
                                        password=str(random.randrange(1111111111,9999999999))    #8
                                        user.set_password(str(password))
                                        user.save()
                                        profile_create=Profile.objects.create(user=user,name=name,mobile=username)
                                        profile_create.save()
                                        profiles=getprofile(request)                                                       #11
                                       
                                        m={"name":name,"password":password,"username":str(user)}
                                                                                       #12
                                        return render(request,'home.html',{'form1':form,'profiles':profiles,'m':m})      #13              
                                    else:
                                        m= None 
                                        form=CreateProfileForm(request.POST)
                                        return render(request,'home.html',{'form1':form,'profiles':profiles,'m':m})              #13
                elif request.POST.get('form_type')=='search':                             #14
                   form=CreateProfileForm() 
                   m= None                                              #15
                   profiles=search_user(request)
                   return render(request,'home.html',{'form1':form,'profiles':profiles,'m':m})
                else:
                 m= None 
                 form=CreateProfileForm()
                 return render(request,'home.html',{'form1':form,'profiles':profiles,'m':m})  
            else:
               m= None 
               form=CreateProfileForm()
               return render(request,'home.html',{'form1':form,'profiles':profiles,'m':m})      #13              
                                
    except :
           form=CreateProfileForm()
           m= None 
           return render(request,'home.html',{'form1':form,'profiles':profiles,'m':m})
                                                #16 



@login_required(login_url='login')
@api_view(['GET','POST'])
@csrf_exempt
def profileprint(request):
    return render(request,'print.html')
    
@login_required(login_url='login')
@api_view(['GET','POST'])
@csrf_exempt
def profileupdate(request,unique_id):
    '''
    #1,2 check user and profile exists
    #3,4,5,6,7 if user and profile exsits and form is valid save updating data and return the same page
    #8,9 if is not valid load same page with old data profile
    # if user no exists return home page  
    '''
    try:
       profile=Profile.objects.get(unique_id=unique_id)                             #1
       user=User.objects.get(id=profile.user_id)
       if profile and user:  
                if request.method=='POST':                                          #
                        profileform =ProfileUpdate(request.POST,instance=profile )  #5
                        if profileform.is_valid():     
                                profile.save()
                                profileform.save()
                                user.username=profileform.cleaned_data['mobile']  
                                user.first_name=profileform.cleaned_data['name']    
                                user.save()                               #
                                return redirect('home:profileupdate',unique_id=unique_id) #7
                        else:
                            profileform = ProfileUpdate(instance=profile)
                            return render(request,'profile_update.html',{'profileform':profileform})                #8
                else :
                    profileform = ProfileUpdate(instance=profile)                       #9
                    return render(request,'profile_update.html',{'profileform':profileform})#10
       else:
               return redirect('home:home')                                                  #11                                                       #2
    except:
        return redirect('home:home')
                                            #11



@login_required(login_url='login')  
@api_view(['GET','POST'])
@csrf_exempt
def addvisiting(request,unique_id):
    '''
       #1 Verifies that this item already exists  in database 
       #2 exception occure redirect to home page 
       #3 load all visting  to show in page
       #3,4 if visting existis and method post
       #4,6 form takes requset post and check method type ,and valid 
       #7,8,9 try to adding visting ,if exception occure form still empty in page at the end show all visiting image in page 
       #10,11 if item success adding load images show redirect in page contian item added and show form adding in page
        
    '''
    try:
       pro=Profile.objects.get(unique_id=unique_id)
       if pro:      
                visiting_user= getvisitng(request,unique_id)                           #3
                form=VistingForm(request.POST)                                         #4
                if request.method=='POST':                                             #5                                            #    
                        created=date.today()                                                        #7
                        Visiting.objects.create(profile_id=unique_id,created=created) #8
                        visiting_user= getvisitng(request,unique_id)                  #3
                        return render(request,'add_visiting.html',{'formvisting':form,'visting':visiting_user})                       #10
                                                                    #10
                else:
                  return render(request,'add_visiting.html',{'formvisting':form,'visting':visiting_user})  #11
       else:
           return redirect('home:home')                                    #1
    except:
           return redirect('home:home')                                                #2
    
                                  


@login_required(login_url='login')
@api_view(['GET','POST'])
@csrf_exempt
def delete_visitng(request,unique_id):
        '''
        #1 Verifies that this item already exists  in database by uuid
        #2 if exception occure or item not exist redirct home page
        #3 delte visting object
        #4,5 load visitng the same profile and show in add_visting page
        #6 loading page without item deleted   
        '''
        try: 
            item=Visiting.objects.get(unique_id=unique_id)#1
        except:
           return redirect('home:home')                    #2
        else:
            if item:
               prof_id=item.profile_id                     #3
               item.delete()
               form=VistingForm()                           #4
               visiting_user= getvisitng(request,prof_id)   #5   
               return render(request,'add_visiting.html',{'formvisting':form,'visting':visiting_user}) #6 
            else:
               return redirect('home:home')                 #2



@login_required(login_url='login')
@api_view(['GET','POST'])
def uploadimages(request,unique_id):
        '''
       #1 Verifies that this item already exists  in database 
       #2 load all images of visiting to show in page
       #3,4 if visting existis and method post
       #5,6 form takes requset files 
       #7,8,9 try to adding image ,if exception occure form still empty in page at the end show all visiting image in page 
       #10,11 if item success adding load images show redirect in page contian item added and show form adding in page
        
        '''

        try:
            item=Visiting.objects.get(unique_id=unique_id) #1
            img=get_user_image_visiting(unique_id)         #2
        except:
           return redirect('home:home') 
        else:
            if item:                                                       #3
               if request.method=='POST':                                  #4  
                   form = Image_VistingForm(request.POST , request.FILES)  #5
                   files = request.FILES.getlist('img_visiting')           #6
                   if form.is_valid():
                       
                       for f in files:                                      #7
                           try:
                             Image_visiting.objects.create(visiting_id=unique_id,img_visiting=f)
                           except :
                               form = Image_VistingForm()                    #8
                           else:
                               img=get_user_image_visiting(unique_id)         #9
                             
                       img=get_user_image_visiting(unique_id)                 #10
                       return render(request,'upload.html',{'form':form,'img':img}) #11
                   else:
                     form = Image_VistingForm()                                #8
               else:
                   form = Image_VistingForm()                                   #8
                   return render(request,'upload.html',{'form':form,'img':img}) #11      
            else:
                 form = Image_VistingForm()                                      #8
                 return render(request,'upload.html',{'form':form,'img':img})    #11



@api_view(['GET','POST'])
@login_required(login_url='login')                   
def deleteimage(request,unique_id):
        '''
        #1 Verifies that this item already exists  in database by uuid
        #2 if exception occure or item not exist redirct home page
        #3 delte visting object
        #4,5 load image visitng the same visting and show in upload page
        #6 loading page without item deleted 
        ''' 
        try:
            item=Image_visiting.objects.get(unique_id=unique_id)          #1
        except:
           return redirect('home:home')                                    #2                       
        else:
            if item:
               visiting=item.visiting_id                                   #4
               item.delete()
               form=Image_VistingForm()
               img=get_user_image_visiting(visiting)                        #5
               return render(request,'upload.html',{'form':form,'img':img}) #6  
            else:
               return redirect('home:home')                                  #2

'''
rest api 
Get mothed
get all visiting that user login
only user login 
get data by that vsiting.profile_uuid=>profile.user_id=>User.id login uuid 

'''
class ListVisting(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        uuid=request.GET.get('unique_id')

        visting= Visiting.objects.filter(profile_id=uuid).order_by('-created')
        serializers=VisitingSerializers(visting,many=True)
        return Response(serializers.data)


class Img_Visiting(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def get(self,request,format=None):
              unique_id=request.GET.get('unique_id')
              img_visitng=Image_visiting.objects.filter(visiting_id=unique_id)
              serializer=Img_visitingSerializers(img_visitng,many=True)  
              return Response(serializer.data)          