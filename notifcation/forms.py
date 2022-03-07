from django.forms import ModelForm



from .models import notefication

class NoteficationForm(ModelForm):
    	class Meta:
		      model=notefication	
		      fields=['notfication','content_note','category_note','img_note']		 
            