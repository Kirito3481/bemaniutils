# vim: set fileencoding=utf-8
from typing import Optional

from bemani.backend.jubeat.base import JubeatBase
from bemani.common import VersionConstants


class Jubeat(JubeatBase):
    name: str = "Jubeat"
    version: int = VersionConstants.JUBEAT


class JubeatRipples(JubeatBase):
    name: str = "Jubeat Ripples"
    version: int = VersionConstants.JUBEAT_RIPPLES

    def previous_version(self) -> Optional[JubeatBase]:
        return Jubeat(self.data, self.config, self.model)


class JubeatRipplesAppend(JubeatBase):
    name: str = "Jubeat Ripples Append"
    version: int = VersionConstants.JUBEAT_RIPPLES_APPEND

    def previous_version(self) -> Optional[JubeatBase]:
        return JubeatRipples(self.data, self.config, self.model)

