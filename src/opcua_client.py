"""OPC-UA client skeleton for PLC/DCS tag exchange (doc step 5).

Wraps asyncua so the rest of the pipeline can read pH/flow/XRF/UV-Vis tags
and write control commands without depending on asyncua being installed
in environments that only run the rule-based logic and tests.
"""
from __future__ import annotations

from typing import Any

try:
    from asyncua import Client
except ImportError:  # pragma: no cover
    Client = None


class OpcUaTagClient:
    def __init__(self, endpoint_url: str):
        if Client is None:
            raise RuntimeError("asyncua is not installed; add it to requirements.txt to use OPC-UA")
        self._endpoint_url = endpoint_url
        self._client = Client(endpoint_url)

    async def __aenter__(self) -> "OpcUaTagClient":
        await self._client.connect()
        return self

    async def __aexit__(self, *exc_info) -> None:
        await self._client.disconnect()

    async def read_tag(self, node_id: str) -> Any:
        node = self._client.get_node(node_id)
        return await node.read_value()

    async def write_tag(self, node_id: str, value: Any) -> None:
        node = self._client.get_node(node_id)
        await node.write_value(value)
