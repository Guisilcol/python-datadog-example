import os
from logging import StreamHandler, LogRecord, INFO, DEBUG, ERROR, WARNING, CRITICAL
from typing import Literal
from datadog_api_client.v2.api.logs_api import LogsApi

from pythondatadogexample.datadog_api import HTTPLogFactory
from pythondatadogexample.formatter import Formatter

LEVELS_MAP = {
    'INFO': INFO,
    'DEBUG': DEBUG,
    'ERROR': ERROR,
    'WARNING': WARNING,
    'CRITICAL': CRITICAL
}


PossibleLevels = Literal['INFO', 'DEBUG', 'ERROR', 'WARNING', 'CRITICAL']


class DatadogHandler(StreamHandler):
    """
    LogHandler personalizado para envio de logs ao Datadog usando a API Datadog.
    
    Atributos:
        configuration (Configuration): Instância da configuração da API do Datadog.
        service_name (str): Nome do serviço ao qual o log pertence, utilizado para identificar a origem do log no Datadog.
        ddsource (str): Identificação da fonte do log no Datadog.
    """

    def __init__(
        self, 
        logs_api: LogsApi, 
        service_name: str, 
        ddsource: str, 
        log_factory: HTTPLogFactory, 
        raise_on_error: bool = False, 
        *args, 
        **kwargs
    ) -> None:
        """
        Inicializa o DatadogHandler com a configuração da API, nome do serviço e fonte do log.

        Parâmetros:
            configuration (Configuration): Configuração da API Datadog.
            service_name (str): Nome do serviço que envia o log.
            ddsource (str): Fonte identificadora do log.
        """
        super().__init__(*args, **kwargs)
        self.logs_api = logs_api
        self.service_name = service_name
        self.ddsource = ddsource
        self.log_factory = log_factory
        self.raise_on_error = raise_on_error

    def emit(self, record: LogRecord) -> None:
        """
        Envia o log formatado ao Datadog usando a API.

        Parâmetros:1
            record (LogRecord): Registro de log a ser enviado ao Datadog.
        """
        msg = self.format(record)        
        body = self.log_factory.create(self.ddsource, f"env:{os.getenv('ENV', 'development')}", msg, self.service_name)

        try:
            self.logs_api.submit_log(body)
        except Exception as e:
            error_message = f"An error occurred when trying to submit the log to Datadog using the LogsApi.submit_log method"
            
            if self.raise_on_error:
                raise Exception(f"An error occurred when trying to submit the log to Datadog using the LogsApi.submit_log method") from e

            print(error_message)
            print(e)

class LogHandlerFactory:
    """
    Fábrica para criação de instâncias de LogHandler, permitindo a criação de handlers para diferentes destinos (Datadog e console).
    """

    def create_datadog_handler(
        self, 
        logs_api: LogsApi, 
        log_factory: HTTPLogFactory, 
        service_name: str, 
        ddsource: str, 
        level: PossibleLevels, 
        formater: Formatter,
        raise_on_error: bool = False
    ) -> StreamHandler:
        """
        Cria e configura um handler para envio de logs ao Datadog com o nível de log especificado.
        
        Parâmetros:
            configuration (Configuration): Configuração da API Datadog.
            service_name (str): Nome do serviço que envia o log.
            ddsource (str): Fonte identificadora do log.
            level (PossibleLevels): Nível do log (ex.: 'INFO', 'ERROR').

        Retorna:
            StreamHandler: Instância de DatadogHandler configurada para o Datadog.
        """
        handler = DatadogHandler(logs_api, service_name, ddsource, log_factory, raise_on_error)
        handler.setLevel(LEVELS_MAP[level])
        handler.setFormatter(formater)
        return handler
    
    def create_console_handler(self, level: PossibleLevels, formatter: Formatter) -> StreamHandler:
        """
        Cria e configura um handler para exibição de logs no console com o nível de log especificado.

        Parâmetros:
            level (PossibleLevels): Nível do log (ex.: 'INFO', 'ERROR').

        Retorna:
            StreamHandler: Instância de StreamHandler configurada para exibir logs no console.
        """
        handler = StreamHandler()
        handler.setLevel(LEVELS_MAP[level])
        handler.setFormatter(formatter)
        return handler
