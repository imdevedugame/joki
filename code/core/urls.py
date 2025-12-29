from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # 🏠 Home
    path('', views.home_view, name='home'),

    # 🌸 Profiling Silk wrapper
    path('profiling/', views.silk_wrapper_view, name='profiling'),

    # 📊 Statistik Course (HTML)
    path('courses/stat/', views.course_stat_view, name='course_stat'),

    # 📊 Statistik User (HTML)
    path('users/stat/', views.user_stat_view, name='user_stat'),

    # 📘 Detail Course (HTML)
    path('courses/<int:course_id>/', views.course_detail_view, name='course_detail'),

    # 👥 Daftar User dari REST API (HTML)
    path('users/list/', views.user_list_view, name='user_list_view'),

    # 🧪 API Course Explorer (Pertemuan 10)
    path('tugas-10/', views.tugas_10_view, name='tugas_10'),
]
