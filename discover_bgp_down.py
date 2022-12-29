from datetime import date
from getpass import getpass

import pynetbox
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from rich import print

username = input("Digite o seu nome de usuario: ")
passwd = getpass("Digite seua senha: ")

today = date.today()
today = today.strftime("%d-%m-%Y")
file = open(f"outputs/BGP-Sessions-Down-{today}.txt", "a+")


nr_config_file = "config.yaml"
command = 'show bgp summary | match "Idle|Active|Connect"'


def nornir_setup():
    nr = InitNornir(config_file=nr_config_file)
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = passwd
    return nr


nr = nornir_setup()
nb = pynetbox.api('http://127.0.0.1:8080', token='token')

devices = nb.dcim.devices.filter(role="core", status="active")

for device in devices:
    # nr = nornir_setup()
    device = str(device)
    rtr = nr.filter(name=device)

    try:
        output = rtr.run(task=netmiko_send_command, command_string=command)
        saida = output[device][0].result

        print(
            f"########### Sessões BGP Dowm para {device} ##################\n")
        print(saida)
        print("\n\n")
        file.write(
            f"########### Sessões BGP Dowm para {device} ##################\n")
        file.write(saida)
        file.write("\n\n")

    except:
        pass
