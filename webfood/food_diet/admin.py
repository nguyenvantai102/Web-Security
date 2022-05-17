from django.contrib import admin
from .models import Blog, Diet, Feedback, Comment

# Register your models here.
admin.site.register(Blog)
admin.site.register(Diet)
admin.site.register(Feedback)
admin.site.register(Comment)