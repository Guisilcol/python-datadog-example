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
from pythondatadogexample.tags import Tags, TagsValidator

def get_datadog_api_logger(
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
    Configura e retorna um logger para envio de logs ao Datadog via API REST, 
    incluindo um handler para console.

    Este logger permite enviar logs de nível WARNING, ERROR e CRITICAL ao Datadog
    por padrão, enquanto todos os níveis de log podem ser enviados ao console.

    Parâmetros:
        - tags (Tags): Dicionário contendo as informações de contexto do log, como serviço, 
          fonte do log, sigla, ambiente, entre outras.
        - data_dog_handler_level (PossibleLevels, opcional): Nível de log para o handler do Datadog. 
          Os logs deste nível ou superior serão enviados ao Datadog. O padrão é 'WARNING'.
        - console_handler_level (PossibleLevels, opcional): Nível de log para o handler do console.
          Os logs deste nível ou superior serão exibidos no console. O padrão é 'DEBUG'.
        - api_key (str, opcional): Chave de API do Datadog para autenticação.
        - app_key (str, opcional): Chave de aplicação do Datadog para operações específicas.
        - site (str, opcional): URL do site Datadog (exemplo: 'datadoghq.com'). O padrão é 'datadoghq.com'.
        - logger_name (str, opcional): Nome do logger. O padrão é 'datadog_logger'.
        - raise_on_error (bool, opcional): Se True, levanta exceções em caso de falha ao enviar logs ao Datadog. 
          Caso contrário, falhas de envio serão silenciosamente ignoradas. O padrão é False.

    Retorna:
        Logger: Uma instância configurada de `logging.Logger` com handlers para envio de logs
        ao Datadog e ao console.

    Exceções:
        Levanta uma exceção se as tags fornecidas forem inválidas.
    """
    
    # Validação das tags. Se houver erro, uma exceção é levantada.
    errors = TagsValidator().validate(tags)
    if errors:
        raise ValueError(f'Erro ao validar tags: {", ".join(errors)}')
    
    
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
