__version__ = "0.0.1"

from extras.plugins import PluginConfig


class NetboxConfigPluginConfig(PluginConfig):
    name = 'netbox_config_plugin'
    verbose_name = 'NetBox Config Plugin'
    description = 'A plugin for generating, comparing and deploying configs to devices',
    version = __version__
    author = 'Johannes Erwerle'
    author_email = 'erwerle@belwue.de'
    base_url = "netbox_config_plugin"
    default_settings = {}
    required_settings = ["CONFIGJOB_AVAILABLE",
                         "CONFIG_GENERATOR",
                         "CONNECTION_OPTIONS"]

config = NetboxConfigPluginConfig
