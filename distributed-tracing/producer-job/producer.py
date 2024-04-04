import os
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

service_name = "Random-Trace-Producer"

resource = Resource(attributes={
    SERVICE_NAME: service_name
})

trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=f'{os.getenv("OTLP_ENDPOINT", "http://localhost:56290")}/v1/traces')
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("example-span"):
    print("Hello, trace!")
