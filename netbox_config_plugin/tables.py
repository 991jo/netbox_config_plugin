from utilities.tables import BaseTable
from django.utils.html import format_html

import django_tables2 as tables

from .models import ConfigJob


class ConfigJobTable(BaseTable):

    pk = tables.LinkColumn()
    device = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = ConfigJob
        fields = ["pk",
                  "device",
                  "config_status",
                  "compare_status",
                  "deployment_status"]


class ConfigJobDeviceTable(BaseTable):
    pk = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = ConfigJob
        fields = ["pk",
                  "config_status",
                  "compare_status",
                  "deployment_status"]


class LogTable(tables.Table):

    class LogColumn(tables.Column):
        def render(self, value):
            badges = (
                      ("bg-light", "Debug"),
                      ("bg-info", "Info"),
                      ("bg-warning", "Warning"),
                      ("bg-danger", "Error"),
                      ("bg-black", "Critical"),
                      )

            style = badges[int(value)][0]
            text = badges[int(value)][1]

            return format_html("<span class=\"badge {}\">{}</span>", style, text)

    time = tables.Column()
    severity = LogColumn()
    message = tables.Column()



    class Meta():
        fields = ["time",
                  "severity",
                  "message"]
