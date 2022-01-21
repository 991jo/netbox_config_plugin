# netbox_config_plugin - A plugin to generate, compare and deploy configurations

This plugin allows you to execute your code to generate a config for a device,
compare it to the current config of that device and replace configuration with
the generated config.


# Status of this Plugin


A basic understanding of python, objects, python modules and the NetBox Django
models is required to install this plugin as you have to provide some code
on your own that will interact with NetBox.

This plugin is in an early development stage.
This features, requirements, UI and workflows of this plugin may change often.
Use at your own risk.
Please report bugs as a Github issue.

All interactions with the device are done with [NAPALM](https://github.com/napalm-automation/napalm)
so this should work with any device supported by NAPALM.
Although currently only IOS-XE is tested.
The general caveats for NAPALM still apply.

# Version compatibility

^ version ^ Netbox < 3.0 ^ Netbox 3.0 ^ NetBox 3.1 ^
| ------- | ------------ | ---------- | ---------- |
| 0.0.1   |              | x          |            |
| 0.0.2   |              |            | x          |

# Things not included in this plugin

You need to provide on your own:

- code for generating configs
- code for wether a device should be configured using this plugin
- code for gathering the required NAPALM connection data like
  - hostnames
  - usernames
  - passwords and secrets
  - further options that might be required

Details regarding those can be found in the config section.

# Installation

First you need to install this python module into your NetBox virtualenv.
For a regular NetBox install this can be done by adding it to the
`local_requirements.txt` file.

```
echo "git+https://github.com/991jo/netbox_config_plugin#egg=netbox_config_plugin" >> /opt/netbox/local_requirements.txt
```

After that you have to add it and the `netbox-plugin-extensions` the netbox
configuration.

```
# /opt/netbox/netbox/netbox/configuraton.py

...

PLUGINS = [
	"netbox_config_plugin",
	"netbox_plugin_extensions"
	]
PLUGINS_CONFIG = {
	"netbox_config_plugin" : {
    default_settings = {"CONFIGJOB_AVAILABLE": <your function here>,
                        "CONFIG_GENERATOR": <your function here>,
                        "CONNECTION_OPTIONS": <your function here>}
	}
}
```

The parts with `<your function here>` needs to be replaced with a python
function. Details on what these functions habe to do can be found in the
"Your own functions" section.

After that you can run the NetBox `upgrade.sh` script to regenerate the venv.
If everything works you have to restart your netbox and netbox-rq services.

# Your own functions

This Plugin relies on 3 pieces of code that you have to provide.
You should be somewhat familiar with the NetBox python models to 

## `CONFIGJOB_AVAILABLE`

This function takes a NetBox device instance and returns `True` when
this device should be configurable by this plugin.

To enable the functionallity for all devices you could just return `True`.

```
def configjob_available(device) -> bool:
    return True
```

But this can be restricted. E.g. to only be able to configure the device with
the name `foo` you could use something like:

```
def configjob_available(device) -> bool:
    return device.name == "foo"
```

Matching on device types, tags, custom fields, and everything else the NetBox
Django Models offer is also possible.

## `CONFIG_GENERATOR`

This is a function that returns a ConfigGenerator object.
This ConfigGenerator object has only one method called `generate_config:

```
# netbox_config_plugin/config_generators.py
class ConfigGenerator(ABC):

    @abstractmethod
    def generate(self, device) -> str:
        """
        Generates a Config for the given Device.
        """
        pass
```

you have to make a function that returns a subclass of that ConfigGenerator.

```

class DummyConfigGenerator(ConfigGenerator):

    def generate(self, device) -> str:
        # here goes the code that generates your config
		return "my fancy config"


def config_generator_wrapper(device):
    """
    Returns a ConfigGenerator Object for a Device.

    Raises a NoConfigGenerator Exception if no config generator is available
    for the Device.
    """

    return DummyConfigGenerator()
```

You could build multiple ConfigGenerator subclasses, e.g. one per vendor,
platform, device type or device role, and depending on the device
return the apropriate one.

## `CONNECTION_OPTIONS`

This function has to return the driver name, and positional and keyword arguments
for the NAPALM Driver.
These are passed directly to the NAPALM Driver.

```
def get_connection_options(device) -> Tuple[str, List, Dict]:
    """
    This function takes the device and returns the required options for
    NAPALM to connect to that device

    The options are:
      - the driver to use (e.g. "ios" or "junos")
      - args and kwargs that are passed to the driver. These depend on the
        driver but usually are:
        - hostname
        - username
        - password
        - timeout (optional)
        - optional_args (optional)
    """
    driver_name = "ios"
    hostname = "2001:db8::42"
    username = "root"
    password = "supersecretpassword"
    args = [hostname, username, password]

    optional_args = {"secret": "supersecretsecret"}
    kwargs = {"optional_args": optional_args}

    return driver_name, args, kwargs
```

Details on the NAPALM Documentation has details on the [Driver](https://napalm.readthedocs.io/en/latest/support/index.html#optional-arguments)
and the [optional arguments](https://napalm.readthedocs.io/en/latest/support/index.html#optional-arguments)

# Job Handling and Job Queues

This plugin uses redis to send jobs to the netbox-rq workers.
Currently all jobs are sent to the default queue so no changes should be
required for a regular NetBox installation.
