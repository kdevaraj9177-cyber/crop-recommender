"""crop_recommender_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from Remote_User import views
from Service_Provider import views as serviceprovider

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login, name='login'),
    path('Register1/', views.Register1, name='Register1'),
    path('Recommend_Crop/', views.Recommend_Crop, name='Recommend_Crop'),
    path('ViewYourProfile/', views.ViewYourProfile, name='ViewYourProfile'),
    path(
    'Predict_Crop_Yiled_OnDataSets/',
    views.Predict_Crop_Yiled_OnDataSets,
    name='Predict_Crop_Yiled_OnDataSets'
),
path(
        'View_Remote_Users/',
        serviceprovider.View_Remote_Users,
        name='View_Remote_Users'
    ),
     path(
        'serviceproviderlogin/',
        serviceprovider.serviceproviderlogin,
        name='serviceproviderlogin'
    ),

    

]


urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATICFILES_DIRS[0]
)



