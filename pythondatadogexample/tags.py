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
        - correlationId (str): ID de correlação, obrigatório (ex.: '123e4567-e89b-12d3-a456-426614174000').
        - repo_url (Optional[str]): URL do repositório, obrigatório quando cloud_provider for 'aws' ou condominio for 'devops' ou 'tradops' (ex.: 'https://github.com/itau-corp/app').
        - subjornada (Optional[str]): Subjornada, opcional mas recomendada (ex.: 'Validação da leitura do QRCode no Pix').
        - sigla_app (Optional[str]): Sigla da aplicação, opcional.
        - ddsource (Optional[str]): Fonte do log no Datadog. Geralemente é a tecnologia utilizada. Opcional.
        - hostname (Optional[str]): Nome do host onde o log é gerado. Opcional.
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
    subjornada: Optional[str]
    correlationId: str
    repo_url: Optional[str]
    sigla_app: Optional[str]
    ddsource: Optional[str]
    hostname: Optional[str]

class TagsValidator:
    def validate(self, tags: Tags):
        """
        Valida os atributos de um dicionário de metadados de uma aplicação.

        Parâmetros:
            - tags (Tags): Dicionário de metadados a ser validado.

        Exceções:
            - ValueError: Se algum atributo obrigatório não for informado.
            - ValueError: Se cloud_provider e datacenter forem informados ao mesmo tempo.
            - ValueError: Se cloud_provider e datacenter não forem informados.
        """
        if not tags.get('sigla'):
            raise ValueError('A sigla do projeto é obrigatória')

        if not tags.get('cloud_provider') and not tags.get('datacenter'):
            raise ValueError('É necessário informar o provedor de nuvem ou o datacenter')

        if tags.get('cloud_provider') and tags.get('datacenter'):
            raise ValueError('Não é possível informar o provedor de nuvem e o datacenter ao mesmo tempo')

        if not tags.get('condominio'):
            raise ValueError('O condomínio da aplicação é obrigatório')

        if not tags.get('account_id'):
            raise ValueError('O ID da conta é obrigatório')

        if not tags.get('environment'):
            raise ValueError('O ambiente da aplicação é obrigatório')

        if not tags.get('version'):
            raise ValueError('A versão da aplicação é obrigatória')

        if not tags.get('service'):
            raise ValueError('O nome do serviço é obrigatório')

        if not tags.get('produto'):
            raise ValueError('O produto da aplicação é obrigatório')

        if not tags.get('jornada'):
            raise ValueError('A jornada da aplicação é obrigatória')

        if not tags.get('correlationId'):
            raise ValueError('O ID de correlação é obrigatório')

        if tags.get('cloud_provider') == 'aws' or tags.get('condominio') in ['devops', 'tradops']:
            if not tags.get('repo_url'):
                raise ValueError('A URL do repositório é obrigatória')

        return True