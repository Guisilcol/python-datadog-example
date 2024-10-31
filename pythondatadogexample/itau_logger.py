from logging import Logger

from pythondatadogexample.datadog_api import (
    HTTPLogFactory, 
    LogsApiFactory, 
    ConfigurationFactory, 
    ApiClientFactory
)
from pythondatadogexample.formatter import FormatterFactory
from pythondatadogexample.handler import LogHandlerFactory
from pythondatadogexample.logger import LoggerFactory

def get_datadog_logger(service_name: str, 
                       ddsource: str, 
                       acronym: str,
                       job_name: str = '',
                       job_run_id: str = '',
                       hostname: str = '',
                       environment: str = '',
                       api_key: str = '', 
                       app_key: str = '',
                       logger_name: str = 'datadog_logger', 
                       site: str = 'datadoghq.com',
                       raise_on_error: bool = False
) -> Logger:
    
    formatter = FormatterFactory().create_json_formatter(
        environment, 
        acronym, 
        job_name, 
        job_run_id, 
        hostname
    )
    
    datadog_api_configuration = ConfigurationFactory().create(api_key, app_key, site)
    api_client = ApiClientFactory().create(datadog_api_configuration)
    logs_api = LogsApiFactory().create(api_client)
    log_factory  = HTTPLogFactory()
    datadog_handler = LogHandlerFactory().create_datadog_handler(
        logs_api, 
        log_factory, 
        service_name, 
        ddsource, 
        'INFO', 
        formatter,
        raise_on_error
    )
    
    console_handler = LogHandlerFactory().create_console_handler('DEBUG', formatter)
    
    logger = LoggerFactory().create(logger_name, [datadog_handler, console_handler])
    
    return logger
