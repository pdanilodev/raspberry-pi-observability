# Observabilidade em tempo real no Raspberry Pi

API em Python (FastAPI) rodando em um Raspberry Pi 4, monitorada com
Prometheus e Grafana, tudo em containers com Docker Compose.

![Dashboard](docs/dashboard.png)

## Arquitetura

- **app**: API FastAPI que expõe métricas em `/metrics` (requisições, latência, erros e temperatura da CPU)
- **Prometheus**: coleta as métricas a cada 5s
- **Node Exporter**: métricas do sistema (CPU, memória, disco, rede)
- **Grafana**: dashboards e visualização

## Como rodar

Requisitos: Raspberry Pi com Docker e Docker Compose.

```bash
git clone https://github.com/SEU_USUARIO/raspberry-pi-observability.git
cd raspberry-pi-observability
docker compose up -d --build
```

| Serviço | Endereço |
|---|---|
| Grafana | http://IP_DO_PI:3000 (admin / admin) |
| Prometheus | http://IP_DO_PI:9090 |
| API | http://IP_DO_PI:8000/work |

## Configurando o Grafana

1. Connections → Data sources → Prometheus, URL `http://prometheus:9090`
2. Dashboards → Import → ID `1860` (Node Exporter Full)
3. Queries do dashboard da API:
   - Requisições/s: `sum(rate(http_requests_total[1m]))`
   - Erros: `sum(rate(http_requests_total{status="5xx"}[1m]))`
   - Latência p95: `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))`
   - Temperatura: `pi_cpu_temp_celsius`

## Gerando tráfego

```bash
while true; do curl -s localhost:8000/work > /dev/null; sleep 0.2; done
```

## Próximos passos

- Alertas no Telegram
- cAdvisor (métricas por container)
- Loki (logs)

## Stack

Raspberry Pi 4 · Raspberry Pi OS · Docker · FastAPI · Prometheus · Grafana
