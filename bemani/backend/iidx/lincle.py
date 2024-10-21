from typing import Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.resortanthem import IIDXResortAnthem

from bemani.common import VersionConstants


class IIDXLincle(IIDXBase):
    name: str = "Beatmania IIDX Lincle"
    version: int = VersionConstants.IIDX_LINCLE

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXResortAnthem(self.data, self.config, self.model)