from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializer import ProfileSerializers
from .forms import CreateUserForm
from django.contrib.auth import views as views_auth
from django.contrib.auth import logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
'''
cancle
signup to create admin 

'''
def signup(request):
    if request.method=='POST':
     
        form=CreateUserForm(request.POST)
        
        if form.is_valid():
             form.save()
             return redirect('login')
        else:
            form=CreateUserForm(request.POST)     
    else:
        form=CreateUserForm() 

    return render(request,'registration/signup.html',{'form':form})  



class LoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        token_notifcation=request.data['token_notifcation']
         
        user = serializer.validated_data['user']
        profile=Profile.objects.get(user_id=user.id)
        profile.token_notifcation=token_notifcation
        profile.save()
        ser=ProfileSerializers(profile)
        token, created = Token.objects.get_or_create(user=user)
        data={
            'unique_id': ser.data['unique_id'],
            'username':ser.data['mobile'],
            'name':ser.data['name'],
            'token': token.key,
           # 'is_pregnant':ser.data['is_pregnant'],
           # 'date_pregnant':ser.data['date_pregnant'],
           # 'number_week_pregnant':ser.data['number_week_pregnant'],
            'updated':ser.data['updated'],
            'token_notifcation':token_notifcation
        }
        return Response(data=data)

class custom_logout(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated] 
    def post(self,request,format=None):
        user=logout(request)
        data={'logout':'true'}
        return Response(data=data)