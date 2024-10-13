# vim: set fileencoding=utf-8
from typing import Final

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.course import IIDXCourse

from bemani.common import (
    VersionConstants,
    Time,
    ID,
    intish,
)
from bemani.common.validateddict import Profile
from bemani.data.types import UserID
from bemani.protocol.node import Node


class IIDXResident(IIDXCourse, IIDXBase):
    name: str = "Beatmania IIDX RESIDENT"
    version: int = VersionConstants.IIDX_RESIDENT

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
    GAME_SP_DAN_RANK_CHUDEN: Final[int] = 17
    GAME_SP_DAN_RANK_KAIDEN: Final[int] = 18

    GAME_DP_DAN_RANK_7_KYU: Final[int] = 0
    GAME_DP_DAN_RANK_6_KYU: Final[int] = 1
    GAME_DP_DAN_RANK_5_KYU: Final[int] = 2
    GAME_DP_DAN_RANK_4_KYU: Final[int] = 3
    GAME_DP_DAN_RANK_3_KYU: Final[int] = 4
    GAME_DP_DAN_RANK_2_KYU: Final[int] = 5
    GAME_DP_DAN_RANK_1_KYU: Final[int] = 6
    GAME_DP_DAN_RANK_1_DAN: Final[int] = 7
    GAME_DP_DAN_RANK_2_DAN: Final[int] = 8
    GAME_DP_DAN_RANK_3_DAN: Final[int] = 9
    GAME_DP_DAN_RANK_4_DAN: Final[int] = 10
    GAME_DP_DAN_RANK_5_DAN: Final[int] = 11
    GAME_DP_DAN_RANK_6_DAN: Final[int] = 12
    GAME_DP_DAN_RANK_7_DAN: Final[int] = 13
    GAME_DP_DAN_RANK_8_DAN: Final[int] = 14
    GAME_DP_DAN_RANK_9_DAN: Final[int] = 15
    GAME_DP_DAN_RANK_10_DAN: Final[int] = 16
    GAME_DP_DAN_RANK_CHUDEN: Final[int] = 17
    GAME_DP_DAN_RANK_KAIDEN: Final[int] = 18

    GAME_CHART_TYPE_N7: Final[int] = 0
    GAME_CHART_TYPE_H7: Final[int] = 1
    GAME_CHART_TYPE_A7: Final[int] = 2
    GAME_CHART_TYPE_N14: Final[int] = 3
    GAME_CHART_TYPE_H14: Final[int] = 4
    GAME_CHART_TYPE_A14: Final[int] = 5
    GAME_CHART_TYPE_B7: Final[int] = 6

    @property
    def requires_extended_regions(self) -> bool:
        return True

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
                self.DAN_RANK_CHUDEN: self.GAME_SP_DAN_RANK_CHUDEN,
                self.DAN_RANK_KAIDEN: self.GAME_SP_DAN_RANK_KAIDEN,
            }[db_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {
                self.DAN_RANK_7_KYU: self.GAME_DP_DAN_RANK_7_KYU,
                self.DAN_RANK_6_KYU: self.GAME_DP_DAN_RANK_6_KYU,
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
                self.DAN_RANK_CHUDEN: self.GAME_DP_DAN_RANK_CHUDEN,
                self.DAN_RANK_KAIDEN: self.GAME_DP_DAN_RANK_KAIDEN,
            }[db_dan]
        else:
            raise Exception("Invalid cltype!")

    def game_to_db_chart(self, db_chart: int) -> int:
        # No chart id
        if db_chart == -1:
            return -1

        return {
            self.GAME_CHART_TYPE_B7: self.CHART_TYPE_B7,
            self.GAME_CHART_TYPE_N7: self.CHART_TYPE_N7,
            self.GAME_CHART_TYPE_H7: self.CHART_TYPE_H7,
            self.GAME_CHART_TYPE_A7: self.CHART_TYPE_A7,
            self.GAME_CHART_TYPE_N14: self.CHART_TYPE_N14,
            self.GAME_CHART_TYPE_H14: self.CHART_TYPE_H14,
            self.GAME_CHART_TYPE_A14: self.CHART_TYPE_A14,
        }[db_chart]

    def handle_IIDX30shop_getname_request(self, request: Node) -> Node:
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

        root = Node.void("IIDX30shop")
        root.set_attribute("opname", machine_name)
        root.set_attribute("pid", str(self.get_machine_region()))
        root.set_attribute("cls_opt", "1" if close else "0")
        root.set_attribute("hr", str(hour))
        root.set_attribute("mi", str(minute))
        return root
    
    def handle_IIDX30shop_savename_request(self, request: Node) -> Node:
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

        return Node.void("IIDX30shop")

    def handle_IIDX30shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("IIDX30shop")

    def handle_IIDX30gameSystem_systemInfo_request(self, request: Node) -> Node:
        root = Node.void("IIDX30gameSystem")

        arena_schedule = Node.void("arena_schedule")
        root.add_child(arena_schedule)
        arena_schedule.add_child(Node.u8("phase", 3))  # 1 - Not held, 2 - Scheduled to be held, 3 - Currently being held
        arena_schedule.add_child(Node.u32("start", Time.timestamp_from_date(2024, 10, 1)))
        arena_schedule.add_child(Node.u32("end", Time.timestamp_from_date(2024, 10, 31)))

        return root

    def handle_IIDX30music_getrank_request(self, request: Node) -> Node:
        cltype = int(request.attribute("cltype"))

        root = Node.void("IIDX30music")
        style = Node.void("style")
        root.add_child(style)
        style.set_attribute("type", str(cltype))

        return root

    def handle_IIDX30music_reg_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid") or 0)
        musicid = int(request.attribute("mid") or 0)
        chart = int(request.attribute("clid") or -1)
        if extid == 0 or musicid == 0 or chart == -1:
            raise Exception("iidxid or music id or chart is empty")

        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        root = Node.void("IIDX26music")

        if userid is not None:
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
            all_players = {uid: prof for (uid, prof) in self.get_any_profiles([s[0] for s in all_scores])}

            shop_id = ID.parse_machine_id(request.attribute("location_id"))
            if not global_scores:
                all_scores = [score for score in all_scores if (score[0] == userid or score[1].location == shop_id)]

            # Find our actual index
            oldindex = None
            for i in range(len(all_scores)):
                if all_scores[i][0] == userid:
                    oldindex = i
                    break

            clear_status = self.game_to_db_status(int(request.attribute("cflg")))
            pgreats = int(request.attribute("pgnum"))
            greats = int(request.attribute("gnum"))
            miss_count = int(request.attribute("mnum"))
            ghost = request.child_value("ghost")
            shopid = ID.parse_machine_id(request.attribute("location_id"))

            self.update_score(
                userid,
                musicid,
                chart,
                clear_status,
                pgreats,
                greats,
                miss_count,
                ghost,
                shopid,
            )

            # Calculate and return statistics about this song
            root.set_attribute("mid", request.attribute("mid"))
            root.set_attribute("clid", request.attribute("clid"))

            attempts = self.get_clear_rates(musicid, chart)
            count = attempts[musicid][chart]["total"]
            clear = attempts[musicid][chart]["clears"]
            full_combo = attempts[musicid][chart]["fcs"]

            if count > 0:
                root.set_attribute("crate", str(int((1000 * clear) / count)))
                root.set_attribute("frate", str(int((1000 * full_combo) / count)))
            else:
                root.set_attribute("crate", "0")
                root.set_attribute("frate", "0")
            root.set_attribute("rankside", "0")  # only single play ranking

            if userid is not None:
                # Shop ranking
                shopdata = Node.void("shopdata")
                root.add_child(shopdata)
                shopdata.set_attribute("rank", "-1" if oldindex is None else str(oldindex + 1))

                # Grab the rank of some other players on this song
                ranklist = Node.void("ranklist")
                root.add_child(ranklist)

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
                missing_players = [uid for (uid, _) in all_scores if uid not in all_players]
                for uid, prof in self.get_any_profiles(missing_players):
                    all_players[uid] = prof

                if not global_scores:
                    all_scores = [score for score in all_scores if (score[0] == userid or score[1].location == shop_id)]

                # Find our actual index
                ourindex = None
                for i in range(len(all_scores)):
                    if all_scores[i][0] == userid:
                        ourindex = i
                        break
                if ourindex is None:
                    raise Exception("Cannot find our own score after saving to DB!")
                start = ourindex - 4
                end = ourindex + 4
                if start < 0:
                    start = 0
                if end >= len(all_scores):
                    end = len(all_scores) - 1
                relevant_scores = all_scores[start : (end + 1)]

                record_num = start + 1
                for score in relevant_scores:
                    profile = all_players[score[0]]

                    data = Node.void("data")
                    ranklist.add_child(data)
                    data.set_attribute("iidx_id", str(profile.extid))
                    data.set_attribute("name", profile.get_str("name"))

                    machine_name = ""
                    machine = self.get_machine_by_id(shop_id)
                    if machine is not None:
                        machine_name = machine.name
                    data.set_attribute("opname", machine_name)
                    data.set_attribute("rnum", str(record_num))
                    data.set_attribute("score", str(score[1].points))
                    data.set_attribute(
                        "clflg",
                        str(self.db_to_game_status(score[1].data.get_int("clear_status"))),
                    )
                    data.set_attribute("pid", str(profile.get_int("pid")))
                    data.set_attribute("myFlg", "1" if score[0] == userid else "0")
                    data.set_attribute("update", "0")

                    data.set_attribute(
                        "sgrade",
                        str(
                            self.db_to_game_rank(
                                profile.get_int(self.DAN_RANKING_SINGLE, -1),
                                self.GAME_CLTYPE_SINGLE,
                            ),
                        ),
                    )
                    data.set_attribute(
                        "dgrade",
                        str(
                            self.db_to_game_rank(
                                profile.get_int(self.DAN_RANKING_DOUBLE, -1),
                                self.GAME_CLTYPE_DOUBLE,
                            ),
                        ),
                    )

                    qpro = profile.get_dict("qpro")
                    data.set_attribute("head", str(qpro.get_int("head")))
                    data.set_attribute("hair", str(qpro.get_int("hair")))
                    data.set_attribute("face", str(qpro.get_int("face")))
                    data.set_attribute("body", str(qpro.get_int("body")))
                    data.set_attribute("hand", str(qpro.get_int("hand")))

                    record_num = record_num + 1
        else:
            root = Node.void("IIDX30music")
            root.set_attribute("status", "1")

        return root

    def handle_IIDX30pc_common_request(self, request: Node) -> Node:
        root = Node.void("IIDX30pc")
        root.set_attribute("expire", "1")

        root.add_child(
            Node.s32_array("kac_mid", [0] * 30)
        )
        root.add_child(
            Node.s32_array("kac_clid", [0] * 30)
        )

        # ir = Node.void("ir")
        # root.add_child(ir)
        # ir.set_attribute("beat", "0")

        # Missing cm

        # Missing tdj_cm

        playvideo_disable_music = Node.void("playvideo_disable_music")
        root.add_child(playvideo_disable_music)
        playvideo_disable_musics = []
        for music_id in playvideo_disable_musics:
            music = Node.void("music")
            playvideo_disable_music.add_child(music)
            music.set_attribute("music_id", str(music_id))

        music_movie_suspend = Node.void("music_movie_suspend")
        root.add_child(music_movie_suspend)
        music_movie_suspend_ids = []
        for music_id in music_movie_suspend_ids:
            music = Node.void("music")
            music_movie_suspend.add_child(music)
            music.set_attribute("music_id", str(music_id))
            music.set_attribute("kind", str(music_id))
            music.set_attribute("name", str(music_id))

        movie_agreement = Node.void("movie_agreement")
        root.add_child(movie_agreement)
        movie_agreement.set_attribute("version", "1")

        root.add_child(Node.void("play_video"))

        root.add_child(Node.void("display_asio_logo"))

        # Missing hitchart

        root.add_child(Node.void("lane_gacha"))
        root.add_child(Node.void("fps_fix"))
        root.add_child(Node.void("save_unsync_log"))
        root.add_child(Node.void("tourism_booster"))
        root.add_child(Node.void("ameto_event"))

        questionnaire_list = Node.void("questionnaire_list")
        root.add_child(questionnaire_list)

        return root

    def handle_IIDX30pc_delete_request(self, request: Node) -> Node:
        # I'm not sure what to do here, so I'll send an empty response.
        return Node.void("IIDX30pc")

    def handle_IIDX30pc_oldget_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        root = Node.void("IIDX30pc")
        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
            if userid is not None:
                oldversion = self.previous_version()
                if oldversion is not None:
                    profile = oldversion.get_profile(userid)
                else:
                    profile = None
            else:
                profile = None

            root.set_attribute("status", "1" if profile is None else "0")
        else:
            root.set_attribute("status", "2")
        return root

    def handle_IIDX30pc_reg_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        name = request.attribute("name")
        prefecture_id = int(request.attribute("pid") or 0)
        profile = self.new_profile_by_refid(refid, name, prefecture_id)

        root = Node.void("IIDX30pc")
        if profile is not None:
            root.set_attribute("id", str(profile.extid))
            root.set_attribute("id_str", ID.format_extid(profile.extid))
        return root

    def handle_IIDX30pc_get_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("IIDX30pc")
        return root

    def handle_IIDX30pc_visit_request(self, request: Node) -> Node:
        # <call model="LDJ:J:D:A:2023090500" srcid="00010203040506070809" tag="jP00APp2">
        #     <IIDX30pc iidxid="54577776" lid="US-3" method="visit" pid="56" />
        # </call>
        extid = int(request.attribute("iidxid"))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)
        anum, snum, pnum = 0, 0, 0

        if userid is not None:
            play_stats = self.get_play_statistics(userid)
            region = self.get_machine_region()

            visitor_dict = play_stats.get_dict("visitor")

            regions_dict = visitor_dict.get_dict("regions")
            regions_dict.increment_int(str(region))
            visitor_dict.replace_dict("regions", regions_dict)

            arcades_dict = visitor_dict.get_dict("arcades")
            if self.machine_joined_arcade():
                joined_arcade = self.get_arcade()
                if joined_arcade:
                    arcades_dict.increment_int(str(joined_arcade.id))
                    visitor_dict.replace_dict("arcades", arcades_dict)

            machines_dict = visitor_dict.get_dict("machines")
            machines_dict.increment_int(str(self.get_machine_id()))
            visitor_dict.replace_dict("machines", machines_dict)

            play_stats.replace_dict("visitor", visitor_dict)
            self.update_play_statistics(userid, play_stats)

            anum = len(play_stats.get_dict("visitor").get_dict("regions"))
            snum = len(play_stats.get_dict("visitor").get_dict("arcades"))
            pnum = len(play_stats.get_dict("visitor").get_dict("machines"))

        root = Node.void("IIDX30pc")
        root.set_attribute("anum", str(anum))
        root.set_attribute("snum", str(snum))
        root.set_attribute("pnum", str(pnum))
        root.set_attribute("aflg", "0")
        root.set_attribute("sflg", "0")
        root.set_attribute("pflg", "0")
        return root

    def handle_IIDX30pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        self.put_profile_by_extid(extid, request)

        return Node.void("IIDX30pc")

    def handle_IIDX30pc_getLaneGachaTicket_request(self, request: Node) -> Node:
        return Node.void("IIDX30pc")

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("IIDX30pc")

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
        pcdata.set_attribute("mode", str(profile.get_int("mode")))
        pcdata.set_attribute("pmode", str(profile.get_int("pmode")))
        pcdata.set_attribute("ngrade", str(profile.get_int("ngrade")))
        pcdata.set_attribute("rtype", str(profile.get_int("rtype")))
        pcdata.set_attribute("sp_opt", str(profile.get_int("sp_opt")))
        pcdata.set_attribute("dp_opt", str(profile.get_int("dp_opt")))
        pcdata.set_attribute("dp_opt2", str(profile.get_int("dp_opt2")))
        pcdata.set_attribute("gpos", str(profile.get_int("gpos")))
        pcdata.set_attribute("s_sorttype", str(profile.get_int("s_sorttype")))
        pcdata.set_attribute("d_sorttype", str(profile.get_int("d_sorttype")))
        pcdata.set_attribute("s_pace", str(profile.get_int("s_pace")))
        pcdata.set_attribute("d_pace", str(profile.get_int("d_pace")))
        pcdata.set_attribute("s_gno", str(profile.get_int("s_gno")))
        pcdata.set_attribute("d_gno", str(profile.get_int("d_gno")))
        pcdata.set_attribute("s_sub_gno", str(profile.get_int("s_sub_gno")))
        pcdata.set_attribute("d_sub_gno", str(profile.get_int("d_sub_gno")))
        pcdata.set_attribute("s_gtype", str(profile.get_int("s_gtype")))
        pcdata.set_attribute("d_gtype", str(profile.get_int("d_gtype")))
        pcdata.set_attribute("s_sdlen", str(profile.get_int("s_sdlen")))
        pcdata.set_attribute("d_sdlen", str(profile.get_int("d_sdlen")))
        pcdata.set_attribute("s_sdtype", str(profile.get_int("s_sdtype")))
        pcdata.set_attribute("d_sdtype", str(profile.get_int("d_sdtype")))
        pcdata.set_attribute("s_timing", str(profile.get_int("s_timing")))
        pcdata.set_attribute("d_timing", str(profile.get_int("d_timing")))
        pcdata.set_attribute("s_notes", str(profile.get_int("s_notes")))
        pcdata.set_attribute("d_notes", str(profile.get_int("d_notes")))
        pcdata.set_attribute("s_judge", str(profile.get_int("s_judge")))
        pcdata.set_attribute("d_judge", str(profile.get_int("d_judge")))
        pcdata.set_attribute("s_judgeAdj", str(profile.get_int("s_judgeAdj")))
        pcdata.set_attribute("d_judgeAdj", str(profile.get_int("d_judgeAdj")))
        pcdata.set_attribute("s_hispeed", str(profile.get_int("s_hispeed")))
        pcdata.set_attribute("d_hispeed", str(profile.get_int("d_hispeed")))
        pcdata.set_attribute("s_liflen", str(profile.get_int("s_liflen")))
        pcdata.set_attribute("d_liflen", str(profile.get_int("d_liflen")))
        pcdata.set_attribute("s_disp_judge", str(profile.get_int("s_disp_judge")))
        pcdata.set_attribute("d_disp_judge", str(profile.get_int("d_disp_judge")))
        pcdata.set_attribute("s_opstyle", str(profile.get_int("s_opstyle")))
        pcdata.set_attribute("d_opstyle", str(profile.get_int("d_opstyle")))
        pcdata.set_attribute("s_graph_score", str(profile.get_int("s_graph_score")))
        pcdata.set_attribute("d_graph_score", str(profile.get_int("d_graph_score")))
        pcdata.set_attribute("s_auto_scrach", str(profile.get_int("s_auto_scrach")))
        pcdata.set_attribute("d_auto_scrach", str(profile.get_int("d_auto_scrach")))
        pcdata.set_attribute("s_gauge_disp", str(profile.get_int("s_gauge_disp")))
        pcdata.set_attribute("d_gauge_disp", str(profile.get_int("d_gauge_disp")))
        pcdata.set_attribute("s_lane_brignt", str(profile.get_int("s_lane_brignt")))
        pcdata.set_attribute("d_lane_brignt", str(profile.get_int("d_lane_brignt")))
        pcdata.set_attribute("s_camera_layout", str(profile.get_int("s_camera_layout")))
        pcdata.set_attribute("d_camera_layout", str(profile.get_int("d_camera_layout")))
        pcdata.set_attribute("s_ghost_score", str(profile.get_int("s_ghost_score")))
        pcdata.set_attribute("d_ghost_score", str(profile.get_int("d_ghost_score")))
        pcdata.set_attribute("s_tsujigiri_disp", str(profile.get_int("s_tsujigiri_disp")))
        pcdata.set_attribute("d_tsujigiri_disp", str(profile.get_int("d_tsujigiri_disp")))
        pcdata.set_attribute("s_auto_adjust", str(profile.get_int("s_auto_adjust")))
        pcdata.set_attribute("d_auto_adjust", str(profile.get_int("d_auto_adjust")))
        pcdata.set_attribute("s_timing_split", str(profile.get_int("s_timing_split")))
        pcdata.set_attribute("d_timing_split", str(profile.get_int("d_timing_split")))
        pcdata.set_attribute("s_visualization", str(profile.get_int("s_visualization")))
        pcdata.set_attribute("d_visualization", str(profile.get_int("d_visualization")))

        lightning_play_data = Node.void("lightning_play_data")
        root.add_child(lightning_play_data)
        lightning_play_data.set_attribute("spnum", str(play_stats.get_int("lightning_single_plays")))
        lightning_play_data.set_attribute("dpnum", str(play_stats.get_int("lightning_double_plays")))

        lightning_setting_dict = profile.get_dict("lightning_setting")
        lightning_setting = Node.void("lightning_setting")
        root.add_child(lightning_setting)
        lightning_setting.set_attribute("headphone_vol", str(lightning_setting_dict.get_int("headphone_vol", 10)))
        lightning_setting.set_attribute("resistance_sp_left", str(lightning_setting_dict.get_int("resistance_sp_left", 4)))
        lightning_setting.set_attribute("resistance_sp_right", str(lightning_setting_dict.get_int("resistance_sp_right", 4)))
        lightning_setting.set_attribute("resistance_dp_left", str(lightning_setting_dict.get_int("resistance_dp_left", 4)))
        lightning_setting.set_attribute("resistance_dp_right", str(lightning_setting_dict.get_int("resistance_dp_right", 4)))
        lightning_setting.set_attribute("skin_0", str(lightning_setting_dict.get_int("skin_0", 0)))
        lightning_setting.set_attribute("flg_skin_0", str(lightning_setting_dict.get_int("flg_skin_0", 0)))
        lightning_setting.add_child(Node.s32_array("slider", lightning_setting_dict.get_int_array("slider", 7, [7, 7, 7, 7, 7, 15, 15])))
        lightning_setting.add_child(Node.bool_array("light", lightning_setting_dict.get_bool_array("light", 10, [True] * 10)))
        lightning_setting.add_child(Node.bool("concentration", lightning_setting_dict.get_bool("concentration")))

        # Missing weekly_achieve_sp, I don't know what this is supposed to do.

        # Missing weekly_achieve_dp, I don't know what this is supposed to do.

        spdp_rival = Node.void("spdp_rival")
        root.add_child(spdp_rival)
        spdp_rival.set_attribute("flg", "-1")

        # Enable the function to send images to the e-amusement app
        bind_eaappli = Node.void("bind_eaappli")
        root.add_child(bind_eaappli)

        # Set this profile as a profile subscribed to the premium course.
        ea_premium_course = Node.void("ea_premium_course")
        root.add_child(ea_premium_course)

        kac_entry_info = Node.void("kac_entry_info")
        root.add_child(kac_entry_info)
        kac_entry_info.add_child(Node.void("enable_kac_deller"))
        kac_entry_info.add_child(Node.void("disp_kac_mark"))
        kac_entry_info.add_child(Node.void("is_kac_entry"))
        kac_entry_info.add_child(Node.void("is_kac_evnet_entry"))
        kac_secret_music = Node.void("kac_secret_music")
        root.add_child(kac_secret_music)
        kac_secret_musics = [
            30097,  # パーフェクトイーター / BEMANI Sound Team "PON" feat.かなたん
            30030,  # KAC TOURISM 1 - Caldwell 99 / BlackY
            30031,  # KAC TOURISM 2 - mathematical good-bye / 三代目 ADULTIC TEACHERS feat. BEMANI Sound Team "スコーピオン志村"
            30114,  # KAC TOURISM 3 - Stylus / BEMANI Sound Team "HuΣeR"
        ]
        for index, music in enumerate(kac_secret_musics):
            music_info = Node.void("music_info")
            kac_secret_music.add_child(music_info)
            music_info.set_attribute("index", str(index))
            music_info.set_attribute("music_id", str(music))

        # secret = Node.void("secret")
        # root.add_child(secret)
        # secret.add_child(Node.s64_array("flg1", [0] * 4))
        # secret.add_child(Node.s64_array("flg2", [0] * 4))
        # secret.add_child(Node.s64_array("flg3", [0] * 4))
        # secret.add_child(Node.s64_array("flg4", [0] * 4))

        # leggendaria = Node.void("leggendaria")
        # root.add_child(leggendaria)
        # leggendaria.add_child(Node.s64_array("flg1", [0] * 4))

        music_memo_dict = profile.get_dict("music_memo")
        if music_memo_dict is not None:
            music_memo = Node.void("music_memo")
            root.add_child(music_memo)

            for (play_style, folder) in music_memo_dict.items():
                for (folder_id, folder_dict) in folder.items():
                    folder_node = Node.void("folder")
                    music_memo.add_child(folder_node)
                    folder_node.set_attribute("play_style", str(play_style))
                    folder_node.set_attribute("folder_id", str(folder_id))
                    folder_node.set_attribute("name", folder_dict["name"])
                    folder_node.add_child(Node.s32_array("music_id", folder_dict["music_id"]))

        # qpro_secret = Node.void("qpro_secret")
        # root.add_child(qpro_secret)
        # qpro_secret.add_child(Node.s64_array("head", [0] * 16))
        # qpro_secret.add_child(Node.s64_array("hair", [0] * 16))
        # qpro_secret.add_child(Node.s64_array("face", [0] * 16))
        # qpro_secret.add_child(Node.s64_array("body", [0] * 16))
        # qpro_secret.add_child(Node.s64_array("hand", [0] * 16))

        grade = Node.void("grade")
        root.add_child(grade)
        grade.set_attribute("sgid", "-1")
        grade.set_attribute("dgid", "-1")

        # eisei_data = Node.void("eisei_data")
        # root.add_child(eisei_data)

        # root.add_child(Node.s16_array("skin", [0] * 20))

        qpro = profile.get_dict("qpro")
        if qpro is not None:
            root.add_child(Node.u32_array("qprodata", [
                qpro.get_int("head"),
                qpro.get_int("hair"),
                qpro.get_int("face"),
                qpro.get_int("hand"),
                qpro.get_int("body"),
            ]))

        rlist = Node.void("rlist")
        root.add_child(rlist)

        notes_radar_dict = profile.get_dict("notes_radar")
        if notes_radar_dict is not None:
            for (style, radar) in notes_radar_dict.items():
                notes_radar = Node.void("notes_radar")
                root.add_child(notes_radar)
                notes_radar.set_attribute("style", str(style))
                notes_radar.add_child(Node.s32_array("radar_score", radar))

        # notes_radar_old = Node.void("notes_radar_old")
        # root.add_child(notes_radar_old)
        # notes_radar_old.set_attribute("style", str(self.GAME_CLTYPE_SINGLE))
        # notes_radar_old.add_child(Node.s32_array("radar_score", [0] * 6))

        # Missing shitei node, I don't know what this is supposed to do.

        # weekly = Node.void("weekly")
        # root.add_child(weekly)
        # weekly.set_attribute("wid", "0")
        # weekly.set_attribute("mid", "0")

        # weekly_score = Node.void("weekly_score")
        # root.add_child(weekly_score)
        # weekly_score.set_attribute("class_id", "-1")
        # weekly_score.set_attribute("border_score_0", "0")
        # weekly_score.set_attribute("border_score_1", "0")
        # weekly_score.set_attribute("border_score_2", "0")
        # weekly_score.set_attribute("border_score_3", "0")
        # weekly_score.set_attribute("border_score_4", "0")
        # weekly_score.set_attribute("border_rank_0", "0")
        # weekly_score.set_attribute("border_rank_1", "0")
        # weekly_score.set_attribute("border_rank_2", "0")
        # weekly_score.set_attribute("border_rank_3", "0")
        # weekly_score.set_attribute("border_rank_4", "0")
        # weekly_score.set_attribute("rank", "0")
        # weekly_score.set_attribute("score", "0")
        # weekly_score.set_attribute("total_user", "0")

        visitor_dict = play_stats.get_dict("visitor")
        if visitor_dict is not None:
            anum = len(visitor_dict.get_dict("regions"))
            snum = len(visitor_dict.get_dict("arcades"))
            pnum = len(visitor_dict.get_dict("machines"))

            visitor = Node.void("visitor")
            root.add_child(visitor)
            visitor.set_attribute("anum", str(anum))  # 원정 에리어 수
            visitor.set_attribute("snum", str(snum))  # 원정 매장 수
            visitor.set_attribute("pnum", str(pnum))  # 원정 게임기 수
            visitor.set_attribute("vs_flg", "1")

        step_dict = profile.get_dict("step")
        if step_dict is not None:
            step = Node.void("step")
            root.add_child(step)
            step.set_attribute("enemy_damage", str(step_dict.get_int("enemy_damage")))
            step.set_attribute("progress", str(step_dict.get_int("progress")))
            step.set_attribute("total_point", str(step_dict.get_int("total_point")))
            step.set_attribute("enemy_defeat_flg", str(step_dict.get_int("enemy_defeat_flg")))
            step.set_attribute("sp_level", str(step_dict.get_int("sp_level")))
            step.set_attribute("dp_level", str(step_dict.get_int("dp_level")))
            step.set_attribute("sp_fluctuation", str(step_dict.get_int("sp_fluctuation")))
            step.set_attribute("dp_fluctuation", str(step_dict.get_int("dp_fluctuation")))
            step.set_attribute("mission_clear_num", str(step_dict.get_int("mission_clear_num")))
            step.set_attribute("sp_mplay", str(step_dict.get_int("sp_mplay")))
            step.set_attribute("dp_mplay", str(step_dict.get_int("dp_mplay")))
            step.set_attribute("tips_read_list", str(step_dict.get_int("tips_read_list")))
            step.add_child(Node.bool("is_track_ticket", step_dict.get_bool("is_track_ticket")))

        # Missing packinfo node
        pack_id = None

        achievements_dict = profile.get_dict("achievements")
        achievements_node = Node.void("achievements")
        # root.add_child(achievements_node)

        # Dailies
        if pack_id is None:
            achievements_node.set_attribute("pack_comp", "0")
            achievements_node.set_attribute("pack", "0")
        # else:

        achievements_node.set_attribute("last_weekly", str(achievements_dict.get_int("last_weekly")))
        achievements_node.set_attribute("weekly_num", str(achievements_dict.get_int("weekly_num")))
        achievements_node.set_attribute("visit_flg", str(achievements_dict.get_int("visit_flg")))
        achievements_node.set_attribute("rival_crush", str(achievements_dict.get_int("rival_crush")))
        achievements_node.add_child(Node.s64_array("trophy", achievements_dict.get_int_array("trophy", 20)))

        # Missing deller node

        # Missing orb_data node

        # Missing qpro_ticket node

        # Missing old_linkage_secret_flg node

        # Missing arena_data node

        # Missing tsujigiri node

        # Missing tsujigiri_hidden_chara node

        # Missing weekly_result node

        # Missing skin_customize_flg node

        # Missing event_1 node

        # Missing event_1_rival_recommend node

        # Missing event1_rival_bonus node

        # Missing floor_infection4 node

        # Missing bemani_vote node

        # Missing bemani_janken_meeting node

        # Missing bemani_rush node

        # Missing ultimate_mobile_link node

        # Missing bemani_musiq_fes node

        # Missing busou_linkage node

        # Missing busou_linkage_2 node

        # Missing valkyrie_linkage node

        # Missing bemani_song_battle node

        # Missing bemani_mixup node

        # Missing ccj_linkage node

        # Missing triple_tribe node

        # Missing player_compe node

        # Missing news node

        language = profile.get_int("language_setting", -1)
        # If the language is not set, find profile's region and set the language accordingly.
        if language == -1:
            prefecture_id = profile.get_int("pid")
            if prefecture_id == 49:
                # Region code 49 is Korea in the game, so set the language to Korean.
                language = 1
            else:
                # Otherwise, default to Japanese.
                language = 0

        language_setting = Node.void("language_setting")
        root.add_child(language_setting)
        language_setting.set_attribute("language", str(language))

        # Missing movie_agreement node

        # Missing movie_setting node

        # Missing exam_data node

        # Missing world_tourism node

        # Missing world_tourism_secret_flg node

        # Missing bpl_s3_supporter node

        # Missing bpls3_packinfo node

        # Missing bpl_s3_supporter_ticket node

        # Missing questionnaire node

        # Missing badge node

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        play_stats = self.get_play_statistics(userid)

        # Track play counts
        cltype = int(request.attribute("cltype"))
        if cltype == self.GAME_CLTYPE_SINGLE:
            play_stats.increment_int("single_plays")
        if cltype == self.GAME_CLTYPE_DOUBLE:
            play_stats.increment_int("double_plays")

        # Track DJ points
        play_stats.replace_int("single_dj_points", int(request.attribute("s_achi")))
        play_stats.replace_int("double_dj_points", int(request.attribute("d_achi")))

        # Profile settings
        newprofile.replace_int("mode", int(request.attribute("mode")))
        newprofile.replace_int("pmode", int(request.attribute("pmode")))
        newprofile.replace_int("ngrade", int(request.attribute("ngrade")))
        newprofile.replace_int("rtype", int(request.attribute("rtype")))
        newprofile.replace_int("sp_opt", int(request.attribute("sp_opt")))
        newprofile.replace_int("dp_opt", int(request.attribute("dp_opt")))
        newprofile.replace_int("dp_opt2", int(request.attribute("dp_opt2")))
        newprofile.replace_int("gpos", int(request.attribute("gpos")))
        newprofile.replace_int("s_sorttype", int(request.attribute("s_sorttype")))
        newprofile.replace_int("d_sorttype", int(request.attribute("d_sorttype")))
        newprofile.replace_int("s_pace", int(request.attribute("s_pace")))
        newprofile.replace_int("d_pace", int(request.attribute("d_pace")))
        newprofile.replace_int("s_gno", int(request.attribute("s_gno")))
        newprofile.replace_int("d_gno", int(request.attribute("d_gno")))
        newprofile.replace_int("s_sub_gno", int(request.attribute("s_sub_gno")))
        newprofile.replace_int("d_sub_gno", int(request.attribute("d_sub_gno")))
        newprofile.replace_int("s_gtype", int(request.attribute("s_gtype")))
        newprofile.replace_int("d_gtype", int(request.attribute("d_gtype")))
        newprofile.replace_int("s_sdlen", int(request.attribute("s_sdlen")))
        newprofile.replace_int("d_sdlen", int(request.attribute("d_sdlen")))
        newprofile.replace_int("s_sdtype", int(request.attribute("s_sdtype")))
        newprofile.replace_int("d_sdtype", int(request.attribute("d_sdtype")))
        newprofile.replace_int("s_timing", int(request.attribute("s_timing")))
        newprofile.replace_int("d_timing", int(request.attribute("d_timing")))
        newprofile.replace_float("s_notes", float(request.attribute("s_notes")))
        newprofile.replace_float("d_notes", float(request.attribute("d_notes")))
        newprofile.replace_int("s_judge", int(request.attribute("s_judge")))
        newprofile.replace_int("d_judge", int(request.attribute("d_judge")))
        newprofile.replace_int("s_judgeAdj", int(request.attribute("s_judgeAdj")))
        newprofile.replace_int("d_judgeAdj", int(request.attribute("d_judgeAdj")))
        newprofile.replace_float("s_hispeed", float(request.attribute("s_hispeed")))
        newprofile.replace_float("d_hispeed", float(request.attribute("d_hispeed")))
        newprofile.replace_float("s_liflen", int(request.attribute("s_lift")))
        newprofile.replace_float("d_liflen", int(request.attribute("d_lift")))
        newprofile.replace_int("s_disp_judge", int(request.attribute("s_disp_judge")))
        newprofile.replace_int("d_disp_judge", int(request.attribute("d_disp_judge")))
        newprofile.replace_int("s_opstyle", int(request.attribute("s_opstyle")))
        newprofile.replace_int("d_opstyle", int(request.attribute("d_opstyle")))
        newprofile.replace_int("s_graph_score", int(request.attribute("s_graph_score")))
        newprofile.replace_int("d_graph_score", int(request.attribute("d_graph_score")))
        newprofile.replace_int("s_auto_scrach", int(request.attribute("s_auto_scrach")))
        newprofile.replace_int("d_auto_scrach", int(request.attribute("d_auto_scrach")))
        newprofile.replace_int("s_gauge_disp", int(request.attribute("s_gauge_disp")))
        newprofile.replace_int("d_gauge_disp", int(request.attribute("d_gauge_disp")))
        newprofile.replace_int("s_lane_brignt", int(request.attribute("s_lane_brignt")))
        newprofile.replace_int("d_lane_brignt", int(request.attribute("d_lane_brignt")))
        newprofile.replace_int("s_camera_layout", int(request.attribute("s_camera_layout")))
        newprofile.replace_int("d_camera_layout", int(request.attribute("d_camera_layout")))
        newprofile.replace_int("s_ghost_score", int(request.attribute("s_ghost_score")))
        newprofile.replace_int("d_ghost_score", int(request.attribute("d_ghost_score")))
        newprofile.replace_int("s_tsujigiri_disp", int(request.attribute("s_tsujigiri_disp")))
        newprofile.replace_int("d_tsujigiri_disp", int(request.attribute("d_tsujigiri_disp")))
        newprofile.replace_int("s_auto_adjust", int(request.attribute("s_auto_adjust")))
        newprofile.replace_int("d_auto_adjust", int(request.attribute("d_auto_adjust")))
        newprofile.replace_int("s_timing_split", int(request.attribute("s_timing_split")))
        newprofile.replace_int("d_timing_split", int(request.attribute("d_timing_split")))
        newprofile.replace_int("s_visualization", int(request.attribute("s_visualization")))
        newprofile.replace_int("d_visualization", int(request.attribute("d_visualization")))

        lightning_play_data = request.child("lightning_play_data")
        if lightning_play_data is not None:
            # Maybe track lightning play counts
            test = 0

        lightning_setting_dict = newprofile.get_dict("lightning_setting")
        lightning_setting = request.child("lightning_setting")
        if lightning_setting is not None:
            lightning_setting_dict.replace_int("headphone_vol", int(lightning_setting.attribute("headphone_vol")))
            lightning_setting_dict.replace_int("resistance_sp_left", int(lightning_setting.attribute("resistance_sp_left")))
            lightning_setting_dict.replace_int("resistance_sp_right", int(lightning_setting.attribute("resistance_sp_right")))
            lightning_setting_dict.replace_int("resistance_dp_left", int(lightning_setting.attribute("resistance_dp_left")))
            lightning_setting_dict.replace_int("resistance_dp_right", int(lightning_setting.attribute("resistance_dp_right")))
            lightning_setting_dict.replace_int_array("slider", 7, lightning_setting.child_value("slider"))
            lightning_setting_dict.replace_bool_array("light", 10, lightning_setting.child_value("light"))
            lightning_setting_dict.replace_bool("concentration", lightning_setting.child_value("concentration"))

        lightning_customize_flg = request.child_value("lightning_customize_flg")
        if lightning_customize_flg is not None:
            lightning_setting_dict.replace_int("flg_skin_0", lightning_customize_flg.child_value("flg_skin_0"))
        newprofile.replace_dict("lightning_setting", lightning_setting_dict)

        secret = request.child("secret")
        if secret is not None:
            secret_dict = newprofile.get_dict("secret")
            secret_dict.replace_int_array("flg1", 3, secret.child_value("flg1"))
            secret_dict.replace_int_array("flg2", 3, secret.child_value("flg2"))
            secret_dict.replace_int_array("flg3", 3, secret.child_value("flg3"))
            secret_dict.replace_int_array("flg4", 3, secret.child_value("flg4"))
            newprofile.replace_dict("secret", secret_dict)

        leggendaria = request.child("leggendaria")
        if leggendaria is not None:
            leggendaria_dict = newprofile.get_dict("leggendaria")
            leggendaria_dict.replace_int_array("flg1", 3, leggendaria.child_value("flg1"))
            newprofile.replace_dict("leggendaria", leggendaria_dict)

        music_memo = request.child("music_memo")
        if music_memo is not None:
            for child in music_memo.children:
                if child.name != "folder":
                    continue
                music_memo_dict = newprofile.get_dict("music_memo")
                play_style_dict = music_memo_dict.get_dict(str(child.attribute("play_style")))

                folder_dict = play_style_dict.get_dict(str(child.attribute("folder_id")))
                folder_dict.replace_str("name", child.attribute("name"))
                folder_dict.replace_int_array("music_id", 10, child.child_value("music_id"))

                play_style_dict.replace_dict(str(child.attribute("folder_id")), folder_dict)
                music_memo_dict.replace_dict(str(child.attribute("play_style")), play_style_dict)
                newprofile.replace_dict("music_memo", music_memo_dict)

        qpro_secret = request.child("qpro_secret")
        if qpro_secret is not None:
            qpro_secret_dict = newprofile.get_dict("qpro_secret")
            qpro_secret_dict.replace_int_array("head", 8, qpro_secret.child_value("head"))
            qpro_secret_dict.replace_int_array("hair", 8, qpro_secret.child_value("hair"))
            qpro_secret_dict.replace_int_array("face", 8, qpro_secret.child_value("face"))
            qpro_secret_dict.replace_int_array("body", 8, qpro_secret.child_value("body"))
            qpro_secret_dict.replace_int_array("hand", 8, qpro_secret.child_value("hand"))
            newprofile.replace_dict("qpro_secret", qpro_secret_dict)

        qpro_equip = request.child("qpro_equip")
        if qpro_equip is not None:
            qpro_dict = newprofile.get_dict("qpro")
            qpro_dict.replace_int("head", int(qpro_equip.attribute("head")))
            qpro_dict.replace_int("hair", int(qpro_equip.attribute("hair")))
            qpro_dict.replace_int("face", int(qpro_equip.attribute("face")))
            qpro_dict.replace_int("body", int(qpro_equip.attribute("body")))
            qpro_dict.replace_int("hand", int(qpro_equip.attribute("hand")))
            newprofile.replace_dict("qpro", qpro_dict)

        step = request.child("step")
        if step is not None:
            step_dict = newprofile.get_dict("step")
            step_dict.replace_int("enemy_damage", int(step.attribute("enemy_damage")))
            step_dict.replace_int("progress", int(step.attribute("progress")))
            step_dict.replace_int("total_point", int(step.attribute("total_point")))
            step_dict.replace_int("enemy_defeat_flg", int(step.attribute("enemy_defeat_flg")))
            step_dict.replace_int("sp_level", int(step.attribute("sp_level")))
            step_dict.replace_int("dp_level", int(step.attribute("dp_level")))
            step_dict.replace_int("sp_fluctuation", int(step.attribute("sp_fluctuation")))
            step_dict.replace_int("dp_fluctuation", int(step.attribute("dp_fluctuation")))
            step_dict.replace_int("mission_clear_num", int(step.attribute("mission_clear_num")))
            step_dict.replace_int("sp_mplay", int(step.attribute("sp_mplay")))
            step_dict.replace_int("dp_mplay", int(step.attribute("dp_mplay")))
            step_dict.replace_int("tips_read_list", int(step.attribute("tips_read_list")))
            step_dict.replace_bool("is_track_ticket", step.child_value("is_track_ticket"))
            newprofile.replace_dict("step", step_dict)

        achievements = request.child("achievements")
        if achievements is not None:
            achievements_dict = newprofile.get_dict("achievements")
            achievements_dict.replace_int("visit_flg", int(achievements.attribute("visit_flg")))
            achievements_dict.replace_int("last_weekly", int(achievements.attribute("last_weekly")))
            achievements_dict.replace_int("weekly_num", int(achievements.attribute("weekly_num")))

            pack_id = int(achievements.attribute("pack_id"))
            if pack_id > 0:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    pack_id,
                    "daily",
                    {
                        "pack_flg": int(achievements.attribute("pack_flg")),
                        "pack_comp": int(achievements.attribute("pack_comp")),
                    },
                )

            trophies = achievements.child("trophy")
            if trophies is not None:
                # We only load the first 20 in profile load.
                achievements_dict.replace_int_array("trophy", 20, trophies.value[:20])

            newprofile.replace_dict("achievements", achievements_dict)

        notes_radar = request.child("notes_radar")
        if notes_radar is not None:
            notes_radar_dict = newprofile.get_dict("notes_radar")
            for child in notes_radar.children:
                if child.name != "radar_score":
                    continue
                notes_radar_dict.replace_int_array(str(notes_radar.attribute("style")), 6, child.value)
            newprofile.replace_dict("notes_radar", notes_radar_dict)

        # Missing shitei node

        # Deller saving
        deller = request.child("deller")
        if deller is not None:
            newprofile.replace_int("deller", newprofile.get_int("deller") + int(deller.attribute("deller")))

        # Orb data saving
        orb_data = request.child("orb_data")
        if orb_data is not None:
            orbs = newprofile.get_int("orbs")
            orbs = orbs + int(orb_data.attribute("add_orb"))
            if orb_data.child_value("use_vip_pass"):
                orbs = 0
            newprofile.replace_int("orbs", orbs)

        return newprofile
