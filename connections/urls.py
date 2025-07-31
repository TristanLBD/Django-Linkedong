from django.urls import path
from . import views

app_name = 'connections'

urlpatterns = [
    path('', views.ConnectionListView.as_view(), name='connection_list'),
    path('search/', views.SearchUsersView.as_view(), name='search_users'),
    path('profile/<int:user_id>/', views.UserProfileView.as_view(), name='user_profile'),
    # Actions sur les connexions
    path('send/<int:user_id>/', views.SendConnectionRequestView.as_view(), name='send_connection_request'),
    path('accept/<int:connection_id>/', views.AcceptConnectionView.as_view(), name='accept_connection'),
    path('reject/<int:connection_id>/', views.RejectConnectionView.as_view(), name='reject_connection'),
    path('cancel/<int:connection_id>/', views.CancelConnectionRequestView.as_view(), name='cancel_connection_request'),
    path('remove/<int:connection_id>/', views.RemoveConnectionView.as_view(), name='remove_connection'),
]
