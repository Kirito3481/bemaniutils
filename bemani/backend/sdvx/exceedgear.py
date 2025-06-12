from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Final

from bemani.backend.ess import EventLogHandler
from bemani.backend.sdvx.base import SoundVoltexBase
from bemani.backend.sdvx.vividwave import SoundVoltexVividWave
from bemani.common import ID, Profile, VersionConstants
from bemani.data import Score, UserID
from bemani.protocol import Node


class SoundVoltexExceedGear(
    EventLogHandler,
    SoundVoltexBase,
):
    name: str = "SOUND VOLTEX EXCEED GEAR"
    version: int = VersionConstants.SDVX_EXCEED_GEAR

    GAME_LIMITED_LOCKED: Final[int] = 1
    GAME_LIMITED_UNLOCKABLE: Final[int] = 2
    GAME_LIMITED_UNLOCKED: Final[int] = 3

    GAME_CURRENCY_PACKETS: Final[int] = 0
    GAME_CURRENCY_BLOCKS: Final[int] = 1

    GAME_CATALOG_TYPE_SONG: Final[int] = 0
    GAME_CATALOG_TYPE_APPEAL_CARD: Final[int] = 1
    GAME_CATALOG_TYPE_CREW: Final[int] = 4

    # Return the local2 service so that SDVX 6 and above will send certain packets.
    extra_services: List[str] = [
        "local2",
    ]

    def previous_version(self) -> Optional[SoundVoltexBase]:
        return SoundVoltexVividWave(self.data, self.config, self.model)

    def handle_game_sv6_common_request(self, request: Node) -> Node:
        game = Node.void("game")

        music_limited = Node.void("music_limited")
        game.add_child(music_limited)

        # Event config
        event = Node.void("event")
        game.add_child(event)

        def enable_event(eid: str) -> None:
            evt = Node.void("info")
            event.add_child(evt)
            evt.add_child(Node.string("event_id", eid))

        enable_event("DISP_PASELI_BANNER")
        enable_event("CLOUD_LINK_ENABLE")
        enable_event("MEGAMIX_ENABLE")
        enable_event("ARENA_ENABLE")
        enable_event("PREMIUM_TIME_ENABLE")
        enable_event("BLASTER_ABLE")
        enable_event("SKILL_ANALYZER_ABLE")
        enable_event("VOLFORCE_ENABLE")
        enable_event("MATCHING_MODE")
        enable_event("MATCHING_MODE_FREE_IP")
        enable_event("PAUSE_ONLINEUPDATE")
        # enable_event("APRIL_GRACE")
        enable_event("DISABLE_MONITOR_ID_CHECK")
        enable_event("PLAYERJUDGEADJ_ENABLE")
        enable_event("STANDARD_UNLOCK_ENABLE")
        enable_event("GENERATOR_ABLE")
        enable_event("CREW_SELECT_ABLE")
        enable_event("VALGENE_ENABLE")
        enable_event("TENKAICHI_MODE")
        enable_event("TENKAICHI_MODE")
        enable_event("ICON_POLICY_BREAK")
        enable_event("ICON_FLOOR_INFECTION")
        # enable_event("BEMANI_VOTING_2019_ENABLE")
        enable_event("KONAMI_50TH_LOGO")
        enable_event("ACHIEVEMENT_ENABLE")
        enable_event("TOTAL_MEMORIAL_ENABLE")
        enable_event("PCBSTATE_CABINETGROUPID")
        enable_event("EVENTDATE_APRILFOOL")
        enable_event("EVENTDATE_ONIGO")
        enable_event("EVENTDATE_GOTT")
        enable_event("MIXID_INPUT_ENABLE")
        enable_event("OMEGA_ENABLE\t1,2,3,4,5,6,7,8,9")
        enable_event("HEXA_ENABLE\t1,2,3")

        return game

    def handle_game_sv6_load_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        root = self.get_profile_by_refid(refid)
        if root is not None:
            return root

        # Figure out if this user has an older profile or not
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)

        if userid is not None:
            previous_game = self.previous_version()
        else:
            previous_game = None

        if previous_game is not None:
            profile = previous_game.get_profile(userid)
        else:
            profile = None

        if profile is not None:
            root = Node.void("game")
            root.add_child(Node.u8("result", 2))
            root.add_child(Node.string("name", profile.get_str("name")))
            return root
        else:
            root = Node.void("game")
            root.add_child(Node.u8("result", 1))
            return root

    def handle_game_sv6_frozen_request(self, request: Node) -> Node:
        game = Node.void("game")
        game.add_child(Node.u8("result", 0))
        return game

    def handle_game_sv6_new_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        name = request.child_value("name")
        loc = ID.parse_machine_id(request.child_value("locid"))
        self.new_profile_by_refid(refid, name, loc)

        root = Node.void("game")
        return root

    def handle_game_sv6_load_m_request(self, request: Node) -> Node:
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            scores = self.data.remote.music.get_scores(self.game, self.version, userid)
        else:
            scores = []

        # Output to the game
        game = Node.void("game")
        music = Node.void("music")
        game.add_child(music)

        for score in scores:
            info = Node.void("info")
            music.add_child(info)

            stats = score.data.get_dict("stats")
            info.add_child(
                Node.u32_array(
                    "param",
                    [
                        score.id,
                        score.chart,
                        score.points,
                        self.__db_to_game_clear_type(score.data.get_int("clear_type")),
                        self.__db_to_game_grade(score.data.get_int("grade")),
                        0,  # 5: Any value
                        0,  # 6: Any value
                        stats.get_int("btn_rate"),
                        stats.get_int("long_rate"),
                        stats.get_int("vol_rate"),
                        0,  # 10: Any value
                        0,  # 11: Another medal, perhaps old score medal?
                        0,  # 12: Another grade, perhaps old score grade?
                        0,  # 13: Any value
                        0,  # 14: Any value
                        0,  # 15: Any value
                        0,  # 16: Another medal, perhaps old score medal?
                        0,  # 17: Another grade, perhaps old score grade?
                        0,  # 18: Any value
                        0,  # 19: Any value
                    ],
                ),
            )

        return game

    def handle_game_sv6_load_r_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        game = Node.void("game")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            links = self.data.local.user.get_links(self.game, self.version, userid)
            index = 0
            for link in links:
                if link.type != "rival":
                    continue
                other_profile = self.get_profile(link.other_userid)
                if other_profile is None:
                    continue

                # Base information about rival
                rival = Node.void("rival")
                game.add_child(rival)
                rival.add_child(Node.s16("no", index))
                rival.add_child(Node.string("seq", ID.format_extid(other_profile.extid)))
                rival.add_child(Node.string("name", other_profile.get_str("name")))

                # Keep track of index
                index = index + 1

                # Return scores for this user on random charts
                scores = self.data.remote.music.get_scores(self.game, self.version, link.other_userid)
                for score in scores:
                    music = Node.void("music")
                    rival.add_child(music)
                    music.add_child(
                        Node.u32_array(
                            "param",
                            [
                                score.id,
                                score.chart,
                                score.points,
                                self.__db_to_game_clear_type(score.data.get_int("clear_type")),
                                self.__db_to_game_grade(score.data.get_int("grade")),
                            ],
                        )
                    )

        return game

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        game = Node.void("game")

        # Generic profile stuff
        game.add_child(Node.string("name", profile.get_str("name")))
        game.add_child(Node.string("code", ID.format_extid(profile.extid)))
        game.add_child(Node.string("sdvx_id", ID.format_extid(profile.extid)))
        game.add_child(Node.u16("appeal_id", profile.get_int("appealid")))
        game.add_child(Node.s16("skill_base_id", profile.get_int("skill_base_id")))
        game.add_child(Node.s16("skill_name_id", profile.get_int("skill_name_id")))
        game.add_child(Node.u32("gamecoin_packet", profile.get_int("packet")))
        game.add_child(Node.u32("gamecoin_block", profile.get_int("block")))
        game.add_child(Node.u32("blaster_energy", profile.get_int("blaster_energy")))
        game.add_child(Node.u32("blaster_count", profile.get_int("blaster_count")))

        # Play statistics
        statistics = self.get_play_statistics(userid)
        game.add_child(Node.u32("play_count", statistics.total_plays))
        game.add_child(Node.u32("today_count", statistics.today_plays))
        game.add_child(Node.u32("play_chain", statistics.consecutive_days))

        # Also exists but we don't support:
        # - day_count: Number of days where this user had at least one play.
        # - max_play_chain: Max consecutive days in a row where the user had at last one play.
        # - week_count: Number of weeks here this user had at least one play.
        # - week_play_count: Number of plays in the last week (I think).
        # - week_chain: Number of weeks in a row where the user had at least one play in that week.
        # - max_week_chain: Maximum number of weeks in a row where the user had at least one play in that week.

        # Player options and last touched song.
        lastdict = profile.get_dict("last")
        game.add_child(Node.s32("hispeed", lastdict.get_int("hispeed")))
        game.add_child(Node.u32("lanespeed", lastdict.get_int("lanespeed")))
        game.add_child(Node.u8("gauge_option", lastdict.get_int("gauge_option")))
        game.add_child(Node.u8("ars_option", lastdict.get_int("ars_option")))
        game.add_child(Node.u8("notes_option", lastdict.get_int("notes_option")))
        game.add_child(Node.u8("early_late_disp", lastdict.get_int("early_late_disp")))
        game.add_child(Node.s32("draw_adjust", lastdict.get_int("draw_adjust")))
        game.add_child(Node.u8("eff_c_left", lastdict.get_int("eff_c_left")))
        game.add_child(Node.u8("eff_c_right", lastdict.get_int("eff_c_right", 1)))
        game.add_child(Node.s32("last_music_id", lastdict.get_int("music_id", -1)))
        game.add_child(Node.u8("last_music_type", lastdict.get_int("music_type")))
        game.add_child(Node.u8("sort_type", lastdict.get_int("sort_type")))
        game.add_child(Node.u8("narrow_down", lastdict.get_int("narrow_down")))
        game.add_child(Node.u8("headphone", lastdict.get_int("headphone")))

        # Item unlocks
        itemnode = Node.void("item")
        game.add_child(itemnode)

        game_config = self.get_game_config()
        achievements = self.data.local.user.get_achievements(self.game, self.version, userid)

        for item in achievements:
            if item.type[:5] != "item_":
                continue
            itemtype = int(item.type[5:])

            if game_config.get_bool("force_unlock_songs") and itemtype == self.GAME_CATALOG_TYPE_SONG:
                # Don't echo unlocked songs, we will add all of them later
                continue
            if game_config.get_bool("force_unlock_cards") and itemtype == self.GAME_CATALOG_TYPE_APPEAL_CARD:
                # Don't echo unlocked appeal cards, we will add all of them later
                continue
            if game_config.get_bool("force_unlock_crew") and itemtype == self.GAME_CATALOG_TYPE_CREW:
                # Don't echo unlocked crew, we will add all of them later
                continue

            info = Node.void("info")
            itemnode.add_child(info)
            info.add_child(Node.u8("type", itemtype))
            info.add_child(Node.u32("id", item.id))
            info.add_child(Node.u32("param", item.data.get_int("param")))

        if game_config.get_bool("force_unlock_songs"):
            ids: Dict[int, int] = {}
            songs = self.data.local.music.get_all_songs(self.game, self.version)
            for song in songs:
                if song.id not in ids:
                    ids[song.id] = 0

                if song.data.get_int("difficulty") > 0:
                    ids[song.id] = ids[song.id] | (1 << song.chart)

            for itemid in ids:
                if ids[itemid] == 0:
                    continue

                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", self.GAME_CATALOG_TYPE_SONG))
                info.add_child(Node.u32("id", itemid))
                info.add_child(Node.u32("param", ids[itemid]))

        if game_config.get_bool("force_unlock_cards"):
            catalog = self.data.local.game.get_items(self.game, self.version)
            for unlock in catalog:
                if unlock.type != "appealcard":
                    continue

                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", self.GAME_CATALOG_TYPE_APPEAL_CARD))
                info.add_child(Node.u32("id", unlock.id))
                info.add_child(Node.u32("param", 1))

        if game_config.get_bool("force_unlock_crew"):
            for crewid in range(1, 999):
                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", self.GAME_CATALOG_TYPE_CREW))
                info.add_child(Node.u32("id", crewid))
                info.add_child(Node.u32("param", 1))

            for crewid in range(0, 300):
                info = Node.void("info")
                itemnode.add_child(info)
                info.add_child(Node.u8("type", 11))
                info.add_child(Node.u32("id", crewid))
                info.add_child(Node.u32("param", 15))

            # MITSURU's voice
            info = Node.void("info")
            itemnode.add_child(info)
            info.add_child(Node.u8("type", self.GAME_CATALOG_TYPE_CREW))
            info.add_child(Node.u32("id", 599))
            info.add_child(Node.u32("param", 10))

        # Skill courses
        skill = Node.void("skill")
        game.add_child(skill)
        skill_level = 0

        for course in achievements:
            if course.type != "course":
                continue

            course_id = course.id % 100
            season_id = int(course.id / 100)

            if course.data.get_int("clear_type") >= 2:
                # The user cleared this, lets take the highest level clear for this
                courselist = [
                    c
                    for c in self.__get_skill_analyzer_courses()
                    if c.get("course_id", c.get("skill_level", -1)) == course_id and c["season_id"] == season_id
                ]
                if len(courselist) > 0:
                    skill_level = max(skill_level, courselist[0]["skill_level"])

            course_node = Node.void("course")
            skill.add_child(course_node)
            course_node.add_child(Node.s16("ssnid", season_id))
            course_node.add_child(Node.s16("crsid", course_id))
            course_node.add_child(Node.s32("sc", course.data.get_int("score")))
            course_node.add_child(Node.s16("ct", course.data.get_int("clear_type")))
            course_node.add_child(Node.s16("gr", course.data.get_int("grade")))
            course_node.add_child(Node.s16("ar", course.data.get_int("achievement_rate")))
            course_node.add_child(Node.s16("cnt", 1))

        # Calculated skill level
        game.add_child(Node.s16("skill_level", skill_level))

        # Game parameters
        paramnode = Node.void("param")
        game.add_child(paramnode)

        for param in achievements:
            if param.type[:6] != "param_":
                continue
            paramtype = int(param.type[6:])

            info = Node.void("info")
            paramnode.add_child(info)
            info.add_child(Node.s32("id", param.id))
            info.add_child(Node.s32("type", paramtype))
            info.add_child(
                Node.s32_array("param", param.data["param"])
            )  # This looks to be variable, so no validation on length

        # Infection nodes, we don't support these but it here for posterity.
        pbc_infection = Node.void("pbc_infection")
        game.add_child(pbc_infection)
        for name in ["packet", "block", "coloris"]:
            child = Node.void(name)
            pbc_infection.add_child(child)
            child.add_child(Node.s32("before", 0))
            child.add_child(Node.s32("after", 0))

        pb_infection = Node.void("pb_infection")
        game.add_child(pb_infection)
        for name in ["packet", "block"]:
            child = Node.void(name)
            pb_infection.add_child(child)
            child.add_child(Node.s32("before", 0))
            child.add_child(Node.s32("after", 0))

        return game