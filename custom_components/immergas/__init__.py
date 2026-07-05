"""Integrazione Immergas Smartech Plus per Home Assistant."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL
from homeassistant.core import HomeAssistant

from .api import ImmergasClient
from .const import DOMAIN, PLATFORMS, CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL
from .coordinator import ImmergasCoordinator

CONF_TOKEN_A   = "token_a"
CONF_TOKEN_B   = "token_b"
CONF_PHPSESSID = "phpsessid"

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura l'integrazione a partire da un config entry."""
    token_a   = entry.data[CONF_TOKEN_A]
    token_b   = entry.data[CONF_TOKEN_B]
    phpsessid = entry.data[CONF_PHPSESSID]
    interval  = entry.options.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)

    client = ImmergasClient(
        token_a=token_a,
        token_b=token_b,
        phpsessid=phpsessid,
    )

    devices = await hass.async_add_executor_job(client.get_devices)
    device      = devices[0]
    thing_id    = device["thing_id"]
    device_name = device["device_name"]

    coordinators = []
    for zone in devices:
        coordinator = ImmergasCoordinator(
            hass,
            client,
            zone["device_name"],
            zone["thing_id"],
            zone["device_n"],
            interval,
        )
        await coordinator.async_config_entry_first_refresh()
        coordinators.append(coordinator)

    _LOGGER.debug(
        "Immergas setup found %s gateway(s) and created %s zone coordinator(s)",
        len({zone["thing_id"] for zone in devices}),
        len(coordinators),
    )

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {
        "coordinator": coordinators[0],
        "coordinators": coordinators,
        "client":      client,
        "device_name": device_name,
        "thing_id":    thing_id,
        "devices":     devices,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Rimuove l'integrazione."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Ricarica l'integrazione quando cambiano le opzioni."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
