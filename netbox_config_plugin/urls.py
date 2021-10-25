from django.urls import path

from .views import ConfigJobView, ConfigJobListView, ConfigJobGenerateConfigView, ConfigJobCompareConfigView, ConfigJobCreateView, ConfigJobDeployConfigView

urlpatterns = [
        path("config-job/<int:pk>", ConfigJobView.as_view(), name="configjob"),
        path("config-job/<int:pk>/generate_config", ConfigJobGenerateConfigView.as_view(), name="configjob_generate_config"),
        path("config-job/<int:pk>/compare_config", ConfigJobCompareConfigView.as_view(), name="configjob_compare_config"),
        path("config-job/<int:pk>/deploy_config", ConfigJobDeployConfigView.as_view(), name="configjob_deploy_config"),
        path("config-job", ConfigJobListView.as_view(), name="configjob_list"),
        path("config-job/create", ConfigJobCreateView.as_view(), name="configjob_create"),
    ]
