# vim: set fileencoding=utf-8
from typing import Optional

from bemani.backend.jubeat.base import JubeatBase
from bemani.common import VersionConstants


class Jubeat(JubeatBase):
    name: str = "Jubeat"
    version: int = VersionConstants.JUBEAT
