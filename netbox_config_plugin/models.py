from datetime import datetime

from django.db import models
from django.urls import reverse

from dcim.models import Device

from netbox_plugin_extensions.querysets import PluginRestrictedQuerySet

from netbox_plugin_extensions.models import PluginChangeLoggedModel


class ConfigJob(PluginChangeLoggedModel):

    class JobStatus(models.TextChoices):
        NOT_STARTED = 0, "Not started"
        RUNNING = 1, "Running"
        COMPLETED = 2, "Completed"
        FAILED = 3, "Failed"

    class LoggingSeverities(models.TextChoices):
        DEBUG = 0, "Debug"
        INFO = 1, "Info"
        WARNING = 2, "Warning"
        ERROR = 3, "Error"
        CRITICAL = 4, "Critical"

    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    config_status = models.CharField(choices=JobStatus.choices,
                                     default=JobStatus.NOT_STARTED,
                                     max_length=20)
    config_log = models.JSONField(default=list, blank=True)
    config = models.TextField(blank=True)

    compare_status = models.CharField(choices=JobStatus.choices,
                                      default=JobStatus.NOT_STARTED,
                                      max_length=20)
    compare_log = models.JSONField(default=list, blank=True)
    diff = models.TextField(blank=True)

    deployment_status = models.CharField(choices=JobStatus.choices,
                                         default=JobStatus.NOT_STARTED,
                                         max_length=20)
    deployment_log = models.JSONField(default=list, blank=True)

    objects = PluginRestrictedQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("plugins:netbox_config_plugin:configjob",
                       kwargs={"pk": self.pk})

    def log_message(self, log: models.JSONField, severity, message: str):
        """
        Appends a message to the given log.
        """
        time = datetime.now().isoformat()

        log_entry = (time, severity, str(message))

        log.append(log_entry)

    # Logging Function shortcuts

    def log_config_debug(self, message):
        self.log_message(self.config_log, self.LoggingSeverities.DEBUG, message)

    def log_config_info(self, message):
        self.log_message(self.config_log, self.LoggingSeverities.INFO, message)

    def log_config_warning(self, message):
        self.log_message(self.config_log, self.LoggingSeverities.WARNING, message)

    def log_config_error(self, message):
        self.log_message(self.config_log, self.LoggingSeverities.ERROR, message)

    def log_config_critical(self, message):
        self.log_message(self.config_log, self.LoggingSeverities.CRITICAL, message)

    def log_compare_debug(self, message):
        self.log_message(self.compare_log, self.LoggingSeverities.DEBUG, message)

    def log_compare_info(self, message):
        self.log_message(self.compare_log, self.LoggingSeverities.INFO, message)

    def log_compare_warning(self, message):
        self.log_message(self.compare_log, self.LoggingSeverities.WARNING, message)

    def log_compare_error(self, message):
        self.log_message(self.compare_log, self.LoggingSeverities.ERROR, message)

    def log_compare_critical(self, message):
        self.log_message(self.compare_log, self.LoggingSeverities.CRITICAL, message)

    def log_deployment_debug(self, message):
        self.log_message(self.deployment_log, self.LoggingSeverities.DEBUG, message)

    def log_deployment_info(self, message):
        self.log_message(self.deployment_log, self.LoggingSeverities.INFO, message)

    def log_deployment_warning(self, message):
        self.log_message(self.deployment_log, self.LoggingSeverities.WARNING, message)

    def log_deployment_error(self, message):
        self.log_message(self.deployment_log, self.LoggingSeverities.ERROR, message)

    def log_deployment_critical(self, message):
        self.log_message(self.deployment_log, self.LoggingSeverities.CRITICAL, message)
