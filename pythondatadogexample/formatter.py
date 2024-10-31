from typing import Optional
from logging import Formatter, LogRecord
from json import dumps

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
        environment: str,
        acronym: str,
        job_name: Optional[str] = None,
        job_run_id: Optional[str] = None,
        hostname: Optional[str] = None,
        *args,
        **kwargs
    ):
        """
        Inicializa o JSONFormatter com informações de ambiente, serviço e execução.

        Parâmetros:
            environment (str): Ambiente do código (ex.: produção, desenvolvimento).
            acronym (str): Acrônimo do serviço.
            job_name (Optional[str]): Nome do job, se disponível.
            job_run_id (Optional[str]): ID de execução do job, se disponível.
            hostname (Optional[str]): Nome do host, se disponível.
            *args, **kwargs: Argumentos adicionais para a superclasse Formatter.
        """
        super().__init__(*args, **kwargs)
        self.environment = environment
        self.acronym = acronym
        self.job_name = job_name
        self.job_run_id = job_run_id
        self.hostname = hostname 

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
            'sigla': self.acronym,
            'message': record.getMessage(),
            'level': record.levelname,
            'service': f'{self.acronym} - {self.job_name or "N/A"}',
            'version': 'v1.0',
            'hostname': self.hostname or "N/A",
            'env': self.environment,
            'logger.name': record.funcName,
            'correlationId': self.job_run_id or "N/A"
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
        environment: str,
        acronym: str,
        job_name: Optional[str] = None,
        job_run_id: Optional[str] = None,
        hostname: Optional[str] = None) -> JSONFormatter:
        """
        Cria um novo JSONFormatter com as informações de ambiente e execução.

        Retorna:
            JSONFormatter: Formatter JSON criado.
        """
        return JSONFormatter(environment, acronym, job_name, job_run_id, hostname)