import pytest

from src.mqtt_client import MqttBridge
from src.opcua_client import OpcUaTagClient


def test_opcua_client_constructs_with_endpoint():
    client = OpcUaTagClient("opc.tcp://localhost:4840/freeopcua/server/")
    assert client._endpoint_url == "opc.tcp://localhost:4840/freeopcua/server/"


def test_mqtt_bridge_constructs_without_connecting():
    bridge = MqttBridge(broker_host="localhost", broker_port=1883)
    assert bridge._broker_host == "localhost"


def test_mqtt_bridge_requires_real_broker_to_connect():
    bridge = MqttBridge(broker_host="127.0.0.1", broker_port=1)
    with pytest.raises(Exception):
        bridge.connect()
