# vim: set fileencoding=utf-8
from typing import Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.casthour import IIDXCasthour
from bemani.common import VersionConstants


class IIDXResident(IIDXBase):
    name: str = "Beatmania IIDX Resident"
    version: int = VersionConstants.IIDX_RESIDENT

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXCasthour(self.data, self.config, self.model)