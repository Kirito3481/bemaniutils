from typing import Any, Dict, Final, List, Optional

from flask.sessions import SecureCookieSessionInterface

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.stubs import IIDXResortAnthem

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

    def handle_shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("shop")

    def handle_shop_getname_request(self, request: Node) -> Node:
        machine = self.data.local.machine.get_machine(self.config.machine.pcbid)
        if machine is not None:
            machine_name = machine.name
            close = machine.data.get_bool("close")
            hour = machine.data.get_int("hour")
            minute = machine.data.get_int("minute")
        else:
            machine_name = ""
            close = False
            hour = 0
            minute = 0

        root = Node.void("shop")
        root.set_attribute("opname", machine_name)
        root.set_attribute("pid", str(self.get_machine_region()))
        root.set_attribute("cls_opt", "1" if close else "0")
        root.set_attribute("hr", str(hour))
        root.set_attribute("mi", str(minute))
        return root

    def handle_shop_savename_request(self, request: Node) -> Node:
        self.update_machine_name(request.attribute("opname"))

        shop_close = intish(request.attribute("cls_opt")) or 0
        minutes = intish(request.attribute("mnt")) or 0
        hours = intish(request.attribute("hr")) or 0

        self.update_machine_data(
            {
                "close": shop_close != 0,
                "minutes": minutes,
                "hours": hours,
            }
        )

        return Node.void("shop")

    def handle_ranking_getranker_request(self, request: Node) -> Node:
        chart = self.game_to_db_chart(int(request.attribute("clid")))

        root = Node.void("ranking")

        if chart not in [
            self.CHART_TYPE_N7,
            self.CHART_TYPE_H7,
            self.CHART_TYPE_A7,
            self.CHART_TYPE_N14,
            self.CHART_TYPE_H14,
            self.CHART_TYPE_A14,
        ]:
            # Chart type 6 is presumably beginner mode, but it crashes the game
            return root

        machine = self.data.local.machine.get_machine(self.config.machine.pcbid)
        if machine is not None:
            if machine.arcade is not None:
                course = self.data.local.machine.get_settings(machine.arcade, self.game, self.music_version, "shop_course")
            else:
                course = None

            if course is None:
                course = ValidatedDict()

            if not course.get_bool("valid"):
                # Shop course not enabled or not present
                return root

            convention = Node.void("convention")
            root.add_child(convention)
            convention.set_attribute("clid", str(chart))
            convention.set_attribute("update_date", str(Time.now() * 1000))

            # Grab all scores for each of the four songs, filter all scores not achieved
            # on this machine and then return the top 20 scores (adding all 4 songs).
            songids = [
                course.get_int("music_0"),
                course.get_int("music_1"),
                course.get_int("music_2"),
                course.get_int("music_3"),
            ]

            totalscores: Dict[UserID, int] = {}
            profiles: Dict[UserID, Profile] = {}
            for songid in songids:
                scores = self.data.local.music.get_all_scores(
                    self.game,
                    self.music_version,
                    songid=songid,
                    songchart=chart,
                )

                for score in scores:
                    # Exclude scores not achieved here
                    if score[1].location != machine.id:
                        continue
                    if score[0] not in totalscores:
                        totalscores[score[0]] = 0
                        profile = self.get_any_profile(score[0])
                        if profile is None:
                            profile = Profile(self.game, self.version, "", 0)
                        profiles[score[0]] = profile

                    totalscores[score[0]] += score[1].points

            topscores = sorted(
                [(totalscores[userid], profiles[userid]) for userid in totalscores],
                key=lambda tup: tup[0],
                reverse=True,
            )[:20]

            rank = 0
            for topscore in topscores:
                rank = rank + 1

                detail = Node.void("detail")
                convention.add_child(detail)
                detail.set_attribute("name", topscore[1].get_str("name"))
                detail.set_attribute("rank", str(rank))
                detail.set_attribute("score", str(topscore[0]))
                detail.set_attribute("pid", str(topscore[1].get_int("pid")))

                qpro = topscore[1].get_dict("qpro")
                detail.set_attribute("head", str(qpro.get_int("head")))
                detail.set_attribute("hair", str(qpro.get_int("hair")))
                detail.set_attribute("face", str(qpro.get_int("face")))
                detail.set_attribute("body", str(qpro.get_int("body")))
                detail.set_attribute("hand", str(qpro.get_int("hand")))

        return root

    def handle_music_crate_request(self, request: Node) -> Node:
        root = Node.void("music")
        attempts = self.get_clear_rates()

        return root

    def handle_music_getrank_request(self, request: Node) -> Node:
        cltype = int(request.attribute("cltype"))

        root = Node.void("music")

        for rivalid in [-1, 0, 1, 2, 3, 4]:
            if rivalid == -1:
                attr = "iidxid"
            else:
                attr = f"iidxid{rivalid}"

            try:
                extid = int(request.attribute(attr))
            except Exception:
                # Invalid extid
                continue

            userid = self.data.remote.user.from_extid(self.game, self.version, extid)
            if userid is not None:
                scores = self.data.remote.music.get_scores(self.game, self.music_version, userid)

                # Grab score data for user/rival
                scoredata = self.make_score_struct(
                    scores,
                    self.CLEAR_TYPE_SINGLE if cltype == self.GAME_CLTYPE_SINGLE else self.CLEAR_TYPE_DOUBLE,
                    rivalid,
                )
                for s in scoredata:
                    root.add_child(Node.s16_array("m", s))

                # Grab most played for user/rival
                most_played = [
                    play[0] for play in self.data.local.music.get_most_played(self.game, self.music_version, userid, 20)
                ]
                if len(most_played) < 20:
                    most_played.extend([0] * (20 - len(most_played)))
                best = Node.u16_array("best", most_played)
                best.set_attribute("rno", str(rivalid))
                root.add_child(best)

                if rivalid == -1:
                    # Grab beginner statuses for user only
                    beginnerdata = self.make_beginner_struct(scores)
                    for b in beginnerdata:
                        root.add_child(Node.u16_array("b", b))

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
                None
            )

        root = Node.void("muisc")
        root.set_attribute("mid", str(musicid))
        root.set_attribute("clid", str(chart))

        attemps = self.get_clear_rates(musicid, chart)
        count = attemps[musicid][chart]["total"]
        clear = attemps[musicid][chart]["clears"]
        full_combo = attemps[musicid][chart]["fcs"]

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

        return Node.void("music")

    def handle_pc_common_request(self, request: Node) -> Node:
        root = Node.void("pc")

        # Monthly music ranking
        root.add_child(Node.u16_array("mranking", [0] * 20))

        courses: List[Dict[str, Any]] = [
            {
                "id": 1,
                "name": "Expert Course",
                "music_0": 1919,
                "music_1": 1919,
                "music_2": 1919,
                "music_3": 1919,
                "music_4": 1919,
                "open": True,
            }
        ]

        # Monthly expert course
        mexpert = Node.void("mexpert")
        root.add_child(mexpert)
        for course in courses:

            coursenode = Node.void("course")
            mexpert.add_child(coursenode)
            coursenode.set_attribute("me_id", str(course["id"]))
            coursenode.set_attribute("name", course["name"])
            coursenode.set_attribute("mid0", str(course["music_0"]))
            coursenode.set_attribute("mid1", str(course["music_1"]))
            coursenode.set_attribute("mid2", str(course["music_2"]))
            coursenode.set_attribute("mid3", str(course["music_3"]))
            coursenode.set_attribute("mid4", str(course["music_4"]))
            coursenode.set_attribute("opflg", str(1 if course["open"] else 0))

        # What is this
        # daily = Node.void("daily")
        # root.add_child(daily)
        # daily.set_attribute("mid", "0")

        ir = Node.void("ir")
        root.add_child(ir)
        ir.set_attribute("beat", "0")

        # cm = Node.void("cm")
        # root.add_child(cm)
        # cm.set_attribute("id", "0")
        # cm.set_attribute("folder", "0")
        # cm.set_attribute("compo", "0")

        # secret = Node.void("secret")
        # root.add_child(secret)
        # secret.add_child(Node.u16_array("mid", [0] * 6))
        # secret.add_child(Node.bool_array("open", [False] * 6))

        # Lincle LINK
        lincle = Node.void("lincle")
        root.add_child(lincle)
        lincle.set_attribute("phase", "2")  # 1 - third time, 2 - 4th time, 3 - 5th time (Game Crash)

        # Lincle Kingdom
        # boss = Node.void("boss")
        # root.add_child(boss)
        # boss.set_attribute("phase", "0")  # 1 - Event Start

        # monex = Node.void("monex")
        # root.add_child(monex)
        # monex.set_attribute("no", "1")

        # mr_secret = Node.void("mr_secret")
        # root.add_child(mr_secret)
        # mr_secret.set_attribute("flg", "0")

        # travel = Node.void("travel")
        # root.add_child(travel)
        # travel.set_attribute("flg", "1")

        return root

    def handle_pc_playstart_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_playend_request(self, request: Node) -> Node:
        return Node.void("pc")

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
            Node.s16_array(
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
                ]
            )
        )

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
                ]
            )
        )

        rlist = Node.void("rlist")
        root.add_child(rlist)

        # rival = Node.void("rival")
        # rlist.add_child(rival)
        # rival.set_attribute("spdp", "1")  # 1 - Single, 2 - Double
        # rival.set_attribute("id", "84388293")
        # rival.set_attribute("id_str", "8438-8293")
        # rival.set_attribute("djname", "TEST1")
        # rival.set_attribute("pid", "49")
        # rival.set_attribute("sg", "-1")
        # rival.set_attribute("dg", "-1")
        # rival.set_attribute("sa", "0")
        # rival.set_attribute("da", "0")
        # stepdata = Node.void("stepdata")
        # rival.add_child(stepdata)
        # stepdata.set_attribute("step_sach", "0")
        # stepdata.set_attribute("step_dach", "0")
        # qprodata = Node.void("qprodata")
        # rival.add_child(qprodata)
        # qprodata.set_attribute("head", "0")
        # qprodata.set_attribute("hair", "0")
        # qprodata.set_attribute("face", "0")
        # qprodata.set_attribute("body", "0")
        # qprodata.set_attribute("hand", "0")
        # comment = Node.void("comment")
        # rival.add_child(comment)
        # comment.set_attribute("play1", "")
        # comment.set_attribute("play2", "")
        # comment.set_attribute("play3", "")
        # comment.set_attribute("win", "")
        # comment.set_attribute("lose", "")
        # phase2 = Node.void("phase2")
        # rival.add_child(phase2)
        # phase2.set_attribute("ryellow", "0")

        # ocrs = Node.void("ocrs")
        # root.add_child(ocrs)

        # flist = Node.void("flist")
        # root.add_child(flist)

        # weekly = Node.void("weekly")
        # root.add_child(weekly)
        # weekly.set_attribute("wid", "1")
        # weekly.set_attribute("mid", "1000")

        # visitor = Node.void("visitor")
        # root.add_child(visitor)
        # visitor.set_attribute("anum", "0")
        # visitor.set_attribute("snum", "0")
        # visitor.set_attribute("pnum", "0")
        # visitor.set_attribute("vs_flg", "1")

        # attack = Node.void("attack")
        # root.add_child(attack)
        # attack.set_attribute("a0", "1")
        # attack.set_attribute("a1", "2")
        # attack.set_attribute("a2", "3")
        # attack.set_attribute("a3", "4")
        # attack.set_attribute("a4", "5")
        # attack.set_attribute("a5", "6")
        # attack.set_attribute("a6", "7")

        root.add_child(
            Node.s16_array(
                "fcombo",
                [
                    profile.get_int("sp_fcombo"),
                    profile.get_int("dp_fcombo"),
                ]
            )
        )

        step_dict = profile.get_dict("step")
        if step_dict is not None:
            step = Node.void("step")
            root.add_child(step)
            step.set_attribute("sp_ach", str(step_dict.get_int("sp_ach")))
            step.set_attribute("dp_ach", str(step_dict.get_int("dp_ach")))
            step.set_attribute("sp_dif", str(step_dict.get_int("sp_dif")))
            step.set_attribute("dp_dif", str(step_dict.get_int("dp_dif")))
            step.add_child(
                Node.u8_array(
                    "hdpt",
                    [
                        step_dict.get_int("sp_hand0"),
                        step_dict.get_int("sp_hand1"),
                        step_dict.get_int("sp_hand2"),
                        step_dict.get_int("sp_hand3"),
                        step_dict.get_int("sp_hand4"),
                        step_dict.get_int("dp_hand0"),
                        step_dict.get_int("dp_hand1"),
                        step_dict.get_int("dp_hand2"),
                        step_dict.get_int("dp_hand3"),
                        step_dict.get_int("dp_hand4"),
                    ]
                )
            )
            step.add_child(Node.binary("sp_cflg", step_dict.get_bytes("sp_cflg")))
            step.add_child(Node.binary("dp_cflg", step_dict.get_bytes("dp_cflg")))

        lincle_dict = profile.get_dict("lincle")
        if lincle_dict is not None:
            lincle = Node.void("lincle")
            root.add_child(lincle)
            lincle.set_attribute("comflg", "0")
            lincle.set_attribute("flg1", str(lincle_dict.get_int("flg1")))
            lincle.set_attribute("flg2", str(lincle_dict.get_int("flg2")))
            lincle.set_attribute("flg3", str(lincle_dict.get_int("flg3")))
            lincle.set_attribute("flg4", str(lincle_dict.get_int("flg4")))
            lincle.set_attribute("flg5", str(lincle_dict.get_int("flg5")))
            lincle.set_attribute("flg6", str(lincle_dict.get_int("flg6")))
            lincle.set_attribute("flg7", str(lincle_dict.get_int("flg7")))

        reflec = Node.void("reflec")
        root.add_child(reflec)
        reflec.set_attribute("tf", "0")
        reflec.set_attribute("br", "0")
        reflec.set_attribute("ssc", "0")
        reflec.set_attribute("sr", "0")
        reflec.set_attribute("wu", "0")
        reflec.set_attribute("sg", "0")
        reflec.set_attribute("tb", "0")

        # phase2 = Node.void("phase2")
        # root.add_child(phase2)
        # phase2.set_attribute("wonder", "0")
        # phase2.set_attribute("yellow", "0")

        jubeat = Node.void("jubeat")
        root.add_child(jubeat)
        jubeat.set_attribute("point", "0")
        jubeat.set_attribute("bonus", "0")  # DELLAR BONUS
        jubeat.set_attribute("jbonus", str(profile.get_int("jubeat_point")))  # ACHIEVEMENT POINTS BONUS
        jubeat.set_attribute("open", "0")

        # phase4 = Node.void("phase4")
        # root.add_child(phase4)
        # phase4.set_attribute("qpro", "0")
        # phase4.set_attribute("glass", "0")
        # phase4.set_attribute("treasure", "0")
        # phase4.set_attribute("beautiful", "0")
        # phase4.set_attribute("quaver", "0")
        # phase4.set_attribute("castle", "0")
        # phase4.set_attribute("flip", "0")
        # phase4.set_attribute("titans", "0")
        # phase4.set_attribute("exusia", "0")
        # phase4.set_attribute("waxing", "0")
        # phase4.set_attribute("sampling", "0")
        # phase4.set_attribute("beachside", "0")
        # phase4.set_attribute("cuvelia", "0")
        # phase4.set_attribute("reunion", "0")
        # phase4.set_attribute("bad", "0")
        # phase4.set_attribute("turii", "0")
        # phase4.set_attribute("anisakis", "0")
        # phase4.set_attribute("second", "0")
        # phase4.set_attribute("whydidyou", "0")
        # phase4.set_attribute("china", "0")
        # phase4.set_attribute("fallen", "0")
        # phase4.set_attribute("broken", "0")
        # phase4.set_attribute("summer", "0")
        # phase4.set_attribute("sakura", "0")
        # phase4.set_attribute("wuv", "0")
        # phase4.set_attribute("survival", "0")
        # phase4.set_attribute("thunder", "0")
        # phase4.set_attribute("qproflg", "0")
        # phase4.set_attribute("glassflg", "0")

        kingdom_dict = profile.get_dict("kingdom")
        if kingdom_dict is not None:
            kingdom = Node.void("kingdom")
            root.add_child(kingdom)
            kingdom.set_attribute("level", str(kingdom_dict.get_int("level")))
            kingdom.set_attribute("exp", str(kingdom_dict.get_int("exp")))
            kingdom.set_attribute("deller", str(kingdom_dict.get_int("deller")))
            kingdom.set_attribute("place", str(kingdom_dict.get_int("place")))
            kingdom.set_attribute("tower", str(kingdom_dict.get_int("tower")))
            kingdom.set_attribute("boss", str(kingdom_dict.get_int("boss")))
            kingdom.set_attribute("combo", str(kingdom_dict.get_int("combo")))
            kingdom.set_attribute("jewel", str(kingdom_dict.get_int("jewel")))
            kingdom.set_attribute("generic", str(kingdom_dict.get_int("generic")))
            kingdom.add_child(Node.binary("cf", kingdom_dict.get_bytes("cf")))
            kingdom.add_child(Node.binary("qcf", kingdom_dict.get_bytes("qcf")))
            kingdom.add_child(Node.binary("piece", kingdom_dict.get_bytes("piece")))

        # shop = Node.void("shop")
        # root.add_child(shop)
        # shop.set_attribute("spitem", "0")
        # shop.add_child(Node.u8_array("item", [0, 0, 0]))

        # event = Node.void("event")
        # root.add_child(event)
        # event.set_attribute("knee", "0")
        # event.set_attribute("lethe", "0")
        # event.set_attribute("resist", "0")
        # event.set_attribute("jknee", "0")
        # event.set_attribute("jlethe", "0")
        # event.set_attribute("jresist", "0")

        # root.add_child(Node.void("travel"))

        # history = Node.void("history")
        # root.add_child(history)
        # history.add_child(Node.u8_array("type", [0] * 30))
        # history.add_child(Node.time_array("time", [0] * 30))
        # history.add_child(Node.s32_array("param0", [0] * 30))
        # history.add_child(Node.s32_array("param1", [0] * 30))
        # history.add_child(Node.s32_array("param2", [0] * 30))
        # history.add_child(Node.s32_array("param3", [0] * 30))
        # history.add_child(Node.s32_array("param4", [0] * 30))

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
        newprofile.replace_int("help", int(request.attribute("help")))
        newprofile.replace_int("sdhd", int(request.attribute("sdhd")))
        newprofile.replace_int("sdtype", int(request.attribute("sdtype")))
        newprofile.replace_float("notes", float(request.attribute("notes")))
        newprofile.replace_int("pase", int(request.attribute("pase")))
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

        jpoint = request.child("jpoint")
        if jpoint is not None:
            newprofile.replace_int("jubeat_point", int(jpoint.attribute("point")))

        step = request.child("step")
        if step is not None:
            step_dict = newprofile.get_dict("step")
            if cltype == self.GAME_CLTYPE_SINGLE:
                step_dict.replace_int("sp_ach", int(step.attribute("sp_ach")))
                step_dict.replace_int("sp_dif", int(step.attribute("sp_dif")))
                step_dict.replace_int("sp_hand0", int(step.attribute("sp_hand0")))
                step_dict.replace_int("sp_hand1", int(step.attribute("sp_hand1")))
                step_dict.replace_int("sp_hand2", int(step.attribute("sp_hand2")))
                step_dict.replace_int("sp_hand3", int(step.attribute("sp_hand3")))
                step_dict.replace_int("sp_hand4", int(step.attribute("sp_hand4")))
                step_dict.replace_bytes("sp_cflg", step.value)
            else:
                step_dict.replace_int("dp_ach", int(step.attribute("dp_ach")))
                step_dict.replace_int("dp_dif", int(step.attribute("dp_dif")))
                step_dict.replace_int("dp_hand0", int(step.attribute("dp_hand0")))
                step_dict.replace_int("dp_hand1", int(step.attribute("dp_hand1")))
                step_dict.replace_int("dp_hand2", int(step.attribute("dp_hand2")))
                step_dict.replace_int("dp_hand3", int(step.attribute("dp_hand3")))
                step_dict.replace_int("dp_hand4", int(step.attribute("dp_hand4")))
                step_dict.replace_bytes("dp_cflg", step.value)

            newprofile.replace_dict("step", step_dict)

        kingdom = request.child("kingdom")
        if kingdom is not None:
            kingdom_dict = newprofile.get_dict("kingdom")
            kingdom_dict.replace_int("level", int(kingdom.attribute("level")))
            kingdom_dict.replace_int("exp", int(kingdom.attribute("exp")))
            kingdom_dict.replace_int("deller", int(kingdom.attribute("deller")))
            kingdom_dict.replace_int("place", int(kingdom.attribute("place")))
            kingdom_dict.replace_int("tower", int(kingdom.attribute("tower")))
            kingdom_dict.replace_int("boss", int(kingdom.attribute("boss")))
            kingdom_dict.replace_int("combo", int(kingdom.attribute("combo")))
            kingdom_dict.replace_int("jewel", int(kingdom.attribute("jewel")))
            kingdom_dict.replace_int("generic", int(kingdom.attribute("generic")))
            kingdom_dict.replace_bytes("cf", kingdom.child_value("cf"))
            kingdom_dict.replace_bytes("qcf", kingdom.child_value("qcf"))
            kingdom_dict.replace_bytes("piece", kingdom.child_value("piece"))
            newprofile.replace_dict("kingdom", kingdom_dict)

        # Keep track of play statistics across all mixes
        self.update_play_statistics(userid, play_stats)

        return newprofile
