from enum import unique
import re
from django.http import response
from django.shortcuts import render
import datetime
from rest_framework import authentication, permissions
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import Profile
from reservation.serializer import *
from reservation.forms import  ReservationFrom
from reservation.models import Reservation, time_reservations
def getitemstimes(date_reservation):
     
     return Reservation.objects.filter(date_reservation=date_reservation)
     
              
def gettimes(date_reservation):
     items=[]
     times=Reservation.objects.filter(date_reservation=date_reservation)
     if times:
            
         for item in times:
             items.append(str(item.time_reservation))
      
         q= time_reservations.objects.all()
         q1=q.exclude(time_reservation_part__in=items)
         
         return q1
     else:
        q= time_reservations.objects.all()      

        return q
    
 
           

def getlistdayreservation(request):
      today=datetime.date.today().strftime('%Y-%m-%d')
      list_reservation_done=[]
      profile=Profile.objects.all()
      form=ReservationFrom()
      list_times_empty=[]
      date_reservation=request.POST.get('date_reservation')
      reslist=getitemstimes(date_reservation=date_reservation)
      if date_reservation is None:
            date_reservation=today
            reslist=getitemstimes(date_reservation=date_reservation)
      if reslist:
            list_reservation_done=reslist
            list_times_empty=gettimes(date_reservation=date_reservation)
      else:   
            list_reservation_done=[]  
            list_times_empty=gettimes(date_reservation=date_reservation)      
            reslist=getitemstimes(date_reservation=date_reservation)
      if request.method=='POST':  
         if request.POST.get('form_type')=='list':
            if reslist:
                  list_reservation_done=reslist
                  list_times_empty=gettimes(date_reservation=date_reservation)
                  return render(request,'reservation.html',{'form':form,"list_reservation_done":list_reservation_done,'list_times_empty':list_times_empty,'today':date_reservation,'profile':profile})
            else:   
                  list_reservation_done=[]  
                  list_times_empty=gettimes(date_reservation=date_reservation)
                  print(str(list_times_empty))
                  return render(request,'reservation.html',{'form':form,"list_reservation_done":list_reservation_done,'list_times_empty':list_times_empty,'today':date_reservation,'profile':profile})  
         if request.POST.get('form_type')=='create':
               
               if form.is_valid:
                  print(str(list_times_empty))  
                  time=request.POST.get('time')
                  date=request.POST.get('date')      
                  pro=request.POST.get('profile')
                  
                  Reservation.objects.create(profile_id=pro,date_reservation=date,time_reservation=time)
                  reslist=getitemstimes(date_reservation=date)
                  if reslist:
                      list_reservation_done=reslist
                  list_times_empty=gettimes(date_reservation=date)
                  date_reservation=date
                  print(str(list_times_empty))
                  return render(request,'reservation.html',{'form':form,"list_reservation_done":list_reservation_done,'list_times_empty':list_times_empty,'today':date_reservation,'profile':profile})
               else:   
                  list_reservation_done=[]  
                  list_times_empty=gettimes(date_reservation=date_reservation)
                  print(str(list_times_empty))
                  return render(request,'reservation.html',{'form':form,"list_reservation_done":list_reservation_done,'list_times_empty':list_times_empty,'today':date_reservation,'profile':profile})  
      return render(request,'reservation.html',{'form':form,"list_reservation_done":list_reservation_done,'list_times_empty':list_times_empty,'today':date_reservation,'profile':profile})  
class create_reservation(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def post(self,request,format=None):
         time=request.POST.get('time')
         date=request.POST.get('date')      
         pro=request.POST.get('profile')
         try:        
            Reservation.objects.create(profile_id=pro,date_reservation=date,time_reservation=time)
            return Response('saved successfully')
         except Exception as e:      
            return Response(e)
              
                  
class reservation_list(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,format=None):
            today=datetime.date.today().strftime('%Y-%m-%d')
            date_reservation=request.POST.get('date_reservation')
            if date_reservation is None:
                  date_reservation=today  
            list_times_empty=gettimes(date_reservation=date_reservation)
            serializer=ReservationSerializers(list_times_empty,many=True)
            return Response(serializer.data)
      
                 