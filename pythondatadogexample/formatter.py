from typing import Optional
from logging import Formatter, LogRecord
from json import dumps
from pythondatadogexample.tags import Tags


class JSONFormatter(Formatter):
    """
    Formata logs no formato JSON com informações de contexto do ambiente e do job em execução.

    Atributos:
        tags (Tags): Objeto contendo informações de tags como ambiente, serviço e correlação.
    """

    def __init__(self, tags: Tags, *args, **kwargs):
        """
        Inicializa o JSONFormatter com informações de ambiente, serviço e execução.

        Parâmetros:
            tags (Tags): Objeto de tags contendo dados de contexto como ambiente e serviço.
            *args: Argumentos posicionais adicionais para o inicializador.
            **kwargs: Argumentos nomeados adicionais para o inicializador.
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
    Fábrica para criar formatadores JSON para logs, utilizando contexto de ambiente e execução.
    """

    def create_json_formatter(self, tags: Tags) -> JSONFormatter:
        """
        Cria uma instância de JSONFormatter com informações de ambiente e execução.

        Parâmetros:
            tags (Tags): Objeto de tags contendo dados de contexto como ambiente e serviço.

        Retorna:
            JSONFormatter: Formatter JSON configurado com as tags fornecidas.
        """
        return JSONFormatter(tags)
