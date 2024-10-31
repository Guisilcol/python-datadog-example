from typing import Literal, Optional
from logging import Logger
from pythondatadogexample.datadog_api import (
    HTTPLogFactory, 
    LogsApiFactory, 
    ConfigurationFactory, 
    ApiClientFactory
)
from pythondatadogexample.formatter import FormatterFactory
from pythondatadogexample.handler import LogHandlerFactory, PossibleLevels
from pythondatadogexample.logger import LoggerFactory
from pythondatadogexample.tags import Tags

def get_datadog_logger(
    tags: Tags,
    data_dog_handler_level: PossibleLevels = 'WARNING',
    console_handler_level: PossibleLevels = 'DEBUG',
    api_key: str = '',
    app_key: str = '',
    site: str = 'datadoghq.com',
    logger_name: str = 'datadog_logger',
    raise_on_error: bool = False
) -> Logger:
    """
    Cria e configura um logger para envio de logs ao Datadog com um handler para console.
    Somente logs de nível WARNING, ERROR, e CRITICAL são enviados ao Datadog por padrão, enquanto todos os logs são enviados ao console.

    Parâmetros:
        - service_name (str): Nome do serviço ao qual o log pertence.
        - ddsource (str): Fonte do log no Datadog.
        - acronym (str): Acrônimo do projeto/serviço.
        - job_name (str, opcional): Nome do job em execução.
        - job_run_id (str, opcional): ID de execução do job.
        - hostname (str, opcional): Nome do host onde o log é gerado.
        - environment (str, opcional): Ambiente do sistema (ex.: produção, desenvolvimento).
        - api_key (str, opcional): Chave de API do Datadog.
        - app_key (str, opcional): Chave de aplicação do Datadog.
        - logger_name (str, opcional): Nome do logger. Padrão é 'datadog_logger'.
        - site (str, opcional): Site do Datadog (ex.: 'datadoghq.com').
        - raise_on_error (bool, opcional): Indica se exceções devem ser levantadas em caso de erro de envio de log. Padrão é False.

    Retorna:
        Logger: Instância de logging.Logger configurada com handlers para Datadog e console.
    """
    
    # Cria o formatter JSON
    formatter = FormatterFactory().create_json_formatter(tags)

    # Configuração da API Datadog e criação de cliente e API
    datadog_api_configuration = ConfigurationFactory().create(api_key, app_key, site)
    api_client = ApiClientFactory().create(datadog_api_configuration)
    logs_api = LogsApiFactory().create(api_client)

    # Criação dos handlers para envio dos logs ao Datadog e console.
    log_factory = HTTPLogFactory()
    datadog_handler = LogHandlerFactory().create_datadog_handler(
        tags, logs_api, log_factory, data_dog_handler_level, formatter, raise_on_error
    ) 
    console_handler = LogHandlerFactory().create_console_handler(console_handler_level, formatter)

    # Criação do logger com os handlers configurados.
    logger = LoggerFactory().create(logger_name, [datadog_handler, console_handler])
    
    return logger
