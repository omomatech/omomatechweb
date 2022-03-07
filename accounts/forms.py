from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from home.models import Visiting
from home.models import Image_visiting

from .models import Profile


'''
form to create User admin ### not used in code

'''
class CreateUserForm(UserCreationForm):
    	
	class Meta:
    		
		    model = User
		    fields = ['username', 'first_name', 'password1', 'password2']
'''
form to create profile by name and mobile 
that first create user [username=mobile,first_name=name,password =auto generated]
'''
class CreateProfileForm(ModelForm):
        class Meta:
	        model = Profile
	        fields = ['mobile', 'name']
'''
profile update if user is pregnant and number week pregnant
and update mobile name add about 
'''
class ProfileUpdate(ModelForm):
	 class Meta:
		 model=Profile
		 fields= ['mobile','name','about'] 
'''
form create visiting by date only and profile uuid added auto
'''		 		
class VistingForm(ModelForm):
    	class Meta:
		    model=Visiting	
		    fields=['created']
'''
form create image of visiting input file mulitple max 4
 image and if you select >4 that save first selected
'''			
class Image_VistingForm(ModelForm):
    	class Meta:
		    model=Image_visiting	
		    fields=['img_visiting']				 
