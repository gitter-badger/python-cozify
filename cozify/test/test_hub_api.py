#!/usr/bin/env python3
import pytest

from cozify import conftest
from cozify import cloud, hub, hub_api, config

@pytest.mark.live
def test_hub(live_cloud, live_hub):
    assert live_hub.ping()
    hub_id = live_hub.default()
    assert hub_api.hub(
            hub_id = hub_id,
            host = live_hub.host,
            remote = live_hub.remote,
            cloud_token = live_cloud.token(),
            hub_token = live_hub.token(hub_id)
            )
