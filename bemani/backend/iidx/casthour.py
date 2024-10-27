# vim: set fileencoding=utf-8
from typing import Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.bistrover import IIDXBistrover
from bemani.common import VersionConstants


class IIDXCastHour(IIDXBase):
    name: str = "Beatmania IIDX CastHour"
    version: int = VersionConstants.IIDX_CASTHOUR

    requires_extended_regions: bool = True

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXBistrover(self.data, self.config, self.model)
