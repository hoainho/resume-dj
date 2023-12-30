from django.urls import path
from .views import (
    ContactView,
    HomeView,
    ResumeView,
    ProjectView,
)

app_name = 'v1'

urlpatterns = [
    path('<user_name>/', HomeView.as_view(), name='home'),
    path('<user_name>/resume/', ResumeView.as_view(), name='resume'),
    path('<user_name>/projects/', ProjectView.as_view(), name='projects'),
    path(r'<user_name>/contact/', ContactView.as_view(), name='contact'),
]
