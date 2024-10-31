import pythondatadogexample.itau_logger as logger
import os

def main():
    api_key = ""
    app_key = ""
    site = "us5.datadoghq.com"
    env = "DEV"
    
    log = logger.get_datadog_logger(
        {
            'sigla': 'ITAU',
            'cloud_provider': 'aws',
            'condominio': 'devops',
            'account_id': '123456789012',
            'environment': env,
            'version': '1.0.0',
            'service': 'ITAU-TEST',
            'hostname': os.getenv('HOSTNAME', 'localhost'),
            'correlationId': '123456789',
            'ddsource': 'python',
        },

        logger_name='itau_logger',
        api_key=api_key,
        app_key=app_key,
        site=site,
        raise_on_error=True
    )
    
    
    log.debug('This is a debug message')
    log.info('This is a test message')
    log.error('This is an error message')
    log.warning('This is a warning message')
    log.critical('This is a critical message')

if __name__ == '__main__':
    main()
