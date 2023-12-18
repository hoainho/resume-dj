from django.contrib import admin

# Register your models here.
from .models import  UserProfile, ProjectItem, SkillItem, Social, EducationItem

admin.site.register((UserProfile, ProjectItem, SkillItem, Social, EducationItem))