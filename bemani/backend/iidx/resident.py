# vim: set fileencoding=utf-8
from typing import Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.casthour import IIDXCastHour
from bemani.common import VersionConstants


class IIDXResident(IIDXBase):
    name: str = "Beatmania IIDX RESIDENT"
    version: int = VersionConstants.IIDX_RESIDENT

    requires_extended_regions: bool = True

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXCastHour(self.data, self.config, self.model)
