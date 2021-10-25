from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib import messages

# from netbox.views import generic
from netbox_plugin_extensions.views import generic

from dcim.models import Device

from .models import ConfigJob
from .forms import ConfigJobForm

from .tables import ConfigJobTable, LogTable
from .config_generators import generate_config, compare_config, deploy_config


class ConfigJobCreateView(View):

    def post(self, request):

        form = ConfigJobForm(request.POST)
        if form.is_valid():
            instance = form.save()

    def get(self, request):

        devices = Device.objects.all()
        device = get_object_or_404(devices, pk=request.GET.get("pk"))
        config_job = ConfigJob(device=device)
        config_job.save()
        return redirect(config_job)


class ConfigJobView(View):

    queryset = ConfigJob.objects.all()

    def get(self, request, pk):
        config_job_object = get_object_or_404(self.queryset, pk=pk)

        def format_log(log) -> LogTable:
            output_log = list()
            for time, severity, message in log:
                output_log.append({"time": time, "severity": severity, "message": message})

            return LogTable(output_log)

        config_log_table = format_log(config_job_object.config_log)
        deployment_log_table = format_log(config_job_object.deployment_log)
        compare_log_table = format_log(config_job_object.compare_log)

        return render(request,
                      "netbox_config_plugin/configjob_view.html",
                      {"object": config_job_object,
                       "config_log_table": config_log_table,
                       "deployment_log_table": deployment_log_table,
                       "compare_log_table": compare_log_table})


class ConfigJobGenerateConfigView(View):

    queryset = ConfigJob.objects.all()

    def post(self, request, pk):
        job_object = get_object_or_404(self.queryset, pk=pk)

        if job_object.config_status in [ConfigJob.JobStatus.RUNNING, ]:
            messages.warning(request, "ConfigJob not in a state where a Config Generation can be started!")
        else:
            generate_config(job_object)

        return redirect(job_object)


class ConfigJobCompareConfigView(View):

    queryset = ConfigJob.objects.all()

    def post(self, request, pk):
        job_object = get_object_or_404(self.queryset, pk=pk)

        if job_object.compare_status in [ConfigJob.JobStatus.RUNNING, ]:
            messages.warning(request, "ConfigJob not in a state where a Config Comparation can be started!")
        else:
            compare_config(job_object)

        return redirect(job_object)

class ConfigJobDeployConfigView(View):

    queryset = ConfigJob.objects.all()

    def post(self, request, pk):
        job_object = get_object_or_404(self.queryset, pk=pk)

        if job_object.deployment_status in [ConfigJob.JobStatus.RUNNING, ]:
            messages.warning(request, "ConfigJob not in a state where a Config Deployment can be started!")
        else:
            print("starting deployment")
            deploy_config(job_object)

        return redirect(job_object)


class ConfigJobListView(generic.PluginObjectListView):
    table = ConfigJobTable
    queryset = ConfigJob.objects.all()
    action_buttons = None
