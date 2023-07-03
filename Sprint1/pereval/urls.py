from django.urls import path
from .views import PerevalList, submit_data, get_data, update_data, AuthEmailPerevalAPI, get_email

urlpatterns = [
    path('submitData/', PerevalList.as_view(), name='pereval_list'),
    path('submitData/create/', submit_data, name='submit_data'),

    path('api/submitData/<int:pk>/', get_data, name='get_data'),
    path('api/submitData/<int:pk>/update/', update_data, name='update_data'),
    path('submitData/user__email=<str:email>', AuthEmailPerevalAPI.as_view({'get': 'list'}))
]
