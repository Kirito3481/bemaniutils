from typing import Any, Dict, List, Optional, Tuple, Union
from typing_extensions import Final

from bemani.backend.ess import EventLogHandler
from bemani.backend.sdvx.base import SoundVoltexBase
from bemani.backend.sdvx.heavenlyhaven import SoundVoltexHeavenlyHaven
from bemani.common import ID, Profile, VersionConstants
from bemani.data import Score, UserID
from bemani.protocol import Node


class SoundVoltexVividWave(
    EventLogHandler,
    SoundVoltexBase
):
    name: str = "SOUND VOLTEX VIVID WAVE"
    version: int = VersionConstants.SDVX_VIVID_WAVE

    GAME_LIMITED_LOCKED: Final[int] = 1
    GAME_LIMITED_UNLOCKABLE: Final[int] = 2
    GAME_LIMITED_UNLOCKED: Final[int] = 3

    GAME_CURRENCY_PACKETS: Final[int] = 0
    GAME_CURRENCY_BLOCKS: Final[int] = 1

    GAME_CATALOG_TYPE_SONG: Final[int] = 0
    GAME_CATALOG_TYPE_APPEAL_CARD: Final[int] = 1
    GAME_CATALOG_TYPE_CREW: Final[int] = 4

    GAME_CLEAR_TYPE_NO_PLAY: Final[int] = 0
    GAME_CLEAR_TYPE_FAILED: Final[int] = 1
    GAME_CLEAR_TYPE_CLEAR: Final[int] = 2
    GAME_CLEAR_TYPE_HARD_CLEAR: Final[int] = 3
    GAME_CLEAR_TYPE_ULTIMATE_CHAIN: Final[int] = 4
    GAME_CLEAR_TYPE_PERFECT_ULTIMATE_CHAIN: Final[int] = 5

    GAME_GRADE_NO_PLAY: Final[int] = 0
    GAME_GRADE_D: Final[int] = 1
    GAME_GRADE_C: Final[int] = 2
    GAME_GRADE_B: Final[int] = 3
    GAME_GRADE_A: Final[int] = 4
    GAME_GRADE_A_PLUS: Final[int] = 5
    GAME_GRADE_AA: Final[int] = 6
    GAME_GRADE_AA_PLUS: Final[int] = 7
    GAME_GRADE_AAA: Final[int] = 8
    GAME_GRADE_AAA_PLUS: Final[int] = 9
    GAME_GRADE_S: Final[int] = 10

    # Return the local2 service so that SDVX 5 and above will send certain packets.
    extra_services: List[str] = [
        "local2",
    ]

    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """
        Return all of our front-end modifiably settings.
        """
        return {
            "bools": [
                {
                    "name": "Disable Online Matching",
                    "tip": "Disable online matching between games.",
                    "category": "game_config",
                    "setting": "disable_matching",
                },
                {
                    "name": "Force Song Unlock",
                    "tip": "Force unlock all songs.",
                    "category": "game_config",
                    "setting": "force_unlock_songs",
                },
                {
                    "name": "Force Appeal Card Unlock",
                    "tip": "Force unlock all appeal cards.",
                    "category": "game_config",
                    "setting": "force_unlock_cards",
                },
                {
                    "name": "Force Crew Card Unlock",
                    "tip": "Force unlock all crew and subcrew cards.",
                    "category": "game_config",
                    "setting": "force_unlock_crew",
                },
                {
                    "name": "50th Anniversary Celebration",
                    "tip": "Display the 50th anniversary screen in attract mode",
                    "category": "game_config",
                    "setting": "50th_anniversary",
                },
            ],
        }

    def previous_version(self) -> Optional[SoundVoltexBase]:
        return SoundVoltexHeavenlyHaven(self.data, self.config, self.model)

    def handle_game_sv5_entry_s_request(self, request: Node) -> Node:
        game = Node.void("game")
        # This should be created on the fly for a lobby that we're in.
        game.add_child(Node.u32("entry_id", 1))
        return game

    def handle_game_sv5_common_request(self, request: Node) -> Node:
        game = Node.void("game")

        limited = Node.void("music_limited")
        game.add_child(limited)

        # Song unlock config
        game_config = self.get_game_config()
        if game_config.get_bool("force_unlock_songs"):
            ids = set()
            songs = self.data.local.music.get_all_songs(self.game, self.version)
            for song in songs:
                if song.data.get_int("limited") in (
                        self.GAME_LIMITED_LOCKED,
                        self.GAME_LIMITED_UNLOCKABLE,
                ):
                    ids.add((song.id, song.chart))

            for songid, chart in ids:
                info = Node.void("info")
                limited.add_child(info)
                info.add_child(Node.s32("music_id", songid))
                info.add_child(Node.u8("music_type", chart))
                info.add_child(Node.u8("limited", self.GAME_LIMITED_UNLOCKED))

        # Catalog, maybe this is for the online store?
        catalog = Node.void("catalog")
        game.add_child(catalog)

        for _item in []:  # type: ignore
            info = Node.void("info")
            catalog.add_child(info)
            info.add_child(Node.u8("catalog_type", 0))
            info.add_child(Node.u32("catalog_id", 0))
            info.add_child(Node.u32("discount_rate", 0))

        # Event config
        event = Node.void("event")
        game.add_child(event)

        def enable_event(eid: str) -> None:
            evt = Node.void("info")
            event.add_child(evt)
            evt.add_child(Node.string("event_id", eid))

        if not game_config.get_bool("disable_matching"):
            # Matching enabled events
            enable_event("MATCHING_MODE")
            enable_event("MATCHING_MODE_FREE_IP")
        if game_config.get_bool("50th_anniversary"):
            enable_event("KONAMI_50TH_LOGO")
        enable_event("ICON_FLOOR_INFECTION")
        enable_event("ICON_POLICY_BREAK")
        enable_event("DISABLE_MONITOR_ID_CHECK")
        enable_event("VOLFORCE_ENABLE")
        enable_event("ACHIEVEMENT_ENABLE")
        enable_event("PLAYERJUDGEADJ_ENABLE")
        enable_event("PREMIUM_TIME_ENABLE")
        enable_event("GENERATOR_ABLE")
        enable_event("CREW_SELECT_ABLE")
        enable_event("BLASTER_ABLE")
        enable_event("SKILL_ANALYZER_ABLE")
        enable_event("STANDARD_UNLOCK_ENABLE")
        enable_event("EVENTDATE_ONIGO")
        enable_event("EVENTDATE_GOTT")
        enable_event("EVENTDATE_APRILFOOL")
        enable_event("OMEGA_ENABLE\t1,2,3,4,5,6,7,8,9")
        enable_event("HEXA_ENABLE\t1,2,3")
        enable_event("PAUSE_ONLINEUPDATE")
        enable_event("DEMOGAME_PLAY")
        enable_event("TENKAICHI_MODE")
        enable_event("PCBSTATE_CABINETGROUPID")
        enable_event("MIXID_INPUT_ENABLE")

        extend = Node.void("extend")
        game.add_child(extend)

        def add_extend(etype: int, eid: int, params: List[Union[int, str]]):
            info = Node.void("info")
            info.add_child(Node.u32("extend_type", etype))
            info.add_child(Node.u32("extend_id", eid))
            info.add_child(Node.s32("param_num_1", params[0]))
            info.add_child(Node.s32("param_num_2", params[1]))
            info.add_child(Node.s32("param_num_3", params[2]))
            info.add_child(Node.s32("param_num_4", params[3]))
            info.add_child(Node.s32("param_num_5", params[4]))
            info.add_child(Node.string("param_str_1", params[5]))
            info.add_child(Node.string("param_str_2", params[6]))
            info.add_child(Node.string("param_str_3", params[7]))
            info.add_child(Node.string("param_str_4", params[8]))
            info.add_child(Node.string("param_str_5", params[9]))
            extend.add_child(info)

        add_extend(17, 91, [0, 1, 0, 0, 1, "1,2,6,7,8,19,24,25,31,39,42,47,54,55,59,60,63,64,69,86,87,88,94,96,97,98,101,103,109,115,117,120,125,126,127,128,134,135,180,182,192,212,216,224,225,230,241,246,251,252,253,255,256,257,258,259,267,268,269,271,272,286,290,298,299,304,307,312,313,316,324,330,344,349,359,364,365,369,374,381,422,437,471,479,499,500,517,519,538,539,540,541,542,543,546,551,552,553,581,597,606,611,616,623,626,633,634,669,673,678,684,698,699,704,708,717,718,743,788,816,823,831,855,866,903,907,939,961,978,1072,1225,1231,1260,1261,1297,1331,1333,1422,1423,1490,1491,", "0", "0", "0", "0"])

        return game

    def handle_game_sv5_load_request(self, request: Node) -> Node:
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

    def handle_game_sv5_frozen_request(self, request: Node) -> Node:
        game = Node.void("game")
        game.add_child(Node.u8("result", 0))
        return game

    def handle_game_sv5_new_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        name = request.child_value("name")
        loc = ID.parse_machine_id(request.child_value("locid"))
        self.new_profile_by_refid(refid, name, loc)

        root = Node.void("game")
        return root

    def handle_game_sv5_load_m_request(self, request: Node) -> Node:
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

        return game

    def handle_game_sv5_load_r_request(self, request: Node) -> Node:
        refid = request.child_value("refid")
        game = Node.void("game")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        return game

    def handle_game_sv5_save_request(self, request: Node) -> Node:
        refid = request.child_value("refid")

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            oldprofile = self.get_profile(userid)
            newprofile = self.unformat_profile(userid, request, oldprofile)
        else:
            newprofile = None

        if userid is not None and newprofile is not None:
            self.put_profile(userid, newprofile)

        return Node.void("game")

    def handle_game_sv5_play_e_request(self, request: Node) -> Node:
        return Node.void("game")

    def handle_game_sv5_save_e_request(self, request: Node) -> Node:
        # This has to do with Policy floor infection, but we don't
        # implement multi-game support so meh.
        game = Node.void("game")

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

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()

        # Update blaster energy and in-game currencies
        earned_gamecoin_packet = request.child_value("earned_gamecoin_packet")
        if earned_gamecoin_packet is not None:
            newprofile.replace_int("packet", newprofile.get_int("packet") + earned_gamecoin_packet)
        earned_gamecoin_block = request.child_value("earned_gamecoin_block")
        if earned_gamecoin_block is not None:
            newprofile.replace_int("block", newprofile.get_int("block") + earned_gamecoin_block)
        earned_blaster_energy = request.child_value("earned_blaster_energy")
        if earned_blaster_energy is not None:
            newprofile.replace_int(
                "blaster_energy",
                newprofile.get_int("blaster_energy") + earned_blaster_energy,
            )

        # Miscelaneous profile stuff
        newprofile.replace_int("blaster_count", request.child_value("blaster_count"))
        newprofile.replace_int("appealid", request.child_value("appeal_id"))
        newprofile.replace_int("skill_level", request.child_value("skill_level"))
        newprofile.replace_int("skill_base_id", request.child_value("skill_base_id"))
        newprofile.replace_int("skill_name_id", request.child_value("skill_name_id"))

        # Update user's unlock status if we aren't force unlocked
        game_config = self.get_game_config()

        if request.child("item") is not None:
            for child in request.child("item").children:
                if child.name != "info":
                    continue

                item_id = child.child_value("id")
                item_type = child.child_value("type")
                param = child.child_value("param")

                if game_config.get_bool("force_unlock_cards") and item_type == self.GAME_CATALOG_TYPE_APPEAL_CARD:
                    # Don't save back appeal cards because they were force unlocked
                    continue
                if game_config.get_bool("force_unlock_songs") and item_type == self.GAME_CATALOG_TYPE_SONG:
                    # Don't save back songs, because they were force unlocked
                    continue
                if game_config.get_bool("force_unlock_crew") and item_type == self.GAME_CATALOG_TYPE_CREW:
                    # Don't save back crew, because they were force unlocked
                    continue

                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    item_id,
                    f"item_{item_type}",
                    {
                        "param": param,
                    },
                )

        # Update params
        if request.child("param") is not None:
            for child in request.child("param").children:
                if child.name != "info":
                    continue

                param_id = child.child_value("id")
                param_type = child.child_value("type")
                param_param = child.child_value("param")
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    param_id,
                    f"param_{param_type}",
                    {
                        "param": param_param,
                    },
                )

        # Grab last information and player options.
        lastdict = newprofile.get_dict("last")
        lastdict.replace_int("music_id", request.child_value("music_id"))
        lastdict.replace_int("music_type", request.child_value("music_type"))
        lastdict.replace_int("sort_type", request.child_value("sort_type"))
        lastdict.replace_int("narrow_down", request.child_value("narrow_down"))
        lastdict.replace_int("headphone", request.child_value("headphone"))
        lastdict.replace_int("gauge_option", request.child_value("gauge_option"))
        lastdict.replace_int("ars_option", request.child_value("ars_option"))
        lastdict.replace_int("notes_option", request.child_value("notes_option"))
        lastdict.replace_int("early_late_disp", request.child_value("early_late_disp"))
        lastdict.replace_int("eff_c_left", request.child_value("eff_c_left"))
        lastdict.replace_int("eff_c_right", request.child_value("eff_c_right"))
        lastdict.replace_int("lanespeed", request.child_value("lanespeed"))
        lastdict.replace_int("hispeed", request.child_value("hispeed"))
        lastdict.replace_int("draw_adjust", request.child_value("draw_adjust"))

        # Save back last information gleaned from results
        newprofile.replace_dict("last", lastdict)

        # Keep track of play statistics
        self.update_play_statistics(userid)

        return newprofile
