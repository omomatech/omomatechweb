from copy import error
from django.http import Http404
from rest_framework.views import APIView
from home.models import *
from accounts.models import *
from notifcation.forms import NoteficationForm
from .serializers import *
from .models import notefication
from django.shortcuts import render
import requests
import json
from random import randint
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from datetime import date
from rest_framework import authentication, permissions
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from rest_framework.decorators import api_view
from accounts.models import *
from home.models import Visiting


def getnote():
            note=notefication.objects.all()
            Serializer=Note_Serializers(note,many=True)  
            data=Serializer.data
            return data
def getcatgory():
    cat=catgorys.objects.all()
    serializers=Catogreys_serializer(cat,many=True)   
    data=serializers.data
    return data         

@login_required(login_url='login')  
@api_view(['GET','POST'])
@csrf_exempt
def note_create(request):
    '''
       #1 Verifies that this item already exists  in database 
       #2 exception occure redirect to home page 
       #3 load all visting  to show in page
       #3,4 if visting existis and method post
       #4,6 form takes requset post and check method type ,and valid 
       #7,8,9 try to adding visting ,if exception occure form still empty in page at the end show all visiting image in page 
       #10,11 if item success adding load images show redirect in page contian item added and show form adding in page
        
    '''
    notefications=getnote
    cat_items=getcatgory                       #3
    form=NoteficationForm()                                         #4
    if request.method=='POST':
                    form=NoteficationForm(request.POST, request.FILES)                                            #5
                    if form.is_valid():                                                  #7
                           img_note = request.FILES.get('img_note')
                           content_note= request.POST.get('content_note')
                           print(content_note)
                           notfication= request.POST.get('notfication')
                           category_note= request.POST.get('category_note')
                           notefication.objects.create(notfication=notfication,content_note=content_note,category_note=category_note,img_note=img_note)
                           notefications=getnote
                           return render(request,'note.html',{'form':form,'note':notefications,'cat_items':cat_items})                       #10   
                    else:
                        form=NoteficationForm(request.POST, request.FILES)
                        return render(request,'note.html',{'form':form,'note':notefications,'cat_items':cat_items})                       #10                                                       #10
    else:
         return render(request,'note.html',{'form':form,'note':notefications,'cat_items':cat_items})  #11
       
def delete_note(request,unique_id):
      form=NoteficationForm()
      notefications=getnote
      cat_items=getcatgory  
      try: 
            item=notefication.objects.get(unique_id=unique_id)#1
      except:
           return render(request,'note.html',{"form":form,'note':notefications,'cat_items':cat_items})                  #2
      else:
            if item:              #3
               item.delete()
               form=NoteficationForm()                          #4
               notefications=getnote                 #3
               return redirect('notifcation:create_note')     
            else:
                notefications=getnote 
                return render(request,'note.html',{"form":form,'note':notefications,'cat_items':cat_items})
def send_notification(registration_ids,title,body,image,type_note):

    fcm_api = "AAAArQcAWAg:APA91bE5VnxK6tdn88TLBXxyJn3GqffHpvdH9BO7rRPYPFIO_E0Voy5YskYL_dwRGF1Ucr3yRRTCoN_MKCWj6ESmEY7nyRYUbriwjOMVzTaoZHeYQAGFKgcYRxFjOhQ__Tq4IsC1-QAo"
    url = "https://fcm.googleapis.com/fcm/send"
    
    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key='+fcm_api}

    payload = {
        "registration_ids" :registration_ids,
        "priority" : "high",
    'notification':{
          "title" : title,
          "body" :body,
              },
    "data" : {
     "type": type_note,   
    "image":image,

    "click_action": "FLUTTER_NOTIFICATION_CLICK",
    "sound": "true", 
    "status": "done",
    
  },
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())

def send_note():
    resgistration = []
    pro=Profile.objects.all()
    for item in pro:
        resgistration.append(item.token_notifcation)
    
    if resgistration:

            count = notefication.objects.filter().count()
            
            if count:
                 note=notefication.objects.filter(expired=False)[randint(0, count - 1)]
                 send_notification(resgistration,note.notfication,note.content_note,str(note.img_note),note.category_note)
                 note.expired=True
                 note.date_sending=datetime.datetime.now()
                 note.save()
            else:
                print("no note avaliable")     
    else:
        print('no person pragnant')

class Notes(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def get(self,request,format=None):
              note=notefication.objects.filter(expired=True)
              serializer=Note_Serializers(note,many=True)
              return Response(serializer.data)   
      
class Noteprivate(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def post(self,request,format=None):
              unique_id=request.POST.get('unique_id')
              note=notefication.objects.filter(unique_id=unique_id)
              serializer=Note_Serializers(note,many=True)  
              return Response(serializer.data)   