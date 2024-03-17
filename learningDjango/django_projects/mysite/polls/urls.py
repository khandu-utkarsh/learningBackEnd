from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),                                        #Example is /polls/
    path("<int:question_id>/", views.detail, name="detail"),                    #Example is /polls/5/
    path("<int:question_id>/results/", views.results, name="results"),           #Example is /polls/5/results/
    path("<int:question_id>/vote/", views.vote, name="vote"),                   #Example is /polls/5/vote/
]