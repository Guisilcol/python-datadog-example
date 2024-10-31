import pythondatadogexample.itau_logger as logger
import os

def main():
    api_key = ""
    app_key = ""
    site = "us5.datadoghq.com"
    env = "DEV"
    
    log = logger.get_datadog_logger(
        service_name='service_itau_logger', 
        ddsource='ddsourceitau_logger',
        acronym='QJ6',
        logger_name='itau_logger',
        api_key=api_key,
        app_key=app_key,
        site=site,
        environment=env,
        raise_on_error=True
    )
    
    
    log.debug('This is a debug message')
    log.info('This is a test message')
    log.error('This is an error message')
    log.warning('This is a warning message')
    log.critical('This is a critical message')

if __name__ == '__main__':
    main()
