
from getpass import getpass

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result

username = input("Digite o seu nome de usuario: ")
passwd = getpass("Digite seua senha: ")

router = input("Digite o roteador para coletar as informacoes: ")

nr_config_file = "config.yaml"


def nornir_setup():
    nr = InitNornir(config_file=nr_config_file)
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = passwd
    return nr


nr = nornir_setup()

rtr = nr.filter(name=router)
bgp_neighbor = rtr.run(task=napalm_get, getters=["bgp_neighbors"])
print_result(bgp_neighbor)
