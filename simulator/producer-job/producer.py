import os
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import inject
import requests

service_name = "producer-service"

resource = Resource(attributes={
    SERVICE_NAME: service_name
})

trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=f'{os.getenv("OTLP_ENDPOINT", "http://localhost:56290")}/v1/traces')
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

def send_message_to_broker(message):
    with tracer.start_as_current_span("produce_message"):
        headers = {}
        inject(headers)
        response = requests.post(f'{os.getenv("BROKER_ENDPOINT","http://localhost:5000")}/broker', json=message, headers=headers)
        return response.text
    
if __name__ == "__main__":
    message = {"data": "Hello, Consumer!"}
    print("Producer sending message to broker:", message)
    send_message_to_broker(message)
