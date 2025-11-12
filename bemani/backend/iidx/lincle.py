# vim: set fileencoding=utf-8
from typing import Optional
from typing_extensions import Final

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.stubs import IIDXResortAnthem

from bemani.common import (
    Profile,
    ValidatedDict,
    VersionConstants,
    Time,
    ID,
)
from bemani.data import Data, UserID
from bemani.protocol import Node


class IIDXLincle(IIDXBase):
    name: str = "Beatmania IIDX Lincle"
    version: int = VersionConstants.IIDX_LINCLE

    GAME_CLTYPE_SINGLE: Final[int] = 0
    GAME_CLTYPE_DOUBLE: Final[int] = 1

    DAN_STAGES_SINGLE: Final[int] = 4
    DAN_STAGES_DOUBLE: Final[int] = 3

    GAME_CLEAR_STATUS_NO_PLAY: Final[int] = 0
    GAME_CLEAR_STATUS_FAILED: Final[int] = 1
    GAME_CLEAR_STATUS_ASSIST_CLEAR: Final[int] = 2
    GAME_CLEAR_STATUS_EASY_CLEAR: Final[int] = 3
    GAME_CLEAR_STATUS_CLEAR: Final[int] = 4
    GAME_CLEAR_STATUS_HARD_CLEAR: Final[int] = 5
    GAME_CLEAR_STATUS_EX_HARD_CLEAR: Final[int] = 6
    GAME_CLEAR_STATUS_FULL_COMBO: Final[int] = 7

    GAME_GHOST_TYPE_RIVAL: Final[int] = 1
    GAME_GHOST_TYPE_GLOBAL_TOP: Final[int] = 2
    GAME_GHOST_TYPE_GLOBAL_AVERAGE: Final[int] = 3
    GAME_GHOST_TYPE_LOCAL_TOP: Final[int] = 4
    GAME_GHOST_TYPE_LOCAL_AVERAGE: Final[int] = 5
    GAME_GHOST_TYPE_DAN_TOP: Final[int] = 6
    GAME_GHOST_TYPE_DAN_AVERAGE: Final[int] = 7
    GAME_GHOST_TYPE_RIVAL_TOP: Final[int] = 8
    GAME_GHOST_TYPE_RIVAL_AVERAGE: Final[int] = 9

    GAME_GHOST_LENGTH: Final[int] = 48

    GAME_SP_DAN_RANK_7_KYU: Final[int] = 0
    GAME_SP_DAN_RANK_6_KYU: Final[int] = 1
    GAME_SP_DAN_RANK_5_KYU: Final[int] = 2
    GAME_SP_DAN_RANK_4_KYU: Final[int] = 3
    GAME_SP_DAN_RANK_3_KYU: Final[int] = 4
    GAME_SP_DAN_RANK_2_KYU: Final[int] = 5
    GAME_SP_DAN_RANK_1_KYU: Final[int] = 6
    GAME_SP_DAN_RANK_1_DAN: Final[int] = 7
    GAME_SP_DAN_RANK_2_DAN: Final[int] = 8
    GAME_SP_DAN_RANK_3_DAN: Final[int] = 9
    GAME_SP_DAN_RANK_4_DAN: Final[int] = 10
    GAME_SP_DAN_RANK_5_DAN: Final[int] = 11
    GAME_SP_DAN_RANK_6_DAN: Final[int] = 12
    GAME_SP_DAN_RANK_7_DAN: Final[int] = 13
    GAME_SP_DAN_RANK_8_DAN: Final[int] = 14
    GAME_SP_DAN_RANK_9_DAN: Final[int] = 15
    GAME_SP_DAN_RANK_10_DAN: Final[int] = 16
    GAME_SP_DAN_RANK_KAIDEN: Final[int] = 17

    GAME_DP_DAN_RANK_5_KYU: Final[int] = 0
    GAME_DP_DAN_RANK_4_KYU: Final[int] = 1
    GAME_DP_DAN_RANK_3_KYU: Final[int] = 2
    GAME_DP_DAN_RANK_2_KYU: Final[int] = 3
    GAME_DP_DAN_RANK_1_KYU: Final[int] = 4
    GAME_DP_DAN_RANK_1_DAN: Final[int] = 5
    GAME_DP_DAN_RANK_2_DAN: Final[int] = 6
    GAME_DP_DAN_RANK_3_DAN: Final[int] = 7
    GAME_DP_DAN_RANK_4_DAN: Final[int] = 8
    GAME_DP_DAN_RANK_5_DAN: Final[int] = 9
    GAME_DP_DAN_RANK_6_DAN: Final[int] = 10
    GAME_DP_DAN_RANK_7_DAN: Final[int] = 11
    GAME_DP_DAN_RANK_8_DAN: Final[int] = 12
    GAME_DP_DAN_RANK_9_DAN: Final[int] = 13
    GAME_DP_DAN_RANK_10_DAN: Final[int] = 14
    GAME_DP_DAN_RANK_KAIDEN: Final[int] = 15

    GAME_CHART_TYPE_N7: Final[int] = 0
    GAME_CHART_TYPE_H7: Final[int] = 1
    GAME_CHART_TYPE_A7: Final[int] = 2
    GAME_CHART_TYPE_N14: Final[int] = 3
    GAME_CHART_TYPE_H14: Final[int] = 4
    GAME_CHART_TYPE_A14: Final[int] = 5
    GAME_CHART_TYPE_B7: Final[int] = 6

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXResortAnthem(self.data, self.config, self.model)

    def db_to_game_status(self, db_status: int) -> int:
        return {
            self.CLEAR_STATUS_NO_PLAY: self.GAME_CLEAR_STATUS_NO_PLAY,
            self.CLEAR_STATUS_FAILED: self.GAME_CLEAR_STATUS_FAILED,
            self.CLEAR_STATUS_ASSIST_CLEAR: self.GAME_CLEAR_STATUS_ASSIST_CLEAR,
            self.CLEAR_STATUS_EASY_CLEAR: self.GAME_CLEAR_STATUS_EASY_CLEAR,
            self.CLEAR_STATUS_CLEAR: self.GAME_CLEAR_STATUS_CLEAR,
            self.CLEAR_STATUS_HARD_CLEAR: self.GAME_CLEAR_STATUS_HARD_CLEAR,
            self.CLEAR_STATUS_EX_HARD_CLEAR: self.GAME_CLEAR_STATUS_EX_HARD_CLEAR,
            self.CLEAR_STATUS_FULL_COMBO: self.GAME_CLEAR_STATUS_FULL_COMBO,
        }[db_status]

    def game_to_db_status(self, game_status: int) -> int:
        return {
            self.GAME_CLEAR_STATUS_NO_PLAY: self.CLEAR_STATUS_NO_PLAY,
            self.GAME_CLEAR_STATUS_FAILED: self.CLEAR_STATUS_FAILED,
            self.GAME_CLEAR_STATUS_ASSIST_CLEAR: self.CLEAR_STATUS_ASSIST_CLEAR,
            self.GAME_CLEAR_STATUS_EASY_CLEAR: self.CLEAR_STATUS_EASY_CLEAR,
            self.GAME_CLEAR_STATUS_CLEAR: self.CLEAR_STATUS_CLEAR,
            self.GAME_CLEAR_STATUS_HARD_CLEAR: self.CLEAR_STATUS_HARD_CLEAR,
            self.GAME_CLEAR_STATUS_EX_HARD_CLEAR: self.CLEAR_STATUS_EX_HARD_CLEAR,
            self.GAME_CLEAR_STATUS_FULL_COMBO: self.CLEAR_STATUS_FULL_COMBO,
        }[game_status]

    def db_to_game_rank(self, db_dan: int, cltype: int) -> int:
        # Special case for no DAN rank
        if db_dan == -1:
            return -1

        if cltype == self.GAME_CLTYPE_SINGLE:
            return {
                self.DAN_RANK_7_KYU: self.GAME_SP_DAN_RANK_7_KYU,
                self.DAN_RANK_6_KYU: self.GAME_SP_DAN_RANK_6_KYU,
                self.DAN_RANK_5_KYU: self.GAME_SP_DAN_RANK_5_KYU,
                self.DAN_RANK_4_KYU: self.GAME_SP_DAN_RANK_4_KYU,
                self.DAN_RANK_3_KYU: self.GAME_SP_DAN_RANK_3_KYU,
                self.DAN_RANK_2_KYU: self.GAME_SP_DAN_RANK_2_KYU,
                self.DAN_RANK_1_KYU: self.GAME_SP_DAN_RANK_1_KYU,
                self.DAN_RANK_1_DAN: self.GAME_SP_DAN_RANK_1_DAN,
                self.DAN_RANK_2_DAN: self.GAME_SP_DAN_RANK_2_DAN,
                self.DAN_RANK_3_DAN: self.GAME_SP_DAN_RANK_3_DAN,
                self.DAN_RANK_4_DAN: self.GAME_SP_DAN_RANK_4_DAN,
                self.DAN_RANK_5_DAN: self.GAME_SP_DAN_RANK_5_DAN,
                self.DAN_RANK_6_DAN: self.GAME_SP_DAN_RANK_6_DAN,
                self.DAN_RANK_7_DAN: self.GAME_SP_DAN_RANK_7_DAN,
                self.DAN_RANK_8_DAN: self.GAME_SP_DAN_RANK_8_DAN,
                self.DAN_RANK_9_DAN: self.GAME_SP_DAN_RANK_9_DAN,
                self.DAN_RANK_10_DAN: self.GAME_SP_DAN_RANK_10_DAN,
                self.DAN_RANK_KAIDEN: self.GAME_SP_DAN_RANK_KAIDEN,
            }[db_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {
                self.DAN_RANK_7_KYU: self.GAME_DP_DAN_RANK_5_KYU,
                self.DAN_RANK_6_KYU: self.GAME_DP_DAN_RANK_5_KYU,
                self.DAN_RANK_5_KYU: self.GAME_DP_DAN_RANK_5_KYU,
                self.DAN_RANK_4_KYU: self.GAME_DP_DAN_RANK_4_KYU,
                self.DAN_RANK_3_KYU: self.GAME_DP_DAN_RANK_3_KYU,
                self.DAN_RANK_2_KYU: self.GAME_DP_DAN_RANK_2_KYU,
                self.DAN_RANK_1_KYU: self.GAME_DP_DAN_RANK_1_KYU,
                self.DAN_RANK_1_DAN: self.GAME_DP_DAN_RANK_1_DAN,
                self.DAN_RANK_2_DAN: self.GAME_DP_DAN_RANK_2_DAN,
                self.DAN_RANK_3_DAN: self.GAME_DP_DAN_RANK_3_DAN,
                self.DAN_RANK_4_DAN: self.GAME_DP_DAN_RANK_4_DAN,
                self.DAN_RANK_5_DAN: self.GAME_DP_DAN_RANK_5_DAN,
                self.DAN_RANK_6_DAN: self.GAME_DP_DAN_RANK_6_DAN,
                self.DAN_RANK_7_DAN: self.GAME_DP_DAN_RANK_7_DAN,
                self.DAN_RANK_8_DAN: self.GAME_DP_DAN_RANK_8_DAN,
                self.DAN_RANK_9_DAN: self.GAME_DP_DAN_RANK_9_DAN,
                self.DAN_RANK_10_DAN: self.GAME_DP_DAN_RANK_10_DAN,
                self.DAN_RANK_KAIDEN: self.GAME_DP_DAN_RANK_KAIDEN,
            }[db_dan]
        else:
            raise Exception("Invalid cltype!")

    def game_to_db_rank(self, game_dan: int, cltype: int) -> int:
        # Special case for no DAN rank
        if game_dan == -1:
            return -1

        if cltype == self.GAME_CLTYPE_SINGLE:
            return {
                self.GAME_SP_DAN_RANK_7_KYU: self.DAN_RANK_7_KYU,
                self.GAME_SP_DAN_RANK_6_KYU: self.DAN_RANK_6_KYU,
                self.GAME_SP_DAN_RANK_5_KYU: self.DAN_RANK_5_KYU,
                self.GAME_SP_DAN_RANK_4_KYU: self.DAN_RANK_4_KYU,
                self.GAME_SP_DAN_RANK_3_KYU: self.DAN_RANK_3_KYU,
                self.GAME_SP_DAN_RANK_2_KYU: self.DAN_RANK_2_KYU,
                self.GAME_SP_DAN_RANK_1_KYU: self.DAN_RANK_1_KYU,
                self.GAME_SP_DAN_RANK_1_DAN: self.DAN_RANK_1_DAN,
                self.GAME_SP_DAN_RANK_2_DAN: self.DAN_RANK_2_DAN,
                self.GAME_SP_DAN_RANK_3_DAN: self.DAN_RANK_3_DAN,
                self.GAME_SP_DAN_RANK_4_DAN: self.DAN_RANK_4_DAN,
                self.GAME_SP_DAN_RANK_5_DAN: self.DAN_RANK_5_DAN,
                self.GAME_SP_DAN_RANK_6_DAN: self.DAN_RANK_6_DAN,
                self.GAME_SP_DAN_RANK_7_DAN: self.DAN_RANK_7_DAN,
                self.GAME_SP_DAN_RANK_8_DAN: self.DAN_RANK_8_DAN,
                self.GAME_SP_DAN_RANK_9_DAN: self.DAN_RANK_9_DAN,
                self.GAME_SP_DAN_RANK_10_DAN: self.DAN_RANK_10_DAN,
                self.GAME_SP_DAN_RANK_KAIDEN: self.DAN_RANK_KAIDEN,
            }[game_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {
                self.GAME_DP_DAN_RANK_5_KYU: self.DAN_RANK_5_KYU,
                self.GAME_DP_DAN_RANK_4_KYU: self.DAN_RANK_4_KYU,
                self.GAME_DP_DAN_RANK_3_KYU: self.DAN_RANK_3_KYU,
                self.GAME_DP_DAN_RANK_2_KYU: self.DAN_RANK_2_KYU,
                self.GAME_DP_DAN_RANK_1_KYU: self.DAN_RANK_1_KYU,
                self.GAME_DP_DAN_RANK_1_DAN: self.DAN_RANK_1_DAN,
                self.GAME_DP_DAN_RANK_2_DAN: self.DAN_RANK_2_DAN,
                self.GAME_DP_DAN_RANK_3_DAN: self.DAN_RANK_3_DAN,
                self.GAME_DP_DAN_RANK_4_DAN: self.DAN_RANK_4_DAN,
                self.GAME_DP_DAN_RANK_5_DAN: self.DAN_RANK_5_DAN,
                self.GAME_DP_DAN_RANK_6_DAN: self.DAN_RANK_6_DAN,
                self.GAME_DP_DAN_RANK_7_DAN: self.DAN_RANK_7_DAN,
                self.GAME_DP_DAN_RANK_8_DAN: self.DAN_RANK_8_DAN,
                self.GAME_DP_DAN_RANK_9_DAN: self.DAN_RANK_9_DAN,
                self.GAME_DP_DAN_RANK_10_DAN: self.DAN_RANK_10_DAN,
                self.GAME_DP_DAN_RANK_KAIDEN: self.DAN_RANK_KAIDEN,
            }[game_dan]
        else:
            raise Exception("Invalid cltype!")

    def game_to_db_chart(self, db_chart: int) -> int:
        return {
            self.GAME_CHART_TYPE_B7: self.CHART_TYPE_B7,
            self.GAME_CHART_TYPE_N7: self.CHART_TYPE_N7,
            self.GAME_CHART_TYPE_H7: self.CHART_TYPE_H7,
            self.GAME_CHART_TYPE_A7: self.CHART_TYPE_A7,
            self.GAME_CHART_TYPE_N14: self.CHART_TYPE_N14,
            self.GAME_CHART_TYPE_H14: self.CHART_TYPE_H14,
            self.GAME_CHART_TYPE_A14: self.CHART_TYPE_A14,
        }[db_chart]

    def handle_shop_getname_request(self, request: Node) -> Node:
        root = Node.void("shop")
        root.set_attribute("cls_opt", "0")
        machine = self.data.local.machine.get_machine(self.config.machine.pcbid)
        root.set_attribute("opname", machine.name)
        root.set_attribute("pid", str(self.get_machine_region()))
        return root

    def handle_shop_savename_request(self, request: Node) -> Node:
        self.update_machine_name(request.attribute("opname"))
        root = Node.void("shop")
        return root

    def handle_shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("shop")

    def handle_ranking_getranker_request(self, request: Node) -> Node:
        root = Node.void("ranking")

        return root

    def handle_music_crate_request(self, request: Node) -> Node:
        root = Node.void("music")
        attempts = self.get_clear_rates()

        all_songs = list(set([song.id for song in self.data.local.music.get_all_songs(self.game, self.music_version)]))
        for song in all_songs:
            clears = []
            fcs = []

            for chart in [0, 1, 2, 3, 4, 5]:
                placed = False
                if song in attempts and chart in attempts[song]:
                    values = attempts[song][chart]
                    if values["total"] > 0:
                        clears.append(int((100 * values["clears"]) / values["total"]))
                        fcs.append(int((100 * values["fcs"]) / values["total"]))
                        placed = True
                if not placed:
                    clears.append(101)
                    fcs.append(101)

            clearnode = Node.u8_array("c", clears + fcs)
            clearnode.set_attribute("mid", str(song))
            root.add_child(clearnode)

        return root

    def handle_music_getrank_request(self, request: Node) -> Node:
        cltype = int(request.attribute("cltype"))

        root = Node.void("music")
        style = Node.void("style")
        root.add_child(style)
        style.set_attribute("type", str(cltype))

        return root

    def handle_music_reg_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        musicid = int(request.attribute("mid"))
        chart = self.game_to_db_chart(int(request.attribute("clid")))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        if userid is not None:
            clear_status = self.game_to_db_status(int(request.attribute("cflg")))
            pgreats = int(request.attribute("pgnum"))
            greats = int(request.attribute("gnum"))
            miss_count = int(request.attribute("mnum"))
            ghost = request.child_value("ghost")

            self.update_score(
                userid,
                musicid,
                chart,
                clear_status,
                pgreats,
                greats,
                miss_count,
                ghost,
                None,
            )

        # Calculate and return statistics about this song
        root = Node.void("music")
        root.set_attribute("clid", request.attribute("clid"))
        root.set_attribute("mid", request.attribute("mid"))

        attempts = self.get_clear_rates(musicid, chart)
        count = attempts[musicid][chart]["total"]
        clear = attempts[musicid][chart]["clears"]
        full_combo = attempts[musicid][chart]["fcs"]

        if count > 0:
            root.set_attribute("crate", str(int((100 * clear) / count)))
            root.set_attribute("frate", str(int((100 * full_combo) / count)))
        else:
            root.set_attribute("crate", "0")
            root.set_attribute("frate", "0")

        return root

    def handle_music_breg_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        musicid = int(request.attribute("mid"))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        if userid is not None:
            clear_status = self.game_to_db_status(int(request.attribute("cflg")))
            pgreats = int(request.attribute("pgnum"))
            greats = int(request.attribute("gnum"))

            self.update_score(
                userid,
                musicid,
                self.CHART_TYPE_B7,
                clear_status,
                pgreats,
                greats,
                -1,
                b"",
                None,
            )

        # Return nothing.
        root = Node.void("music")
        return root

    def handle_music_play_request(self, request: Node) -> Node:
        musicid = int(request.attribute("mid"))
        chart = self.game_to_db_chart(int(request.attribute("clid")))
        clear_status = self.game_to_db_status(int(request.attribute("cflg")))

        self.update_score(
            None,  # No userid since its anonymous
            musicid,
            chart,
            clear_status,
            0,  # No ex score
            0,  # No ex score
            0,  # No miss count
            None,  # No ghost
            None,  # No shop for this user
        )

        # Calculate and return statistics about this song
        root = Node.void("music")
        root.set_attribute("clid", request.attribute("clid"))
        root.set_attribute("mid", request.attribute("mid"))

        attempts = self.get_clear_rates(musicid, chart)
        count = attempts[musicid][chart]["total"]
        clear = attempts[musicid][chart]["clears"]
        full_combo = attempts[musicid][chart]["fcs"]

        if count > 0:
            root.set_attribute("crate", str(int((100 * clear) / count)))
            root.set_attribute("frate", str(int((100 * full_combo) / count)))
        else:
            root.set_attribute("crate", "0")
            root.set_attribute("frate", "0")

        return root

    def handle_music_appoint_request(self, request: Node) -> Node:
        musicid = int(request.attribute("mid"))
        chart = self.game_to_db_chart(int(request.attribute("clid")))
        ghost_type = int(request.attribute("ctype"))
        extid = int(request.attribute("iidxid"))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        root = Node.void("music")

        if userid is not None:
            # Try to look up previous ghost for user
            my_score = self.data.remote.music.get_score(self.game, self.music_version, userid, musicid, chart)
            if my_score is not None:
                mydata = Node.binary("mydata", my_score.data.get_bytes("ghost"))
                mydata.set_attribute("score", str(my_score.points))
                root.add_child(mydata)

            ghost_score = self.get_ghost(
                {
                    self.GAME_GHOST_TYPE_RIVAL: self.GHOST_TYPE_RIVAL,
                    self.GAME_GHOST_TYPE_GLOBAL_TOP: self.GHOST_TYPE_GLOBAL_TOP,
                    self.GAME_GHOST_TYPE_GLOBAL_AVERAGE: self.GHOST_TYPE_GLOBAL_AVERAGE,
                    self.GAME_GHOST_TYPE_LOCAL_TOP: self.GHOST_TYPE_LOCAL_TOP,
                    self.GAME_GHOST_TYPE_LOCAL_AVERAGE: self.GHOST_TYPE_LOCAL_AVERAGE,
                    self.GAME_GHOST_TYPE_DAN_TOP: self.GHOST_TYPE_DAN_TOP,
                    self.GAME_GHOST_TYPE_DAN_AVERAGE: self.GHOST_TYPE_DAN_AVERAGE,
                    self.GAME_GHOST_TYPE_RIVAL_TOP: self.GHOST_TYPE_RIVAL_TOP,
                    self.GAME_GHOST_TYPE_RIVAL_AVERAGE: self.GHOST_TYPE_RIVAL_AVERAGE,
                }.get(ghost_type, self.GHOST_TYPE_NONE),
                request.attribute("subtype"),
                self.GAME_GHOST_LENGTH,
                musicid,
                chart,
                userid,
            )

            # Add ghost score if we support it
            if ghost_score is not None:
                sdata = Node.binary("sdata", ghost_score["ghost"])
                sdata.set_attribute("score", str(ghost_score["score"]))
                if "name" in ghost_score:
                    sdata.set_attribute("name", ghost_score["name"])
                if "pid" in ghost_score:
                    sdata.set_attribute("pid", str(ghost_score["pid"]))
                if "extid" in ghost_score:
                    sdata.set_attribute("riidxid", str(ghost_score["extid"]))
                root.add_child(sdata)

        return root

    def handle_pc_common_request(self, request: Node) -> Node:
        root = Node.void("pc")
        root.set_attribute("expire", "1")

        lincle = Node.void("lincle")
        root.add_child(lincle)
        lincle.set_attribute("phase", "0")

        # Lincle kingdom
        boss = Node.void("boss")
        root.add_child(boss)
        boss.set_attribute("phase", "1")

        return root

    def handle_pc_delete_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_playstart_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_playend_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_oldget_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            oldversion = self.previous_version()
            profile = oldversion.get_profile(userid)
        else:
            profile = None

        root = Node.void("pc")
        root.set_attribute("status", "1" if profile is None else "0")
        return root

    def handle_pc_getname_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            oldversion = self.previous_version()
            profile = oldversion.get_profile(userid)
        else:
            profile = None
        if profile is None:
            raise Exception(
                "Should not get here if we have no profile, we should "
                + "have returned '1' in the 'oldget' method above "
                + "which should tell the game not to present a migration."
            )

        root = Node.void("pc")
        root.set_attribute("name", profile.get_str("name"))
        root.set_attribute("idstr", ID.format_extid(profile.extid))
        root.set_attribute("pid", str(profile.get_int("pid")))
        return root

    def handle_pc_reg_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        name = request.attribute("name")
        pid = int(request.attribute("pid"))
        profile = self.new_profile_by_refid(refid, name, pid)

        root = Node.void("pc")
        if profile is not None:
            root.set_attribute("id", str(profile.extid))
            root.set_attribute("id_str", ID.format_extid(profile.extid))
        return root

    def handle_pc_get_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("pc")
        return root

    def handle_pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        self.put_profile_by_extid(extid, request)

        root = Node.void("pc")
        return root

    def handle_pc_visit_request(self, request: Node) -> Node:
        root = Node.void("pc")
        root.set_attribute("anum", "0")
        root.set_attribute("snum", "0")
        root.set_attribute("pnum", "0")
        root.set_attribute("aflg", "0")
        root.set_attribute("sflg", "0")
        root.set_attribute("pflg", "0")
        return root

    def handle_grade_raised_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        cltype = int(request.attribute("gtype"))
        rank = self.game_to_db_rank(int(request.attribute("gid")), cltype)
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)
        if userid is not None:
            percent = int(request.attribute("achi"))
            stages_cleared = int(request.attribute("cflg"))
            if cltype == self.GAME_CLTYPE_SINGLE:
                max_stages = self.DAN_STAGES_SINGLE
            else:
                max_stages = self.DAN_STAGES_DOUBLE
            cleared = stages_cleared == max_stages

            if cltype == self.GAME_CLTYPE_SINGLE:
                index = self.DAN_RANKING_SINGLE
            else:
                index = self.DAN_RANKING_DOUBLE

            self.update_rank(
                userid,
                index,
                rank,
                percent,
                cleared,
                stages_cleared,
            )

        # Figure out number of players that played this ranking
        all_achievements = self.data.local.user.get_all_achievements(
            self.game, self.version, achievementid=rank, achievementtype=index
        )
        root = Node.void("grade")
        root.set_attribute("pnum", str(len(all_achievements)))
        return root

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("pc")

        # Look up play stats we bridge to every mix
        play_stats = self.get_play_statistics(userid)

        # Profile data
        pcdata = Node.void("pcdata")
        root.add_child(pcdata)
        pcdata.set_attribute("id", str(profile.extid))
        pcdata.set_attribute("idstr", ID.format_extid(profile.extid))
        pcdata.set_attribute("name", profile.get_str("name"))
        pcdata.set_attribute("pid", str(profile.get_int("pid")))
        pcdata.set_attribute("spnum", str(play_stats.get_int("single_plays")))
        pcdata.set_attribute("dpnum", str(play_stats.get_int("double_plays")))
        pcdata.set_attribute("sach", str(play_stats.get_int("single_dj_points")))
        pcdata.set_attribute("dach", str(play_stats.get_int("double_dj_points")))
        pcdata.set_attribute("sflg0", str(profile.get_int("sflg0")))
        pcdata.set_attribute("sflg1", str(profile.get_int("sflg1")))
        pcdata.set_attribute("help", str(profile.get_int("help")))
        pcdata.set_attribute("gno", str(profile.get_int("gno")))
        pcdata.set_attribute("timing", str(profile.get_int("timing")))
        pcdata.set_attribute("sdhd", str(profile.get_int("sdhd")))
        pcdata.set_attribute("sdtype", str(profile.get_int("sdtype")))
        pcdata.set_attribute("notes", str(profile.get_float("notes")))
        pcdata.set_attribute("pase", str(profile.get_int("pase")))
        pcdata.set_attribute("sp_opt", str(profile.get_int("sp_opt")))
        pcdata.set_attribute("dp_opt", str(profile.get_int("dp_opt")))
        pcdata.set_attribute("dp_opt2", str(profile.get_int("dp_opt2")))
        pcdata.set_attribute("mode", str(profile.get_int("mode")))
        pcdata.set_attribute("pmode", str(profile.get_int("pmode")))
        pcdata.set_attribute("liflen", str(profile.get_int("lift")))

        # DAN rankings
        grade = Node.void("grade")
        root.add_child(grade)
        grade.set_attribute(
            "sgid",
            str(
                self.db_to_game_rank(
                    profile.get_int(self.DAN_RANKING_SINGLE, -1),
                    self.GAME_CLTYPE_SINGLE,
                )
            ),
        )
        grade.set_attribute(
            "dgid",
            str(
                self.db_to_game_rank(
                    profile.get_int(self.DAN_RANKING_DOUBLE, -1),
                    self.GAME_CLTYPE_DOUBLE,
                )
            ),
        )
        rankings = self.data.local.user.get_achievements(self.game, self.version, userid)
        for rank in rankings:
            if rank.type == self.DAN_RANKING_SINGLE:
                grade.add_child(
                    Node.u8_array(
                        "g",
                        [
                            self.GAME_CLTYPE_SINGLE,
                            self.db_to_game_rank(rank.id, self.GAME_CLTYPE_SINGLE),
                            rank.data.get_int("stages_cleared"),
                            rank.data.get_int("percent"),
                        ],
                    )
                )
            if rank.type == self.DAN_RANKING_DOUBLE:
                grade.add_child(
                    Node.u8_array(
                        "g",
                        [
                            self.GAME_CLTYPE_DOUBLE,
                            self.db_to_game_rank(rank.id, self.GAME_CLTYPE_DOUBLE),
                            rank.data.get_int("stages_cleared"),
                            rank.data.get_int("percent"),
                        ],
                    )
                )

        ex = Node.void("ex")
        root.add_child(ex)

        # User settings
        settings_dict = profile.get_dict("settings")
        skin = Node.s16_array(
            "skin",
            [
                settings_dict.get_int("frame"),
                settings_dict.get_int("turntable"),
                settings_dict.get_int("burst"),
                settings_dict.get_int("bgm"),
                settings_dict.get_int("flags"),
                settings_dict.get_int("towel"),
                settings_dict.get_int("judge_pos"),
                settings_dict.get_int("voice"),
                settings_dict.get_int("noteskin"),
                settings_dict.get_int("full_combo"),
                settings_dict.get_int("beam"),
                settings_dict.get_int("judge"),
                0,
                settings_dict.get_int("disable_song_preview"),
            ],
        )
        root.add_child(skin)

        # Qpro data
        qpro_dict = profile.get_dict("qpro")
        root.add_child(
            Node.u32_array(
                "qprodata",
                [
                    qpro_dict.get_int("head"),
                    qpro_dict.get_int("hair"),
                    qpro_dict.get_int("face"),
                    qpro_dict.get_int("hand"),
                    qpro_dict.get_int("body"),
                ],
            )
        )

        # Rivals
        rlist = Node.void("rlist")
        root.add_child(rlist)

        fcombo = Node.s16_array("fcombo", [profile.get_int("sp_fcombo"), profile.get_int("dp_fcombo")])
        root.add_child(fcombo)

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        play_stats = self.get_play_statistics(userid)

        # Track play counts, DJ points and options
        cltype = int(request.attribute("cltype"))
        if cltype == self.GAME_CLTYPE_SINGLE:
            play_stats.increment_int("single_plays")
            play_stats.replace_int("single_dj_points", int(request.attribute("achi")))
            newprofile.replace_int("sp_opt", int(request.attribute("opt")))
            newprofile.replace_int("sp_fcombo", int(request.attribute("fcombo")))
        if cltype == self.GAME_CLTYPE_DOUBLE:
            play_stats.increment_int("double_plays")
            play_stats.replace_int("double_dj_points", int(request.attribute("achi")))
            newprofile.replace_int("dp_opt", int(request.attribute("opt")))
            newprofile.replace_int("dp_opt2", int(request.attribute("opt2")))
            newprofile.replace_int("dp_fcombo", int(request.attribute("fcombo")))

        # Profile settings
        newprofile.replace_int("gno", int(request.attribute("gno")))
        newprofile.replace_int("timing", int(request.attribute("timing")))
        newprofile.replace_int("sflg0", int(request.attribute("sflg0")))
        newprofile.replace_int("sflg1", int(request.attribute("sflg1")))
        newprofile.replace_int("help", int(request.attribute("help")))
        newprofile.replace_int("sdhd", int(request.attribute("sdhd")))
        newprofile.replace_int("sdtype", int(request.attribute("sdtype")))
        newprofile.replace_float("notes", float(request.attribute("notes")))
        newprofile.replace_int("pase", int(request.attribute("pase")))
        newprofile.replace_int("mode", int(request.attribute("mode")))
        newprofile.replace_int("pmode", int(request.attribute("pmode")))
        if "lift" in request.attributes:
            newprofile.replace_int("lift", int(request.attribute("lift")))

        # Keep track of play statistics across all mixes
        self.update_play_statistics(userid, play_stats)

        return newprofile
