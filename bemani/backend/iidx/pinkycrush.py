# vim: set fileencoding=utf-8
from typing import Optional
from typing_extensions import Final

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.stubs import IIDXEpolis

from bemani.common import Profile, VersionConstants, ID
from bemani.data import UserID
from bemani.protocol import Node


class IIDXPinkyCrush(IIDXBase):
    name: str = "Beatmania IIDX Pinky Crush"
    version: int = VersionConstants.IIDX_PINKY_CRUSH

    GAME_CLTYPE_SINGLE: Final[int] = 0
    GAME_CLTYPE_DOUBLE: Final[int] = 1

    DAN_STAGES: Final[int] = 4

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

    requires_extended_regions: bool = True

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXEpolis(self.data, self.config, self.model)

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
                self.GAME_SP_DAN_RANK_CHUDEN: self.DAN_RANK_CHUDEN,
                self.GAME_SP_DAN_RANK_KAIDEN: self.DAN_RANK_KAIDEN,
            }[game_dan]
        elif cltype == self.GAME_CLTYPE_DOUBLE:
            return {
                self.GAME_DP_DAN_RANK_7_KYU: self.DAN_RANK_7_KYU,
                self.GAME_DP_DAN_RANK_6_KYU: self.DAN_RANK_6_KYU,
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
                self.GAME_DP_DAN_RANK_CHUDEN: self.DAN_RANK_CHUDEN,
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

    def handle_IIDX32shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("IIDX32shop")

    def handle_IIDX32gameSystem_systemInfo_request(self, request: Node) -> Node:
        root = Node.void("IIDX32gameSystem")

        arena_schedule = Node.void("arena_schedule")
        root.add_child(arena_schedule)
        arena_schedule.add_child(Node.u8("season", 1))
        arena_schedule.add_child(Node.u8("phase", 2))
        arena_schedule.add_child(Node.u8("rule_type", 2))  # rules: 0=no rule, 1=miss count, 2=note radar pick
        arena_schedule.add_child(Node.u32("start", 0))
        arena_schedule.add_child(Node.u32("end", 0))

        Event1Phase = Node.void("Event1Phase")
        root.add_child(Event1Phase)
        Event1Phase.set_attribute("val", "0")

        Event1Value = Node.void("Event1Value")
        root.add_child(Event1Value)
        Event1Value.set_attribute("val", "0")

        return root

    def handle_IIDX32music_getrank_request(self, request: Node) -> Node:
        cltype = int(request.attribute("cltype"))

        root = Node.void("IIDX32music")
        style = Node.void("style")
        root.add_child(style)
        style.set_attribute("type", str(cltype))

        return root

    def handle_IIDX32music_reg_request(self, request: Node) -> Node:
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

        if userid is not None:
            clear_status = self.game_to_db_status(int(request.attribute("cflg")))
            pgreats = int(request.attribute("pgnum"))
            greats = int(request.attribute("gnum"))
            miss_count = int(request.attribute("mnum"))
            ghost = request.child_value("ghost")
            shopid = ID.parse_machine_id(request.attribute("convid"))

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
        root = Node.void("IIDX32music")
        root.set_attribute("clid", request.attribute("clid"))
        root.set_attribute("mid", request.attribute("mid"))

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
        root.set_attribute("rankside", "0")

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

        return root

    def handle_IIDX32pc_common_request(self, request: Node) -> Node:
        root = Node.void("IIDX32pc")
        root.set_attribute("expire", "1")

        ir = Node.void("ir")
        root.add_child(ir)
        ir.set_attribute("beat", "1")

        movie_agreement = Node.void("movie_agreement")
        root.add_child(movie_agreement)
        movie_agreement.set_attribute("version", "1")

        license = Node.void("license")
        root.add_child(license)
        license.add_child(Node.string("string", "LICENSE"))

        file_recovery = Node.void("file_recovery")
        root.add_child(file_recovery)
        file_recovery.set_attribute("url", "http://localhost/recovery")

        movie_upload = Node.void("movie_upload")
        root.add_child(movie_upload)
        movie_upload.set_attribute("url", "http://localhost/upload")

        root.add_child(Node.void("vip_pass_black"))

        deller_bonus = Node.void("deller_bonus")
        root.add_child(deller_bonus)
        deller_bonus.set_attribute("open", "1")

        pcb_check = Node.void("pcb_check")
        root.add_child(pcb_check)
        pcb_check.set_attribute("flg", "1")

        common_evnet = Node.void("common_evnet")
        root.add_child(common_evnet)
        common_evnet.set_attribute("flg", "1")

        play_video = Node.void("play_video")
        root.add_child(play_video)

        music_retry = Node.void("music_retry")
        root.add_child(music_retry)

        display_asio_logo = Node.void("display_asio_logo")
        root.add_child(display_asio_logo)

        # ranking node missing

        # root.add_child(Node.void("lane_gacha"))
        root.add_child(Node.void("fps_fix"))
        root.add_child(Node.void("save_unsync_log"))
        root.add_child(Node.void("fix_framerate"))
        root.add_child(Node.void("fix_real"))
        # tourism_booster node missing
        # root.add_child(Node.void("tsujigiri_event"))
        # root.add_child(Node.void("questionnaire_list"))

        return root

    def handle_IIDX32pc_getLaneGachaTicket_request(self, request: Node) -> Node:
        return Node.void("IIDX32pc")

    def handle_IIDX32pc_delete_request(self, request: Node) -> Node:
        return Node.void("IIDX32pc")

    def handle_IIDX32pc_playstart_request(self, request: Node) -> Node:
        return Node.void("IIDX32pc")

    def handle_IIDX32pc_playend_request(self, request: Node) -> Node:
        return Node.void("IIDX32pc")

    def handle_IIDX32pc_oldget_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            oldversion = self.previous_version()
            profile = oldversion.get_profile(userid)
        else:
            profile = None

        root = Node.void("IIDX32pc")
        root.set_attribute("status", "1" if profile is None else "0")
        return root

    def handle_IIDX32pc_getCompeInfo_request(self, request: Node) -> Node:
        return Node.void("IIDX32pc")

    def handle_IIDX32pc_reg_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        name = request.attribute("name")
        pid = int(request.attribute("pid"))
        profile = self.new_profile_by_refid(refid, name, pid)

        root = Node.void("IIDX32pc")
        if profile is not None:
            root.set_attribute("id", str(profile.extid))
            root.set_attribute("id_str", ID.format_extid(profile.extid))
        return root

    def handle_IIDX32pc_get_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("IIDX32pc")
        return root

    def handle_IIDX32pc_visit_request(self, request: Node) -> Node:
        root = Node.void("IIDX32pc")
        root.set_attribute("anum", "0")
        root.set_attribute("snum", "0")
        root.set_attribute("pnum", "0")
        root.set_attribute("aflg", "0")
        root.set_attribute("sflg", "0")
        root.set_attribute("pflg", "0")
        return root

    def handle_IIDX32pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        self.put_profile_by_extid(extid, request)

        return Node.void("IIDX32pc")

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("IIDX32pc")

        # Look up play stats we bridge to every mix
        play_stats = self.get_play_statistics(userid)

        # Look up judge window adjustments
        judge_dict = profile.get_dict("machine_judge_adjust")
        machine_judge = judge_dict.get_dict(self.config.machine.pcbid)

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
        pcdata.set_attribute("category", str(profile.get_int("category")))
        pcdata.set_attribute("pmode", str(profile.get_int("pmode")))
        pcdata.set_attribute("ngrade", str(profile.get_int("ngrade")))
        pcdata.set_attribute("rtype", str(profile.get_int("rtype")))
        pcdata.set_attribute("bgnflg", str(profile.get_int("bgnflg")))
        pcdata.set_attribute("player_kind", str(profile.get_int("player_kind")))
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
        pcdata.set_attribute("s_notes", str(profile.get_float("s_notes")))
        pcdata.set_attribute("d_notes", str(profile.get_float("d_notes")))
        pcdata.set_attribute("s_judge", str(profile.get_int("s_judge")))
        pcdata.set_attribute("d_judge", str(profile.get_int("d_judge")))
        pcdata.set_attribute("s_judgeAdj", str(machine_judge.get_int("single")))
        pcdata.set_attribute("d_judgeAdj", str(machine_judge.get_int("double")))
        pcdata.set_attribute("s_hispeed", str(profile.get_float("s_hispeed")))
        pcdata.set_attribute("d_hispeed", str(profile.get_float("d_hispeed")))
        pcdata.set_attribute("s_liflen", str(profile.get_int("s_lift")))
        pcdata.set_attribute("d_liflen", str(profile.get_int("d_lift")))
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
        pcdata.set_attribute("s_classic_hispeed", str(profile.get_int("s_classic_hispeed")))
        pcdata.set_attribute("d_classic_hispeed", str(profile.get_int("d_classic_hispeed")))
        pcdata.set_attribute("movie_thumbnail", str(profile.get_int("movie_thumbnail")))

        # Lightning model play data
        lightning_play_data = Node.void("lightning_play_data")
        root.add_child(lightning_play_data)
        lightning_play_data.set_attribute("spnum", str(play_stats.get_int("lightning_single_plays")))
        lightning_play_data.set_attribute("dpnum", str(play_stats.get_int("lightning_double_plays")))

        # Lightning model settings
        lightning_settings_dict = profile.get_dict("lightning_settings")
        lightning_setting = Node.void("lightning_setting")
        root.add_child(lightning_setting)
        lightning_setting.set_attribute("headphone_vol", str(lightning_settings_dict.get_int("headphone_vol", 10)))
        lightning_setting.set_attribute(
            "resistance_sp_left", str(lightning_settings_dict.get_int("resistance_sp_left", 4))
        )
        lightning_setting.set_attribute(
            "resistance_sp_right", str(lightning_settings_dict.get_int("resistance_sp_right", 4))
        )
        lightning_setting.set_attribute(
            "resistance_dp_left", str(lightning_settings_dict.get_int("resistance_dp_left", 4))
        )
        lightning_setting.set_attribute(
            "resistance_dp_right", str(lightning_settings_dict.get_int("resistance_dp_right", 4))
        )
        lightning_setting.set_attribute(
            "keyboard_kind", str(lightning_settings_dict.get_int("keyboard_kind", 10))
        )  # set qwerty keyboard
        lightning_setting.set_attribute("brightness", str(lightning_settings_dict.get_int("brightness", 0)))
        lightning_setting.add_child(
            Node.s32_array("slider", lightning_settings_dict.get_int_array("slider", 7, [7, 7, 7, 7, 7, 15, 15]))
        )
        lightning_setting.add_child(
            Node.bool_array(
                "light",
                lightning_settings_dict.get_bool_array(
                    "light", 10, [True, True, True, True, True, True, True, True, True, True]
                ),
            )
        )
        lightning_setting.add_child(
            Node.bool("concentration", lightning_settings_dict.get_bool("concentration", False))
        )

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
        achievements = self.data.local.user.get_achievements(self.game, self.version, userid)
        for rank in achievements:
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

        # Rivals
        rlist = Node.void("rlist")
        root.add_child(rlist)
        links = self.data.local.user.get_links(self.game, self.version, userid)

        rlist_sub = Node.void("rlist_sub")
        root.add_child(rlist_sub)

        language_setting = Node.void("language_setting")
        root.add_child(language_setting)
        language_setting.set_attribute("language", str(profile.get_int("language", 0)))

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        play_stats = self.get_play_statistics(userid)

        # Track play counts
        cltype = int(request.attribute("cltype"))
        if cltype == self.GAME_CLTYPE_SINGLE:
            play_stats.increment_int("single_plays")
            if request.child("lightning_play_data") is not None:
                play_stats.increment_int("lightning_single_plays")
        if cltype == self.GAME_CLTYPE_DOUBLE:
            play_stats.increment_int("double_plays")
            if request.child("lightning_play_data") is not None:
                play_stats.increment_int("lightning_double_plays")

        # Track DJ points
        play_stats.replace_int("single_dj_points", int(request.attribute("s_achi")))
        play_stats.replace_int("double_dj_points", int(request.attribute("d_achi")))

        # Profile settings
        newprofile.replace_int("sp_opt", int(request.attribute("sp_opt")))
        newprofile.replace_int("dp_opt", int(request.attribute("dp_opt")))
        newprofile.replace_int("dp_opt2", int(request.attribute("dp_opt2")))
        newprofile.replace_int("gpos", int(request.attribute("gpos")))
        newprofile.replace_int("s_sorttype", int(request.attribute("s_sorttype")))
        newprofile.replace_int("d_sorttype", int(request.attribute("d_sorttype")))
        newprofile.replace_int("s_disp_judge", int(request.attribute("s_disp_judge")))
        newprofile.replace_int("d_disp_judge", int(request.attribute("d_disp_judge")))
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
        newprofile.replace_float("s_hispeed", float(request.attribute("s_hispeed")))
        newprofile.replace_float("d_hispeed", float(request.attribute("d_hispeed")))
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
        newprofile.replace_int("s_classic_hispeed", int(request.attribute("s_classic_hispeed")))
        newprofile.replace_int("d_classic_hispeed", int(request.attribute("d_classic_hispeed")))
        newprofile.replace_int("movie_thumbnail", int(request.attribute("movie_thumbnail")))
        newprofile.replace_int("s_lift", int(request.attribute("s_lift")))
        newprofile.replace_int("d_lift", int(request.attribute("d_lift")))
        newprofile.replace_int("mode", int(request.attribute("mode")))
        newprofile.replace_int("category", int(request.attribute("category")))
        newprofile.replace_int("pmode", int(request.attribute("pmode")))
        newprofile.replace_int("ngrade", int(request.attribute("ngrade")))
        newprofile.replace_int("rtype", int(request.attribute("rtype")))
        newprofile.replace_int("bgnflg", int(request.attribute("bgnflg")))

        # Update judge window adjustments per-machine
        judge_dict = newprofile.get_dict("machine_judge_adjust")
        machine_judge = judge_dict.get_dict(self.config.machine.pcbid)
        machine_judge.replace_int("single", int(request.attribute("s_judgeAdj")))
        machine_judge.replace_int("double", int(request.attribute("d_judgeAdj")))
        judge_dict.replace_dict(self.config.machine.pcbid, machine_judge)
        newprofile.replace_dict("machine_judge_adjust", judge_dict)

        # Lightning model settings saving
        lightning_setting = request.child("lightning_setting")
        if lightning_setting is not None:
            lightning_settings_dict = newprofile.get_dict("lightning_settings")
            lightning_settings_dict.replace_int("headphone_vol", int(lightning_setting.attribute("headphone_vol")))
            lightning_settings_dict.replace_int(
                "resistance_sp_left", int(lightning_setting.attribute("resistance_sp_left"))
            )
            lightning_settings_dict.replace_int(
                "resistance_sp_right", int(lightning_setting.attribute("resistance_sp_right"))
            )
            lightning_settings_dict.replace_int(
                "resistance_dp_left", int(lightning_setting.attribute("resistance_dp_left"))
            )
            lightning_settings_dict.replace_int(
                "resistance_dp_right", int(lightning_setting.attribute("resistance_dp_right"))
            )
            lightning_settings_dict.replace_int("keyboard_kind", int(lightning_setting.attribute("keyboard_kind")))
            lightning_settings_dict.replace_int("brightness", int(lightning_setting.attribute("brightness")))
            lightning_settings_dict.replace_int_array("slider", 7, lightning_setting.child_value("slider"))
            lightning_settings_dict.replace_bool_array("light", 10, lightning_setting.child_value("light"))
            lightning_settings_dict.replace_bool("concentration", lightning_setting.child_value("concentration"))
            newprofile.replace_dict("lightning_settings", lightning_settings_dict)

        # Secret flags saving
        game_config = self.get_game_config()
        if not game_config.get_bool("force_unlock_songs"):
            secret = request.child("secret")
            if secret is not None:
                secret_dict = newprofile.get_dict("secret")
                secret_dict.replace_int_array("flg1", 3, secret.child_value("flg1"))
                secret_dict.replace_int_array("flg2", 3, secret.child_value("flg2"))
                secret_dict.replace_int_array("flg3", 3, secret.child_value("flg3"))
                secret_dict.replace_int_array("flg4", 3, secret.child_value("flg4"))
                secret_dict.replace_int_array("flg5", 3, secret.child_value("flg5"))
                newprofile.replace_dict("secret", secret_dict)

        # Leggendaria flags saving
        game_config = self.get_game_config()
        if not game_config.get_bool("force_unlock_songs"):
            leggendaria = request.child("leggendaria")
            if leggendaria is not None:
                leggendaria_dict = newprofile.get_dict("leggendaria")
                leggendaria_dict.replace_int_array("flg1", 3, leggendaria.child_value("flg1"))
                leggendaria_dict.replace_int_array("flg2", 3, leggendaria.child_value("flg2"))
                newprofile.replace_dict("leggendaria", leggendaria_dict)

        # Qpro secret saving
        qpro_secret = request.child("qpro_secret")
        if qpro_secret is not None:
            qpro_secret_dict = newprofile.get_dict("qpro_secret")
            qpro_secret_dict.replace_int("head", int(qpro_secret.attribute("head")))
            qpro_secret_dict.replace_int("hair", int(qpro_secret.attribute("hair")))
            qpro_secret_dict.replace_int("face", int(qpro_secret.attribute("face")))
            qpro_secret_dict.replace_int("body", int(qpro_secret.attribute("body")))
            qpro_secret_dict.replace_int("hand", int(qpro_secret.attribute("hand")))
            qpro_secret_dict.replace_int("back", int(qpro_secret.attribute("back")))
            newprofile.replace_dict("qpro_secret", qpro_secret_dict)

        # Step-up mode
        step = request.child("step")
        if step is not None:
            step_dict = newprofile.get_dict("step")
            step_dict.replace_int("enemy_damage", int(step.attribute("enemy_damage")))
            step_dict.replace_int("progress", int(step.attribute("progress")))
            step_dict.replace_int("total_point", int(step.attribute("total_point")))
            step_dict.replace_int("enemy_defeat_flg", int(step.attribute("enemy_defeat_flg")))
            step_dict.replace_bool("is_track_ticket", bool(step.child_value("is_track_ticket")))
            step_dict.replace_int("sp_level", int(step.attribute("sp_level")))
            step_dict.replace_int("dp_level", int(step.attribute("dp_level")))
            step_dict.replace_int("sp_level_h", int(step.attribute("sp_level_h")))
            step_dict.replace_int("dp_level_h", int(step.attribute("dp_level_h")))
            step_dict.replace_int("sp_level_exh", int(step.attribute("sp_level_exh")))
            step_dict.replace_int("dp_level_exh", int(step.attribute("dp_level_exh")))
            step_dict.replace_int("sp_fluctuation", int(step.attribute("sp_fluctuation")))
            step_dict.replace_int("dp_fluctuation", int(step.attribute("dp_fluctuation")))
            step_dict.replace_int("mission_clear_num", int(step.attribute("mission_clear_num")))
            step_dict.replace_int("sp_mplay", int(step.attribute("sp_mplay")))
            step_dict.replace_int("dp_mplay", int(step.attribute("dp_mplay")))
            step_dict.replace_int("tips_read_list", int(step.attribute("tips_read_list")))
            newprofile.replace_dict("step", step_dict)

        # Basic achievements
        achievements = request.child("achievements")
        if achievements is not None:
            newprofile.replace_int("play_pack", int(achievements.attribute("play_pack")))
            newprofile.replace_int("last_weekly", int(achievements.attribute("last_weekly")))
            newprofile.replace_int("weekly_num", int(achievements.attribute("weekly_num")))
            newprofile.replace_int("visit_flg", int(achievements.attribute("visit_flg")))

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

        # Notes radar saving
        for notes_radar in request.children:
            if notes_radar.name != "notes_radar":
                continue
            radar_dict = newprofile.get_dict("notes_radar")
            if int(notes_radar.attribute("style")) == self.GAME_CLTYPE_SINGLE:
                radar_dict.replace_int_array("single", 6, notes_radar.child_value("radar_score"))
            elif int(notes_radar.attribute("style")) == self.GAME_CLTYPE_DOUBLE:
                radar_dict.replace_int_array("double", 6, notes_radar.child_value("radar_score"))
            newprofile.replace_dict("notes_radar", radar_dict)

        # Deller saving
        deller = request.child("deller")
        if deller is not None:
            newprofile.replace_int("deller", newprofile.get_int("deller") + int(deller.attribute("deller")))

        # Language saving
        language_setting = request.child("language_setting")
        if language_setting is not None:
            newprofile.replace_int("language", int(language_setting.attribute("language")))

        # Keep track of play statistics across all mixes
        self.update_play_statistics(userid, play_stats)

        return newprofile
