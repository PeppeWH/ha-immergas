"""DataUpdateCoordinator per Immergas Smartech Plus."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ImmergasClient, ImmergasConnectionError
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ImmergasCoordinator(DataUpdateCoordinator):
    """Coordina il polling dei dati da Immergas."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: ImmergasClient,
        device_name: str,
        thing_id: str,
        device_n: int,
        poll_interval: int,
    ) -> None:
        self.client      = client
        self.device_name = device_name
        self.thing_id    = thing_id
        self.device_n    = device_n

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=poll_interval),
        )

    async def _async_update_data(self) -> dict:
        """Chiama l'API e restituisce i dati aggiornati."""
        try:
            return await self.hass.async_add_executor_job(
                self.client.get_status,
                self.device_name,
                self.thing_id,
                self.device_n,
            )
        except ImmergasConnectionError as err:
            raise UpdateFailed(f"Errore comunicazione Immergas: {err}") from err
