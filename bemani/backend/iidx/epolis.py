# vim: set fileencoding=utf-8
from typing import Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.resident import IIDXResident
from bemani.common import VersionConstants


class IIDXEpolis(IIDXBase):
    name: str = "Beatmania IIDX EPOLIS"
    version: int = VersionConstants.IIDX_EPOLIS

    requires_extended_regions: bool = True

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXResident(self.data, self.config, self.model)
