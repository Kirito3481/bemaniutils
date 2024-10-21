from typing import Any, Dict, Final, List, Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.stubs import IIDXSirius

from bemani.common import (
    Profile,
    ValidatedDict,
    VersionConstants,
    Time,
    ID,
    intish,
)
from bemani.data import UserID
from bemani.protocol import Node


class IIDXResortAnthem(IIDXBase):
    name: str = "Beatmania IIDX Resort Anthem"
    version: int = VersionConstants.IIDX_RESORT_ANTHEM

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
        return IIDXSirius(self.data, self.config, self.model)
    
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

    def handle_shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("shop")

    def handle_music_getrank_request(self, request: Node) -> Node:
        return Node.void("music")

    def handle_pc_common_request(self, request: Node) -> Node:
        root = Node.void("pc")

        ir = Node.void("ir")
        root.add_child(ir)
        ir.set_attribute("beat", "2")  # 0: BEAT#1, 1: BEAT#2, 2: BEAT#3, 3: BEAT#FREE

        lg = Node.void("lg")
        root.add_child(lg)
        lg.set_attribute("lea", "0")

        lf = Node.void("lf")
        root.add_child(lf)
        lf.set_attribute("life", "1")

        ev = Node.void("ev")
        root.add_child(ev)
        ev.set_attribute("pha", "1")

        lincle = Node.void("lincle")
        root.add_child(lincle)
        lincle.set_attribute("phase", "1")

        return root

    def handle_pc_playstart_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_playend_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_delete_request(self, request: Node) -> Node:
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

    def handle_pc_visit_request(self, request: Node) -> Node:
        root = Node.void("pc")
        root.set_attribute("anum", "0")
        root.set_attribute("snum", "0")
        root.set_attribute("pnum", "0")
        root.set_attribute("aflg", "0")
        root.set_attribute("sflg", "0")
        root.set_attribute("pflg", "0")
        return root

    def handle_pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        self.put_profile_by_extid(extid, request)

        root = Node.void("pc")
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
        pcdata.set_attribute("gno", str(profile.get_int("gno")))
        pcdata.set_attribute("timing", str(profile.get_int("timing")))
        pcdata.set_attribute("sdhd", str(profile.get_int("sdhd")))
        pcdata.set_attribute("sp_opt", str(profile.get_int("sp_opt")))
        pcdata.set_attribute("dp_opt", str(profile.get_int("dp_opt")))
        pcdata.set_attribute("dp_opt2", str(profile.get_int("dp_opt2")))
        pcdata.set_attribute("mcomb", str(profile.get_int("mcomb")))
        pcdata.set_attribute("ncomb", str(profile.get_int("ncomb")))
        pcdata.set_attribute("mode", str(profile.get_int("mode")))
        pcdata.set_attribute("pmode", str(profile.get_int("pmode")))
        pcdata.set_attribute("liflen", str(profile.get_int("liflen")))

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
        root.add_child(
            Node.u16_array(
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
                    0,
                    0,
                    0,
                    0,
                ]
            )
        )

        # Rivals
        rlist = Node.void("rlist")
        root.add_child(rlist)

        ocrs = Node.void("ocrs")
        root.add_child(ocrs)

        root.add_child(Node.s16_array("fcombo", [0, 0]))

        party_dict = profile.get_dict("party")
        if party_dict is not None:
            party = Node.void("party")
            root.add_child(party)
            party.set_attribute("ev", str(party_dict.get_int("ev")))
            party.set_attribute("dif", str(party_dict.get_int("dif")))
            party.add_child(Node.binary("cflg", party_dict.get_bytes("cflg")))
            puzzle = Node.void("puzzle")
            party.add_child(puzzle)
            flg = Node.void("flg")
            puzzle.add_child(flg)
            flg.set_attribute("dif", str(party_dict.get_int("pf")))
            flg.set_attribute("cha", str(party_dict.get_int("pc")))

        lincle = Node.void("lincle")
        root.add_child(lincle)
        lincle.set_attribute("comflg", "1")
        lincle.set_attribute("refcomp", "1")

        reflec = Node.void("reflec")
        root.add_child(reflec)
        reflec.set_attribute("tf", "1")  # THE FALLEN
        reflec.set_attribute("br", "1")  # Broken
        reflec.set_attribute("ssc", "1")  # SUPECIAL SUMMER CAMPAIGN!!
        reflec.set_attribute("sr", "1")  # Sakura Reflection
        reflec.set_attribute("wu", "1")  # Wuv U
        reflec.set_attribute("sg", "1")  # Survival Games
        reflec.set_attribute("tb", "1")  # Thunderbolt

        jubeat = Node.void("jubeat")
        root.add_child(jubeat)
        jubeat.set_attribute("jflg_0", "1")
        jubeat.set_attribute("jflg_1", "1")
        jubeat.set_attribute("jflg_2", "1")
        jubeat.set_attribute("jflg_3", "1")

        lglist = Node.void("lglist")
        root.add_child(lglist)

        tour_dict = profile.get_dict("tour")
        if tour_dict is not None:
            tour = Node.void("tour")
            root.add_child(tour)
            tour.set_attribute("pt", str(tour_dict.get_int("pt")))
            tour.set_attribute("rsv", str(tour_dict.get_int("rsv")))
            tour.set_attribute("r0", str(tour_dict.get_int("r0")))
            tour.set_attribute("r1", str(tour_dict.get_int("r1")))
            tour.set_attribute("r2", str(tour_dict.get_int("r2")))
            tour.set_attribute("r3", str(tour_dict.get_int("r3")))
            tour.set_attribute("r4", str(tour_dict.get_int("r4")))
            tour.set_attribute("r5", str(tour_dict.get_int("r5")))
            tour.set_attribute("r6", str(tour_dict.get_int("r6")))
            tour.set_attribute("r7", str(tour_dict.get_int("r7")))
            tour.add_child(Node.binary("cf", tour_dict.get_bytes("cf")))
            tour.add_child(Node.binary("pf", tour_dict.get_bytes("pf")))
            tour.add_child(Node.binary("mf", tour_dict.get_bytes("mf")))

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        play_stats = self.get_play_statistics(userid)

        # Track play counts, DJ points and options
        cltype = int(request.attribute("cltype"))
        if cltype == self.GAME_CLTYPE_SINGLE:
            play_stats.replace_int("single_plays", int(request.attribute("pnum")))
            play_stats.replace_int("single_dj_points", int(request.attribute("achi")))
            newprofile.replace_int("sp_opt", int(request.attribute("opt")))
            newprofile.replace_int("sp_fcombo", int(request.attribute("fcombo")))
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            play_stats.replace_int("double_plays", int(request.attribute("pnum")))
            play_stats.replace_int("double_dj_points", int(request.attribute("achi")))
            newprofile.replace_int("dp_opt", int(request.attribute("opt")))
            newprofile.replace_int("dp_opt2", int(request.attribute("opt2")))
            newprofile.replace_int("dp_fcombo", int(request.attribute("fcombo")))

        # Profile settings
        newprofile.replace_int("gno", int(request.attribute("gno")))
        newprofile.replace_int("timing", int(request.attribute("timing")))
        newprofile.replace_int("sflg0", int(request.attribute("sflg0")))
        newprofile.replace_int("sflg1", int(request.attribute("sflg1")))
        newprofile.replace_int("sdhd", int(request.attribute("sdhd")))
        newprofile.replace_int("ncomb", int(request.attribute("ncomb")))
        newprofile.replace_int("mcomb", int(request.attribute("mcomb")))
        newprofile.replace_int("mode", int(request.attribute("mode")))
        newprofile.replace_int("pmode", int(request.attribute("pmode")))
        if "lift" in request.attributes:
            newprofile.replace_int("lift", int(request.attribute("lift")))

        lincle = request.child("lincle")
        if lincle is not None:
            lincle_dict = newprofile.get_dict("lincle")
            lincle_dict.replace_int("flg1", int(lincle.attribute("flg1")))
            lincle_dict.replace_int("flg2", int(lincle.attribute("flg2")))
            lincle_dict.replace_int("flg3", int(lincle.attribute("flg3")))
            lincle_dict.replace_int("flg4", int(lincle.attribute("flg4")))
            lincle_dict.replace_int("flg5", int(lincle.attribute("flg5")))
            lincle_dict.replace_int("flg6", int(lincle.attribute("flg6")))
            lincle_dict.replace_int("flg7", int(lincle.attribute("flg7")))
            newprofile.replace_dict("lincle", lincle_dict)

        party = request.child("party")
        if party is not None:
            party_dict = newprofile.get_dict("party")
            party_dict.replace_int("ev", int(party.attribute("ev")))
            party_dict.replace_int("dif", int(party.attribute("dif")))
            party_dict.replace_int("pc", int(party.attribute("pc")))  # puzzle cha?
            party_dict.replace_int("pf", int(party.attribute("pf")))  # puzzle dif?
            party_dict.replace_bytes("cflg", party.value)
            newprofile.replace_dict("party", party_dict)

        tour = request.child("tour")
        if tour is not None:
            tour_dict = newprofile.get_dict("tour")
            tour_dict.replace_int("pt", int(tour.attribute("pt")))
            tour_dict.replace_int("rsv", int(tour.attribute("rsv")))
            tour_dict.replace_int("r0", int(tour.attribute("r0")))
            tour_dict.replace_int("r1", int(tour.attribute("r1")))
            tour_dict.replace_int("r2", int(tour.attribute("r2")))
            tour_dict.replace_int("r3", int(tour.attribute("r3")))
            tour_dict.replace_int("r4", int(tour.attribute("r4")))
            tour_dict.replace_int("r5", int(tour.attribute("r5")))
            tour_dict.replace_int("r6", int(tour.attribute("r6")))
            tour_dict.replace_int("r7", int(tour.attribute("r7")))
            tour_dict.replace_bytes("cf", tour.child_value("cf"))
            tour_dict.replace_bytes("pf", tour.child_value("pf"))
            tour_dict.replace_bytes("mf", tour.child_value("mf"))
            newprofile.replace_dict("tour", tour_dict)

        # Keep track of play statistics across all mixes
        self.update_play_statistics(userid, play_stats)

        return newprofile
