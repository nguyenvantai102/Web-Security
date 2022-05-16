from django.urls import path
from quiz import views

urlpatterns = [
 
    path('quiz', views.result, name='quiz'),
    path('addQuestion', views.addQuestion, name='addQuestion'),

    
]