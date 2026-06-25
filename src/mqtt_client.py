"""MQTT client skeleton for PLC/DCS telemetry exchange (doc step 5).

Wraps paho-mqtt for publishing judgment results and subscribing to process
tags, guarded behind an optional import so the rest of the pipeline works
without paho-mqtt installed.
"""
from __future__ import annotations

import json
from typing import Callable

try:
    import paho.mqtt.client as mqtt
except ImportError:  # pragma: no cover
    mqtt = None


class MqttBridge:
    def __init__(self, broker_host: str, broker_port: int = 1883, client_id: str = "sx-quality-bridge"):
        if mqtt is None:
            raise RuntimeError("paho-mqtt is not installed; add it to requirements.txt to use MQTT")
        self._client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        self._broker_host = broker_host
        self._broker_port = broker_port

    def connect(self) -> None:
        self._client.connect(self._broker_host, self._broker_port)

    def publish_json(self, topic: str, payload: dict) -> None:
        self._client.publish(topic, json.dumps(payload, ensure_ascii=False))

    def subscribe(self, topic: str, on_message: Callable[[dict], None]) -> None:
        def _handler(_client, _userdata, message, *_args) -> None:
            on_message(json.loads(message.payload.decode("utf-8")))

        self._client.on_message = _handler
        self._client.subscribe(topic)

    def loop_forever(self) -> None:
        self._client.loop_forever()
