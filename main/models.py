from django.db import models
from datetime import date, datetime
from django.db import models


class Users_manager(models.Manager):
    def basic_validator(self, post_data):
        errors ={}
        #today = date.today()

        if len(post_data['name']) < 4:
            errors["name"] = "Name should have at least 4 characters"
        
        if len(post_data['email']) < 4:
            errors["email"] = "Email should have at least 4 characters"
        
        if len(post_data['password']) < 6:
            errors['password'] = 'Password should have at least 6 characters'
        
        if post_data['password']!= post_data['password_confirm']:
            errors['password'] = 'Passwords do not match'
        
        
        return errors
    
'''
class text_manager(models.Manager):
    def basic_validator(self, post_data):
        errors ={}
        #today = date.today()

        if len(post_data['message']) < 4:
            errors["message"] = "Please, the text should have at least 4 characters"
        
        
        return errors
'''


class Users(models.Model):
    name = models.CharField(max_length= 255, unique= True)
    email = models.EmailField(max_length = 50, unique= True)
    password  = models.CharField(max_length= 14, unique = True)
    allowed = models.BooleanField(default =True)
    avatar = models.URLField(
        default='https://cdn.icon-icons.com/icons2/1879/PNG/512/iconfinder-3-avatar-2754579_120516.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followeds = models.ManyToManyField('Users', related_name= 'followers')
    objects = Users_manager()
    


class textmessages(models.Model):
    message = models.TextField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Users, related_name="msns", on_delete = models.CASCADE)

    

class comments(models.Model):
    comment = models.TextField(max_length= 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(textmessages, related_name="comments", on_delete = models.CASCADE)
    user = models.ForeignKey(Users, related_name="comments", on_delete = models.CASCADE)



