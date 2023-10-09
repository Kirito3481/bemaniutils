from typing import List, Optional, Type

from bemani.backend.base import Base, Factory
from bemani.backend.beatstream.beatstream import Beatstream
from bemani.common import Model, VersionConstants
from bemani.data import Config, Data


class BeatstreamFactory(Factory):
    MANAGED_CLASSES: List[Type[Base]] = [
        Beatstream
    ]

    @classmethod
    def register_all(cls) -> None:
        for gamecode in ["NBT"]:
            Base.register(gamecode, BeatstreamFactory)

    @classmethod
    def create(
        cls,
        data: Data,
        config: Config,
        model: Model,
        parentmodel: Optional[Model] = None
    ) -> Optional[Base]:
        def version_from_date(date: int) -> Optional[int]:
            if date <= 2015121600:
                return VersionConstants.BEATSTREAM

        if model.gamecode == "NBT":
            if model.version is None:
                if parentmodel is None:
                    return None
                
                if parentmodel.gamecode not in ["NBT"]:
                    return None
                
                parentversion = version_from_date(parentmodel.version)

                return None
            
            version = version_from_date(model.version)
            if version == VersionConstants.BEATSTREAM:
                return Beatstream(data, config, model)

        # Unknown game version
        return None
