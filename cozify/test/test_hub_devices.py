#!/usr/bin/env python3
import pytest

from cozify import hub, hub_api, config
from cozify.test import debug
from cozify.test.fixtures import *
from cozify.Error import APIError


def test_hub_devices_filter_single(tmp_hub):
    ids, devs = tmp_hub.devices()
    out = hub.devices(hub_id=tmp_hub.id, capabilities=hub.capability.COLOR_LOOP, mock_devices=devs)
    assert all(i in out for i in [ids['lamp_osram'], ids['strip_osram']])
    assert len(out) == 2


def test_hub_devices_filter_or(tmp_hub):
    ids, devs = tmp_hub.devices()
    out = hub.devices(
        hub_id=tmp_hub.id,
        and_filter=False,
        capabilities=[hub.capability.TWILIGHT, hub.capability.COLOR_HS],
        mock_devices=devs)
    assert all(i in out for i in [ids['lamp_osram'], ids['strip_osram'], ids['twilight_nexa']])
    assert len(out) == 3


def test_hub_devices_filter_and(tmp_hub):
    ids, devs = tmp_hub.devices()
    out = hub.devices(
        hub_id=tmp_hub.id,
        and_filter=True,
        capabilities=[hub.capability.COLOR_HS, hub.capability.COLOR_TEMP],
        mock_devices=devs)
    assert all(i in out for i in [ids['lamp_osram'], ids['strip_osram']])
    assert len(out) == 2


def test_hub_device_eligible(tmp_hub):
    ids, devs = tmp_hub.devices()
    assert hub.device_eligible(ids['lamp_osram'], hub.capability.COLOR_TEMP, mock_devices=devs)
    assert not hub.device_eligible(
        ids['twilight_nexa'], hub.capability.COLOR_TEMP, mock_devices=devs)


def test_hub_device_implicit_state(tmp_hub):
    ids, devs = tmp_hub.devices()
    state = {}
    hub.device_eligible(
        ids['lamp_osram'], hub.capability.COLOR_TEMP, mock_devices=devs, state=state)
    assert 'temperature' in state
    hub.device_exists(ids['twilight_nexa'], mock_devices=devs, state=state)
    assert 'twilight' in state


def test_hub_device_reachable(tmp_hub):
    ids, devs = tmp_hub.devices()
    assert hub.device_reachable(ids['reachable'], mock_devices=devs)
    assert not hub.device_reachable(ids['not-reachable'], mock_devices=devs)
    with pytest.raises(ValueError):
        hub.device_reachable('dead-beef', mock_devices=devs)


def test_hub_device_exists(tmp_hub):
    ids, devs = tmp_hub.devices()
    assert hub.device_exists(ids['reachable'], mock_devices=devs)
    assert not hub.device_exists('dead-beef', mock_devices=devs)