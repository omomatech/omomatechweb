import uuid
from django.db import models
from datetime import datetime, timezone


'''
model notifaction upload image to folder of week
contain artical of week 


'''

def impage_upload(instance,filename):
        imagename,extension=filename.split(".")
        return 'image_note/%s/%s.%s'%(str(instance.category_note),str(imagename),str(extension))

class catgorys(models.Model):
      unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
      category_name=models.CharField(max_length=50,null=False,blank=False,default='no catgory',unique=True)   
      created=models.DateTimeField(auto_now_add=True)
      updated=models.DateTimeField(auto_now=True)
      def __str__(self):
          return self.category_name
      class Meta:
              ordering = ['category_name']  
              
                
class notefication(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    notfication=models.CharField(max_length=200,null=True,blank=True)    
    content_note=models.TextField(max_length=9999,null=True,blank=True)
    category_note=models.CharField(max_length=100, default='no categroy')
    img_note= models.ImageField(upload_to=impage_upload)
    expired=models.BooleanField(default=False)
    date_sending=models.DateTimeField(default=datetime.now(),blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    def __str__(self):
            return "notefication cat"+str(self.category_note)
    
    class Meta:
          ordering = ['notfication']
    
    
    
    
   