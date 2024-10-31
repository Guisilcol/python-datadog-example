from typing import Literal, TypedDict, Optional

class Tags(TypedDict):
    """
    Representa um dicionário tipado para armazenar metadados de uma aplicação,
    incluindo informações obrigatórias e opcionais de configuração.

    Atributos:
        - sigla (str): Sigla obrigatória para identificação do projeto (ex.: 'ln6', 'ec3').
        - cloud_provider (str): Provedor de nuvem, obrigatório quando datacenter não é especificado (ex.: 'aws', 'gcp', 'azure').
        - datacenter (str): Data center físico, obrigatório quando cloud_provider não é especificado (ex.: 'ctmm1', 'ctsp').
        - condominio (str): Condominio da aplicação, obrigatório (ex.: 'devops', 'tradops', 'paas').
        - account_id (str): ID da conta, obrigatório (ex.: '123456789012').
        - environment (str): Ambiente da aplicação, obrigatório (ex.: 'dev', 'hom', 'prod').
        - version (str): Versão da aplicação, obrigatório (ex.: '1.0.0').
        - service (str): Nome do serviço, obrigatório e deve seguir o formato <SIGLA>-<APP-NOME> (ex.: 'dy5-envio-pix', 'ep9-consulta-saldo').
        - produto (str): Produto da aplicação, obrigatório (ex.: 'Open Finance', 'Pix').
        - jornada (str): Jornada da aplicação, obrigatório (ex.: 'Jornada de Confirmação', 'Jornada de Consumo').
        - repo_url (Optional[str]): URL do repositório, obrigatório quando cloud_provider for 'aws' ou condominio for 'devops' ou 'tradops' (ex.: 'https://github.com/itau-corp/app').
        - subjornada (Optional[str]): Subjornada, opcional mas recomendada (ex.: 'Validação da leitura do QRCode no Pix').
        - sigla_app (Optional[str]): Sigla da aplicação, opcional.
    """
    sigla: str
    cloud_provider: Optional[Literal['aws', 'gcp', 'azure']]
    datacenter: Optional[Literal['ctmm1', 'ctsp']]
    condominio: Literal['devops', 'tradops', 'paas'] 
    account_id: str
    environment: Literal['dev', 'hom', 'prod']
    version: str
    service: str
    produto: str 
    jornada: str
    repo_url: Optional[str]
    subjornada: Optional[str]
    sigla_app: Optional[str]