"""DDPTP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from experiments.views import *
from demo.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),

    path('experiments/', experiments_view),
    path('experiments/run', run_experiments),

    path('demo/index', demo_index_view),
    path('demo/contract', demo_contract_view),
    path('demo/statlog_contract', statlog_contract_view),
    path('demo/submission', individual_submission_view),
    path('demo/api', demo_api_view),
    path('demo/api/result', api_result),
    path('demo/index/predict', predict),
    path('demo/verification', verification_view),

    path('about/', about_view)
]
