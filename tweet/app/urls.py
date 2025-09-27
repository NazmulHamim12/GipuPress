
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("",views.sing_up_page,name='sing_up'),
    path("log/",views.login,name='login'),
    path('profile/<int:user_id>/', views.profile_page, name="profile"),
    path('logout/', views.logout_view, name="logout"),
    path('reset/', views.reset, name="reset"),
    path('reset_done/', views.reset_done, name="reset_done"),
    path('explore/', views.post_list, name="explore"),
    path("create_post/<int:user_id>/", views.create_post, name="create_post"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("update_post/<int:post_id>/", views.update_post, name="update_post"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
    path('u_profile/<int:user_id>/', views.use_pro, name="use_pro"),

    
    
]
