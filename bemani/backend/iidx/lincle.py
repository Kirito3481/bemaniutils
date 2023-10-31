# vim: set fileencoding=utf-8
from typing import Optional, Dict, List, Tuple, Any
from typing_extensions import Final

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.course import IIDXCourse
from bemani.backend.iidx.stubs import IIDXResortAnthem

from bemani.common import (
    Profile,
    ValidatedDict,
    VersionConstants,
    Time,
    ID
)
from bemani.data import Data, UserID
from bemani.protocol import Node


class IIDXLincle(IIDXCourse, IIDXBase):
    name: str = "Beatmania IIDX 19 Lincle"
    version: int = VersionConstants.IIDX_LINCLE

    GAME_CLTYPE_SINGLE: Final[int] = 0
    GAME_CLTYPE_DOUBLE: Final[int] = 1

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

    GAME_GHOST_LENGTH: Final[int] = 124

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

            }[db_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {

            }[db_dan]
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

    def __expert_course_list(self, ) -> List[Dict[str, Any]]:
        return [
            {
                "id": 1,
                "name": "VOCAL",
                "opflg": True,
                "songs": [
                    1919,
                    1925,
                    1945,
                    1910,
                    1918,
                ]
            }
        ]

    def handle_shop_getname_request(self, request: Node) -> Node:
        root = Node.void("shop")

        machine = self.data.local.machine.get_machine(self.config.machine.pcbid)
        root.set_attribute("opname", machine.name)
        root.set_attribute("pid", str(self.get_machine_region()))
        root.set_attribute("cls_opt", str(machine.data.get_int("cls_opt")))
        if machine.data.get_int("cls_opt") == 1:
            root.set_attribute("hr", str(machine.data.get_int("hr")))
            root.set_attribute("mi", str(machine.data.get_int("mi")))

        return root

    def handle_shop_savename_request(self, request: Node) -> Node:
        self.update_machine_name(request.attribute("opname"))
        return Node.void("shop")

    def handle_shop_keepalive_request(self, request: Node) -> Node:
        return Node.void("shop")

    def handle_shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("shop")

    def handle_ranking_getranker_request(self, request: Node) -> Node:
        root = Node.void("ranking")

        return root

    def handle_music_crate_request(self, request: Node) -> Node:
        root = Node.void("music")
        attempts = self.get_clear_rates()

        all_songs = list(
            set(
                [
                    song.id
                    for song in self.data.local.music.get_all_songs(
                        self.game, self.music_version
                    )
                ]
            )
        )
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

            clear = Node.u8_array("c", clears + fcs)
            clear.set_attribute("mid", str(song))
            root.add_child(clear)

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
                scores = self.data.remote.music.get_scores(
                    self.game, self.music_version, userid
                )

                # Grab score data for user/rival
                scoredata = self.make_score_struct(
                    scores,
                    self.CLEAR_TYPE_SINGLE
                    if cltype == self.GAME_CLTYPE_SINGLE
                    else self.CLEAR_TYPE_DOUBLE,
                    rivalid,
                )
                for s in scoredata:
                    root.add_child(Node.s16_array("m", s))

                # Grab most played for user/rival
                most_played = [
                    play[0]
                    for play in self.data.local.music.get_most_played(
                        self.game, self.music_version, userid, 20
                    )
                ]
                if len(most_played) < 20:
                    most_played.extend([0] * (20 - len(most_played)))
                best = Node.u16_array("best", most_played)
                best.set_attribute("rno", str(rivalid))
                root.add_child(best)

                if rivalid == -1:
                    # Grab beginner status for user only
                    beginnerdata = self.make_beginner_struct(scores)
                    for b in beginnerdata:
                        root.add_child(Node.u16_array("b", b))

        return root

    def handle_music_reg_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        musicid = int(request.attribute("mid"))
        chart = self.game_to_db_chart(int(request.attribute("clid")))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        # See if we need to report global or shop scores
        if self.machine_joined_arcade():
            game_config = self.get_game_config()
            global_scores = game_config.get_bool("global_shop_ranking")
            machine = self.data.local.machine.get_machine(self.config.machine.pcbid)
        else:
            # If we aren't in an arcade, we can only show global scores
            global_scores = True
            machine = None

        # First, determine our current ranking before saving the new score
        all_scores = sorted(
            self.data.remote.music.get_all_scores(
                game=self.game,
                version=self.music_version,
                songid=musicid,
                songchart=chart,
            ),
            key=lambda s: (s[1].points, s[1].timestamp),
            reverse=True,
        )
        all_players = {
            uid: prof
            for (uid, prof) in self.get_any_profiles([s[0] for s in all_scores])
        }

        if not global_scores:
            all_scores = [
                score
                for score in all_scores
                if (
                    score[0] == userid
                    or self.user_joined_arcade(machine, all_players[score[0]])
                )
            ]

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
                ghost
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
        return Node.void("music")

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
            my_score = self.data.remote.music.get_score(
                self.game, self.music_version, userid, musicid, chart
            )
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
        root.set_attribute("expire", "600")

        # Top ranking musics
        mranking = Node.u16_array("mranking", [0] * 20)
        root.add_child(mranking)

        # expert course (max 30)
        mexpert = Node.void("mexpert")
        root.add_child(mexpert)

        for c in self.__expert_course_list():
            if c["id"] < 0 or c["id"] >= 20:
                raise Exception("Course ID is out of bounds!")

            course = Node.void("course")
            mexpert.add_child(course)
            course.set_attribute("me_id", str(c["id"]))
            course.set_attribute("name", str(c["name"]))
            course.set_attribute("mid0", str(c["songs"][0]))
            course.set_attribute("mid1", str(c["songs"][1]))
            course.set_attribute("mid2", str(c["songs"][2]))
            course.set_attribute("mid3", str(c["songs"][3]))
            course.set_attribute("mid4", str(c["songs"][4]))
            course.set_attribute("opflg", "1" if c["opflg"] else "0")

        # Daily music
        daily = Node.void("daily")
        root.add_child(daily)
        daily.set_attribute("mid", "0")

        # IR
        ir = Node.void("ir")
        root.add_child(ir)
        ir.set_attribute("beat", "2")

        # i don't know what is this
        cm = Node.void("cm")
        root.add_child(cm)
        cm.set_attribute("id", "0")
        cm.set_attribute("folder", "0")
        cm.set_attribute("compo", "0")

        secret = Node.void("secret")
        root.add_child(secret)
        secret.add_child(Node.u16_array("mid", [0] * 6))
        secret.add_child(Node.bool_array("open", [False] * 6))

        # Lincle LINK Event (maybe)
        lincle = Node.void("lincle")
        root.add_child(lincle)
        lincle.set_attribute("phase", "0")

        # Lincle Kingdom Event (maybe)
        boss = Node.void("boss")
        root.add_child(boss)
        boss.set_attribute("phase", "0")

        # i don't know what is this
        monex = Node.void("monex")
        root.add_child(monex)
        monex.set_attribute("no", "0")

        # i don't know what is this
        mr_secret = Node.void("mr_secret")
        root.add_child(mr_secret)
        mr_secret.set_attribute("flg", "0")

        # Append Travel Event (maybe)
        travel = Node.void("travel")
        root.add_child(travel)
        travel.set_attribute("flg", "0")

        return root

    def handle_pc_delete_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_playstart_request(self, request: Node) -> Node:
        return Node.void("pc")

    def handle_pc_playend_request(self, request: Node) -> Node:
        return Node.void("pc")

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
                + "have returned '1' in the 'oldget' method avobe "
                + "which should tell the game not to present a migration."
            )

        root = Node.void("pc")
        root.set_attribute("name", profile.get_str("name"))
        root.set_attribute("idstr", ID.format_extid(profile.extid))
        root.set_attribute("pid", str(profile.get_int("pid")))
        return root

    def handle_pc_takeover_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        name = request.attribute("name")
        pid = int(request.attribute("pid"))
        newprofile = self.new_profile_by_refid(refid, name, pid)

        root = Node.void("pc")
        if newprofile is not None:
            root.set_attribute("id", str(newprofile.extid))
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
            root = Node.void("root")
        return root

    def handle_pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        self.put_profile_by_extid(extid, request)

        return Node.void("pc")

    def handle_pc_visit_request(self, request: Node) -> Node:
        root = Node.void("pc")
        root.set_attribute("anum", "0")
        root.set_attribute("snum", "0")
        root.set_attribute("pnum", "0")
        root.set_attribute("aflg", "0")
        root.set_attribute("sflg", "0")
        root.set_attribute("pflg", "0")

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
        pcdata.set_attribute("name", profile.get_str("name", "IIDX"))
        pcdata.set_attribute("pid", str(profile.get_int("pid")))
        pcdata.set_attribute("spnum", str(profile.get_int("single_plays")))
        pcdata.set_attribute("dpnum", str(profile.get_int("double_plays")))
        pcdata.set_attribute("sach", str(profile.get_int("single_dj_points")))
        pcdata.set_attribute("dach", str(profile.get_int("double_dj_points")))
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
            )
        )
        grade.set_attribute(
            "dgid",
            str(
                self.db_to_game_rank(
                    profile.get_int(self.DAN_RANKING_DOUBLE, -1),
                    self.GAME_CLTYPE_DOUBLE,
                )
            )
        )
        rankings = self.data.local.user.get_achievements(
            self.game, self.version, userid
        )
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
                        ]
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
                        ]
                    )
                )

        ex = Node.void("ex")
        root.add_child(ex)
        for rank in rankings:
            if rank.type == self.COURSE_TYPE_EXPERT:
                ex.add_child(
                    Node.u32_array(
                        "e",
                        [
                            int(rank.id / 6),  # course ID
                            rank.id % 6,  # course chart
                            self.db_to_game_status(
                                rank.data.get_int("clear_status")
                            ),  # course clear status
                            rank.data.get_int("pgnum"),  # flashing great count
                            rank.data.get_int("gnum"),  # great count
                        ]
                    )
                )

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
            ]
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
        links = self.data.local.user.get_links(self.game, self.version, userid)
        for link in links:
            rival_type = None
            if link.type == "sp_rival":
                rival_type = "1"
            elif link.type == "dp_rival":
                rival_type = "2"
            else:
                # No business with this link type
                continue

            other_profile = self.get_profile(link.other_userid)
            if other_profile is None:
                continue
            other_play_stats = self.get_play_statistics(link.other_userid)

            rival = Node.void("rival")
            rlist.add_child(rival)
            rival.set_attribute("spdp", rival_type)
            rival.set_attribute("id", str(other_profile.extid))
            rival.set_attribute("id_str", ID.format_extid(other_profile.extid))
            rival.set_attribute("djname", other_profile.get_str("name"))
            rival.set_attribute("pid", other_profile.get_int("pid"))
            rival.set_attribute(
                "sg",
                str(
                    self.db_to_game_rank(
                        other_profile.get_int(self.DAN_RANKING_SINGLE, -1),
                        self.GAME_CLTYPE_SINGLE,
                    )
                ),
            )
            rival.set_attribute(
                "dg",
                str(
                    self.db_to_game_rank(
                        other_profile.get_int(self.DAN_RANKING_DOUBLE, -1),
                        self.GAME_CLTYPE_DOUBLE,
                    )
                ),
            )
            rival.set_attribute("sa", str(other_play_stats.get_int("single_dj_points")))
            rival.set_attribute("da", str(other_play_stats.get_int("double_dj_points")))

            qprodata = Node.void("qprodata")
            rival.add_child(qprodata)
            qpro = other_profile.get_dict("qpro")
            qprodata.set_attribute("head", str(qpro.get_int("head")))
            qprodata.set_attribute("hair", str(qpro.get_int("hair")))
            qprodata.set_attribute("face", str(qpro.get_int("face")))
            qprodata.set_attribute("hand", str(qpro.get_int("hand")))
            qprodata.set_attribute("body", str(qpro.get_int("body")))

        # ocrs = Node.void("ocrs")

        # flist = Node.void("flist")

        travel = Node.void("travel")
        root.add_child(travel)

        return root

    def unformat_profile(
        self, userid: UserID, request: Node, oldprofile: Profile
    ) -> Profile:
        newprofile = oldprofile.clone()
        play_stats = self.get_play_statistics(userid)

        # Track play counts, DJ points and options
        cltype = int(request.attribute("cltype"))
        if cltype == self.GAME_CLTYPE_SINGLE:
            play_stats.increment_int("single_plays")
            play_stats.replace_int("single_dj_points", int(request.attribute("achi")))
            play_stats.replace_int("sp_opt", int(request.attribute("opt")))
        if cltype == self.GAME_CLTYPE_DOUBLE:
            play_stats.increment_int("double_plays")
            play_stats.replace_int("double_dj_points", int(request.attribute("achi")))
            play_stats.replace_int("dp_opt", int(request.attribute("opt")))
            play_stats.replace_int("dp_opt2", int(request.attribute("opt2")))

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
        newprofile.replace_int("lift", int(request.attribute("lift")))

        jpoint = request.child("jpoint")
        if jpoint is not None:
            newprofile.replace_int("jpoint", int(jpoint.attribute("point")))

        history = request.child("history")
        if history is not None:
            history_dict = newprofile.get_dict("history")
            history_dict.replace_int_array("type", 30, history.child_value("type"))
            history_dict.replace_int_array("time", 30, history.child_value("time"))
            history_dict.replace_int_array("param0", 30, history.child_value("p0"))
            history_dict.replace_int_array("param1", 30, history.child_value("p1"))
            history_dict.replace_int_array("param2", 30, history.child_value("p2"))
            history_dict.replace_int_array("param3", 30, history.child_value("p3"))
            history_dict.replace_int_array("param4", 30, history.child_value("p4"))

        return newprofile
