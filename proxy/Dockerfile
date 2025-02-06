FROM envoyproxy/envoy:v1.28.0
COPY envoy.yaml /etc/envoy/envoy.yaml
CMD ["envoy", "-c", "/etc/envoy/envoy.yaml", "--log-level", "debug"]
