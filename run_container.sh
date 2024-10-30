docker run -d --name datadog-agent \
  -e DD_API_KEY=YOUR_API_KEY \
  -e DD_SITE="datadoghq.com" \
  -e DD_LOGS_ENABLED=true \
  -e DD_CONTAINER_EXCLUDE="name:datadog-agent" \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  gcr.io/datadoghq/agent:latest