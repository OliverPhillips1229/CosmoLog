from django.urls import path
from . import views

urlpatterns = [
    # Home/About
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Missions (CBVs)
    path('missions/', views.MissionList.as_view(), name='mission-index'),
    path('missions/create/', views.MissionCreate.as_view(), name='mission-create'),
    path('missions/<int:pk>/', views.MissionDetail.as_view(), name='mission-detail'),
    path('missions/<int:pk>/update/', views.MissionUpdate.as_view(), name='mission-update'),
    path('missions/<int:pk>/delete/', views.MissionDelete.as_view(), name='mission-delete'),

    # Experiments (CBVs)
    path('experiments/', views.ExperimentList.as_view(), name='experiment-index'),
    path('experiments/create/', views.ExperimentCreate.as_view(), name='experiment-create'),
    path('experiments/<int:pk>/', views.ExperimentDetail.as_view(), name='experiment-detail'),
    path('experiments/<int:pk>/update/', views.ExperimentUpdate.as_view(), name='experiment-update'),
    path('experiments/<int:pk>/delete/', views.ExperimentDelete.as_view(), name='experiment-delete'),
]