from typing import Optional
from logging import Formatter, LogRecord
from json import dumps

from pythondatadogexample.tags import Tags

class JSONFormatter(Formatter):
    """
    Formata logs no formato JSON com informações de contexto do ambiente e do job em execução.

    Atributos:
        environment (str): Ambiente onde o código está sendo executado (ex.: produção, desenvolvimento).
        acronym (str): Acrônimo identificador do serviço.
        job_name (Optional[str]): Nome do job em execução.
        job_run_id (Optional[str]): ID de execução do job.
        hostname (Optional[str]): Nome do host onde o código está rodando.
    """

    def __init__(
        self,
        tags: Tags,
        *args,
        **kwargs
    ):
        """
        Inicializa o JSONFormatter com informações de ambiente, serviço e execução.
        """
        super().__init__(*args, **kwargs)
        self.tags = tags

    def format(self, record: LogRecord) -> str:
        """
        Formata um LogRecord no formato JSON, incluindo informações de contexto e exceções.

        Parâmetros:
            record (LogRecord): Registro de log a ser formatado.

        Retorna:
            str: Representação do log em formato JSON.
        """
        formatted_record = {
            'timestamp': self.formatTime(record, self.datefmt),
            'sigla': self.tags.get('sigla'),
            'message': record.getMessage(),
            'level': record.levelname,
            'service': self.tags.get('service'),
            'version': self.tags.get('version'),
            'hostname': self.tags.get('hostname'),
            'env': self.tags.get('environment'),
            'logger.name': record.funcName,
            'correlationId': self.tags.get('correlationId'),
        }

        if record.exc_info:
            formatted_record['exception'] = self.formatException(record.exc_info)
            
        return dumps(formatted_record)

class FormatterFactory:
    """
    Fábrica de formatters JSON para logs.

    Atributos:
        environment (str): Ambiente onde o código está sendo executado (ex.: produção, desenvolvimento).
        acronym (str): Acrônimo identificador do serviço.
        job_name (Optional[str]): Nome do job em execução.
        job_run_id (Optional[str]): ID de execução do job.
        hostname (Optional[str]): Nome do host onde o código está rodando.
    """

    def create_json_formatter(
        self,         
        tags: Tags,
    ) -> JSONFormatter:
        """
        Cria um novo JSONFormatter com as informações de ambiente e execução.

        Retorna:
            JSONFormatter: Formatter JSON criado.
        """
        return JSONFormatter(tags)