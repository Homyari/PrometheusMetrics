Metrics Collector

The program is designed to collect server metrics (load average, number of new IP addresses and another in future) and export them in a format compatible with Prometheus. The metrics are served on localhost:9999/metrics, where Prometheus can scrape them.

Current Features:
* Load average tracking for 1 minute (prometheus_prometheus_metric_load_average_1_min)
* Counting new unique ips every day (prometheus_metric_new_ip_counter)
