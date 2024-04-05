from flask import Flask, request, jsonify
import requests
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.propagate import extract, inject
import os
import logging

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({SERVICE_NAME: "broker-service"}))
)
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint=f'{os.getenv("OTLP_ENDPOINT", "http://localhost:56290")}/v1/traces')
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

app = Flask(__name__)

@app.route('/broker', methods=['POST'])
def broker():
    with tracer.start_as_current_span("broker_span"):
      context = extract(request.headers)
      with tracer.start_as_current_span("forward_to_consumer", context=context):
        headers = {}
        inject(headers)
        message = request.json
        response = requests.post(f'{os.getenv("CONSUMER_ENDPOINT", "http://localhost:5001")}/consumer', json=message, headers=headers)
        return jsonify({"status": "message forwarded to consumer", "response": response.text})
      
if __name__ == "__main__":
    app.run(port=5000)



