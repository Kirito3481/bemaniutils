from typing import Dict, Iterable, List, Optional, Set, NamedTuple
from typing_extensions import Final

from bemani.backend.base import Base
from bemani.backend.core import CoreHandler, CardManagerHandler, PASELIHandler
from bemani.common import Profile, ValidatedDict, GameConstants
from bemani.data import Machine, UserID
from bemani.protocol import Node


class BeatstreamBase(CoreHandler, CardManagerHandler, PASELIHandler, Base):
    """
    Base game class for all Beatstream versions
    """

    game: GameConstants = GameConstants.BEATSTREAM

    def previous_version(self) -> Optional["BeatstreamBase"]:
        """
        Returns the previous version of the game, based on this game. Should
        be overridden.
        """
        return None

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        """
        Base handler for a profile. Given a userid and a profile dictionary,
        return a Node representing a profile. Should be overridden.
        """
        return Node.void("player")

    def unformat_profile(
        self, userid: UserID, request: Node, oldprofile: Profile
    ) -> Profile:
        """
        Base handler for profile parsing. Given a request and an old profile,
        return a new profile that's been updated with the contents of the request.
        Should be overridden.
        """
        return oldprofile

    def get_profile_by_refid(self, refid: Optional[str]) -> Optional[Node]:
        """
        Given a RefID, return a formatted profile node. Basically every game
        needs a profile lookup, even if it handles where that happens in
        a different request. This is provided for code deduplication.
        """
        if refid is None:
            return None

        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is None:
            # User doesn't exist but should at this point
            return None

        # Trying to import from current version
        profile = self.get_profile(userid)
        if profile is None:
            return None
        return self.format_profile(userid, profile)

    def put_profile_by_refid(
        self, refid: Optional[str], request: Node
    ) -> Optional[Profile]:
        """
        Given a RefID and a request node, unformat the profile and save it.
        """
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is None:
            return None

        oldprofile = self.get_profile(userid)
        if oldprofile is None:
            # Create one so we can get refid/extid
            oldprofile = Profile(self.game, self.version, refid, 0)
            self.put_profile(userid, oldprofile)
        newprofile = self.unformat_profile(userid, request, oldprofile)
        if newprofile is not None:
            self.put_profile(userid, newprofile)
            return newprofile
        else:
            return oldprofile

    def get_machine_by_id(self, shop_id: int) -> Optional[Machine]:
        pcbid = self.data.local.machine.from_machine_id(shop_id)
        if pcbid is not None:
            return self.data.local.machine.get_machine(pcbid)
        else:
            return None
