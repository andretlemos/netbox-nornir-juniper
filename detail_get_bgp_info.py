from datetime import date
from getpass import getpass

import pynetbox
from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get

today = date.today()
today = today.strftime("%d-%m-%Y")
file = open(f"outputs/BGP-Sessions-Down-{today}.txt", "a+")

username = input("Digite o seu nome de usuario: ")
passwd = getpass("Digite seua senha: ")

# router = input("Digite o roteador para coletar as informacoes: ")

nr_config_file = "config.yaml"


def nornir_setup():
    nr = InitNornir(config_file=nr_config_file)
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = passwd
    return nr


nr = nornir_setup()

nb = pynetbox.api('http://127.0.0.1:8080',
                  token='seu token')

devices = nb.dcim.devices.filter(role="core", status="active")

for device in devices:  # nr = nornir_setup()
    device = str(device)
    rtr = nr.filter(name=device)

    try:
        bgp_neighbor = rtr.run(task=napalm_get, getters=["bgp_neighbors"])
        result = bgp_neighbor[device][0].result

        print(
            f"########### Sessões BGP Dowm para {device} ##################\n")
        file.write(
            f"########### Sessões BGP Dowm para {device} ##################\n")
        print("Peer - ASN - Description\n")
        file.write("Peer - ASN - Description\n")

        for peer in result["bgp_neighbors"]["global"]["peers"]:
            active = result["bgp_neighbors"]["global"]["peers"][peer]["is_up"]

            if active != True:
                asn = result["bgp_neighbors"]["global"]["peers"][peer]["remote_as"]
                description = result["bgp_neighbors"]["global"]["peers"][peer]["description"]
                print(f"{peer} - {asn} - ({description})\n")
                file.write(f"{peer} - {asn} - ({description})\n")
    except:
        pass
