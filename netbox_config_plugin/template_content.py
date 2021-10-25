from extras.plugins import PluginTemplateExtension
from .models import ConfigJob
from .tables import ConfigJobDeviceTable

class DeviceConfigJob(PluginTemplateExtension):

    model = 'dcim.device'

    def right_page(self):
        if self.context["config"]["CONFIGJOB_AVAILABLE"](self.context["object"]):
            queryset = ConfigJob.objects.filter(device=self.context["object"])
            previous_jobs = ConfigJobDeviceTable(queryset)

            return self.render("netbox_config_plugin/inc/device_extension.html",
                                {"previous_jobs": previous_jobs})
        else:
            return ""


template_extensions = [DeviceConfigJob]
