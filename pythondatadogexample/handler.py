import os
from logging import StreamHandler, LogRecord, INFO, DEBUG, ERROR, WARNING, CRITICAL
from typing import Literal
from datadog_api_client.v2.api.logs_api import LogsApi
from pythondatadogexample.datadog_api import HTTPLogFactory
from pythondatadogexample.formatter import Formatter
from pythondatadogexample.tags import Tags

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
        tags (Tags): Tags de contexto do ambiente e execução.
        logs_api (LogsApi): Instância da API de logs do Datadog para envio de logs.
        log_factory (HTTPLogFactory): Fábrica de logs HTTP para formatação de logs.
        raise_on_error (bool): Define se uma exceção será levantada em caso de erro no envio de logs.
    """

    def __init__(
        self, 
        tags: Tags,
        logs_api: LogsApi, 
        log_factory: HTTPLogFactory, 
        raise_on_error: bool = False, 
        *args, 
        **kwargs
    ) -> None:
        """
        Inicializa o DatadogHandler com a configuração da API, tags e parâmetros de controle.

        Parâmetros:
            tags (Tags): Tags de contexto como ambiente, serviço e host.
            logs_api (LogsApi): Instância da API de logs do Datadog.
            log_factory (HTTPLogFactory): Fábrica para criação de logs HTTP formatados.
            raise_on_error (bool): Define se erros de envio devem levantar exceções.
        """
        super().__init__(*args, **kwargs)
        self.tags = tags
        self.logs_api = logs_api
        self.log_factory = log_factory
        self.raise_on_error = raise_on_error

    def emit(self, record: LogRecord) -> None:
        """
        Envia o log formatado ao Datadog usando a API.

        Parâmetros:
            record (LogRecord): Registro de log a ser enviado ao Datadog.
        """
        msg = self.format(record)
        ddtags = [f"{key}:{value}" for key, value in self.tags.items()]
        ddtags = ','.join(ddtags)
        
        body = self.log_factory.create(
            self.tags.get('ddsource'), 
            ddtags, 
            msg, 
            self.tags.get('service')
        )

        try: 
            self.logs_api.submit_log(body)
        except Exception as e:
            error_message = "Erro ao tentar enviar o log para o Datadog usando o método LogsApi.submit_log."
            if self.raise_on_error:
                raise Exception(error_message) from e

            print(error_message)
            print(e)


class LogHandlerFactory:
    """
    Fábrica para criação de instâncias de LogHandler, permitindo a criação de handlers para diferentes destinos (Datadog e console).
    """

    def create_datadog_handler(
        self, 
        tags: Tags,
        logs_api: LogsApi, 
        log_factory: HTTPLogFactory, 
        level: PossibleLevels, 
        formatter: Formatter,
        raise_on_error: bool = False
    ) -> StreamHandler:
        """
        Cria e configura um handler para envio de logs ao Datadog com o nível de log especificado.

        Parâmetros:
            tags (Tags): Tags de contexto para o log.
            logs_api (LogsApi): Instância da API de logs do Datadog.
            log_factory (HTTPLogFactory): Fábrica de logs HTTP para envio.
            level (PossibleLevels): Nível do log (ex.: 'INFO', 'ERROR').
            formatter (Formatter): Formatter para formatação do log.
            raise_on_error (bool): Define se erros de envio devem levantar exceções.

        Retorna:
            StreamHandler: Instância de DatadogHandler configurada para o Datadog.
        """
        handler = DatadogHandler(tags, logs_api, log_factory, raise_on_error)
        handler.setLevel(LEVELS_MAP[level])
        handler.setFormatter(formatter)
        return handler
    
    def create_console_handler(self, level: PossibleLevels, formatter: Formatter) -> StreamHandler:
        """
        Cria e configura um handler para exibição de logs no console com o nível de log especificado.

        Parâmetros:
            level (PossibleLevels): Nível do log (ex.: 'INFO', 'ERROR').
            formatter (Formatter): Formatter para formatação do log.

        Retorna:
            StreamHandler: Instância de StreamHandler configurada para exibir logs no console.
        """
        handler = StreamHandler()
        handler.setLevel(LEVELS_MAP[level])
        handler.setFormatter(formatter)
        return handler
