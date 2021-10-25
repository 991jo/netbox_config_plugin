from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='netbox_config_plugin',
    version="0.0.1",
    packages=find_packages(),
    url="https://github.com/991jo/netbox_config_plugin",
    author='Johannes Erwerle',
    author_email='erwerle@belwue.de',
    description='A netbox plugin to generate, compare and deploy configs to devices',
    include_package_data=True,
    zip_safe=False,
    long_description=readme,
    install_requires=["napalm", "netbox-plugin-extensions"]
)