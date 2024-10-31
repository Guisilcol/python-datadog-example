from typing import Optional
from datadog_api_client.v2 import Configuration, ApiClient
from datadog_api_client.v2.models import HTTPLog, HTTPLogItem
from datadog_api_client.v2.api.logs_api import LogsApi


class ConfigurationFactory:
    
    def create(self, api_key: str, app_key: Optional[str] = None, site: Optional[str] = None) -> Configuration:
        keys = {
            'apiKeyAuth': api_key,
            'appKeyAuth': app_key
        }
        
        server_variables = {
            "site": site
        }
        
        return Configuration(api_key=keys, server_variables=server_variables)


class ApiClientFactory:
    def create(self, configuration: Configuration) -> ApiClient:
        return ApiClient(configuration)
    

class HTTPLogFactory:
    
    def create(self, ddsource: str, ddtags: str, message: str, service: str) -> HTTPLog:
        return HTTPLog([
            HTTPLogItem(
                ddsource=ddsource,
                ddtags=ddtags,
                message=message,
                service=service
            )
        ])
       
 
class LogsApiFactory:
    def create(self, api_client: ApiClient) -> LogsApi:
        return LogsApi(api_client)