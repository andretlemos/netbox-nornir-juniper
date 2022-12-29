# netbox-nornir-juniper

Repositório com arquivos utilizando Nornir e Netbox para Equipamentos Juniper


# Instalação
- pip3 install -r requirements.txt

# Configurações

- É necessário editar o arquivo config.yaml com informações do seu netbox.
- E em alguns arquivos é necessário incluir seu token para utilizar o pynetbox.
    nb = pynetbox.api('http://127.0.0.1:8080', token='token')

