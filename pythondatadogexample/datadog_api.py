from typing import Optional
from datadog_api_client.v2 import Configuration, ApiClient
from datadog_api_client.v2.models import HTTPLog, HTTPLogItem
from datadog_api_client.v2.api.logs_api import LogsApi


class ConfigurationFactory:
    """Fábrica para criar instâncias de Configuration para a API Datadog."""

    def create(self, api_key: str, app_key: Optional[str] = None, site: Optional[str] = None) -> Configuration:
        """
        Cria uma configuração para a API Datadog com as chaves de autenticação e variáveis de servidor.

        Parâmetros:
            api_key (str): Chave de API para autenticação.
            app_key (Optional[str]): Chave de aplicação, opcional.
            site (Optional[str]): Domínio do site Datadog (ex.: 'datadoghq.com').

        Retorna:
            Configuration: Instância de Configuration com autenticação e configuração de site.
        """
        keys = {'apiKeyAuth': api_key, 'appKeyAuth': app_key}
        server_variables = {"site": site}
        
        return Configuration(api_key=keys, server_variables=server_variables)


class ApiClientFactory:
    """Fábrica para criar instâncias de ApiClient com uma configuração especificada."""

    def create(self, configuration: Configuration) -> ApiClient:
        """
        Cria um cliente de API utilizando a configuração fornecida.

        Parâmetros:
            configuration (Configuration): Configuração para o cliente de API.

        Retorna:
            ApiClient: Instância de ApiClient configurada para comunicação com a API Datadog.
        """
        return ApiClient(configuration)


class HTTPLogFactory:
    """Fábrica para criar logs HTTP no formato esperado pela API Datadog."""

    def create(self, ddsource: str, ddtags: str, message: str, service: str) -> HTTPLog:
        """
        Cria um log HTTP com a estrutura necessária para o Datadog.

        Parâmetros:
            ddsource (str): Fonte do log no Datadog.
            ddtags (str): Tags adicionais para o log.
            message (str): Mensagem do log.
            service (str): Nome do serviço de onde o log foi gerado.

        Retorna:
            HTTPLog: Instância de HTTPLog configurada para envio ao Datadog.
        """
        return HTTPLog([HTTPLogItem(ddsource=ddsource, ddtags=ddtags, message=message, service=service)])


class LogsApiFactory:
    """Fábrica para criar instâncias de LogsApi usando um cliente de API."""

    def create(self, api_client: ApiClient) -> LogsApi:
        """
        Cria uma instância de LogsApi utilizando o cliente de API fornecido.

        Parâmetros:
            api_client (ApiClient): Cliente de API para comunicação com o Datadog.

        Retorna:
            LogsApi: Instância de LogsApi pronta para enviar logs ao Datadog.
        """
        return LogsApi(api_client)
