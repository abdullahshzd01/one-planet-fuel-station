from django.urls import path, register_converter
from . import converts, views

from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views

register_converter(converts.FloatUrlParameterConverter, 'float')

urlpatterns = [
    path('', views.site),
    path('index/', views.site),
    path('demo/', views.demo),
    path('FuelStation/<int:station_id>/', views.fuelStation_view),
    path('StationList/', views.fuelStationList_view),
    # path('Products/', views.products_view),
    path('Products/<int:station_id>/', views.products2_view),
    path('Reviews/', views.reviews_view),
    path('ContactUs/', views.contactUs_view),
    path('AboutUs/', views.aboutUs_view),
    path('LogIn/', views.LogIn_view, name="login"),
    path('Register/', views.Register_view, name="register"),
    path('AuthenticateUser/', views.RegisterVerify_view, name="authentication"),
    # path('Register/', auth_views.Register_view.as_view(), name="register"),
    path('Careers/', views.Careers_view),
    path('AddProducts/<int:station_id>/', views.addProduct_view, name="add_products"),
    path('Post-A-Job/<int:station_id>/', views.PostJobs_view, name="post_jobs"),
    path('Check-Out/<int:station_id>/<float:amount>/', views.CheckOut_view, name="check_out"),
    path('Job-Apply/', views.JobApply_view, name="job_apply"),
    path('myAdmin/', views.AdminLogin),
    path('myAdmin/Register/', views.AdminRegistration),
    path('myAdmin/dashboard/', views.AdminSite),
    path('myAdmin/dashboard/<str:table_name>/', views.AdminSiteDetails, name='AdminSiteDetails'),
    path('myAdmin/dashboard/<str:table_name>/<str:action>/<int:data_id>/', views.AdminSiteAction, name='AdminSiteAction'),
    path('test_fb/', views.fireBase_test),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)