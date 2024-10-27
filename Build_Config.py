from distutils.command.config import config
from re import template
import yaml
from jinja2 import Environment, FileSystemLoader
from rich import print as r_print
from inventory import INVENTORY
from netmiko import ConnectHandler


#Test for Jinja
def fun_send_config(device, config):

    net_connect = ConnectHandler(
        device_type=device["device_type"],
        host=device["host"],
        username=device["username"],
        password=device["password"],
        port=device["port"]

    )

    # print(net_connect.find_prompt())
    # list_config=config.splitlines()
    # print(config)
    list_config = config.splitlines()
    output=net_connect.send_config_set(list_config)
    # print(output)



def fun_generate_config(hostname):
    """
    
    """
    file_data_yaml=yaml.safe_load(open(f"host_variable/{hostname}.yaml"))
    r_print(file_data_yaml)
    env_obj = Environment(loader=FileSystemLoader("./jinja_templates"),trim_blocks=True,lstrip_blocks=True)
    template_var=env_obj.get_template("cisco_config_template.j2")
    config = template_var.render(file_data_yaml)
    r_print(type(config))
    with open('config_DB','a') as file:
        file.write(config)
    return config

def main():
    """
    main function
    """
    for each_device in INVENTORY:
        config=fun_generate_config(each_device["hostname"])
        fun_send_config(each_device, config)



main()
