from typing import Dict, List, Optional, Set

from bemani.backend.base import Status
from bemani.backend.jubeat.base import JubeatBase
from bemani.backend.jubeat.common import JubeatGamendRegisterHandler
from bemani.backend.jubeat.stubs import Jubeat
from bemani.common import Profile, ValidatedDict, VersionConstants, Time
from bemani.data import Score, UserID
from bemani.protocol import Node


class JubeatRipples(JubeatGamendRegisterHandler, JubeatBase):
    name: str = "Jubeat Ripples"
    version: int = VersionConstants.JUBEAT_RIPPLES

    def previous_version(self) -> Optional[JubeatBase]:
        return Jubeat(self.data, self.config, self.model)
    
    def handle_shopinfo_regist_request(self, request: Node) -> Node:
        testmode = request.child("testmode")
        is_send = None
        if testmode is not None and testmode.attribute("is_send") is not None:
            is_send = testmode.attribute("is_send")

        # Update the name of this cab for admin purposes
        self.update_machine_name(request.child_value("shop_name"))

        shopinfo = Node.void("shopinfo")

        data = Node.void("data")
        shopinfo.add_child(data)
        data.add_child(Node.u32("cabid", 1))
        data.add_child(Node.string("locationid", request.child_value("shop/locationid") or "nowhere"))
        data.add_child(Node.u8("is_send", int(is_send) if is_send is not None else 0))

        return shopinfo

    def handle_lobby_check_request(self, request: Node) -> Node:
        root = Node.void("lobby")
        data = Node.void("data")
        root.add_child(data)

        entrant_nr = Node.u32("entrant_nr", 0)
        entrant_nr.set_attribute("time", "0")
        data.add_child(entrant_nr)
        data.add_child(Node.s16("interval", 0))
        data.add_child(Node.s16("entry_timeout", 30))

        waitlist = Node.void("waitlist")
        data.add_child(waitlist)
        waitlist.set_attribute("count", "0")

        return root

    def handle_lobby_entry_request(self, request: Node) -> Node:
        music_id = request.child_value("data/music/id")
        music_seq = request.child_value("data/music/seq")

        root = Node.void("lobby")
        data = Node.void("data")
        root.add_child(data)

        roomid = Node.s64("roomid", 1)
        roomid.set_attribute("master", "1")
        data.add_child(roomid)
        data.add_child(Node.s16("refresh_intr", 5))

        music = Node.void("music")
        data.add_child(music)
        music.add_child(Node.u32("id", music_id))
        music.add_child(Node.u8("seq", music_seq))

        return root

    def handle_lobby_refresh_request(self, request: Node) -> Node:
        root = Node.void("lobby")
        data = Node.void("data")
        root.add_child(data)
        data.add_child(Node.s16("refresh_intr", 5))
        return root

    def handle_lobby_report_request(self, request: Node) -> Node:
        root = Node.void("lobby")
        data = Node.void("data")
        root.add_child(data)
        data.add_child(Node.s16("refresh_intr", 5))
        return root
    
    def handle_gametop_regist_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/pass/refid")
        name = request.child_value("data/player/name")
        root = self.new_profile_by_refid(refid, name)
        return root
    
    def handle_gametop_get_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/pass/refid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("gametop")
            root.set_attribute("status", str(Status.NO_PROFILE))
        return root

    def handle_meeting_get_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/refid")
        root = Node.void("meeting")
        data = Node.void("data")
        root.add_child(data)

        entryinfo = Node.void("entryinfo")
        data.add_child(entryinfo)
        entryinfo.set_attribute("count", "0")

        reward = Node.void("reward")
        data.add_child(reward)
        reward.add_child(Node.s32("total", 0))
        reward.add_child(Node.s32("point", 0))

        return root
    
    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("gametop")
        data = Node.void("data")
        root.add_child(data)

        achievements = self.data.local.user.get_achievements(self.game, self.version, userid)
        owned_secrets: Set[int] = set()
        owned_titles: Set[int] = set()
        for achievement in achievements:
            if achievement.type == "secret":
                owned_secrets.add(achievement.id)
            elif achievement.type == "title":
                owned_titles.add(achievement.id)

        player = Node.void("player")
        data.add_child(player)

        player.add_child(Node.u32("session_id", 1))
        player.add_child(Node.u32("jid", profile.extid))
        player.add_child(Node.string("name", profile.get_str("name", "PLAYER")))

        info = Node.void("info")
        player.add_child(info)
        info.add_child(
            Node.bool(
                "inherit",
                profile.get_bool("has_old_version") and not profile.get_bool("saved"),
            )
        )
        info.add_child(Node.s32("online_cnt", profile.get_int("online_cnt")))
        info.add_child(Node.s32("multi_cnt", profile.get_int("multi_cnt")))
        info.add_child(Node.s32("match_cnt", profile.get_int("match_cnt")))
        info.add_child(Node.s32("beat_cnt", profile.get_int("beat_cnt")))
        info.add_child(Node.s32("save_cnt", profile.get_int("save_cnt")))
        info.add_child(Node.s32("saved_cnt", profile.get_int("saved_cnt")))
        info.add_child(Node.u8("grade", profile.get_int("grade")))
        info.add_child(Node.s32("grade_point", profile.get_int("grade_point")))

        lastdict = profile.get_dict("last")
        last = Node.void("last")
        player.add_child(last)
        last.add_child(Node.u8("mode", lastdict.get_int("mode")))
        last.add_child(Node.u32("music_id", lastdict.get_int("music_id")))
        last.add_child(Node.u8("seq_id", lastdict.get_int("seq_id")))
        last.add_child(Node.u8("marker", lastdict.get_int("marker")))
        last.add_child(Node.s16("title", lastdict.get_int("title")))
        last.add_child(Node.u8("theme", lastdict.get_int("theme")))
        last.add_child(Node.u8("sort", lastdict.get_int("sort")))
        last.add_child(Node.u32("filter", lastdict.get_int("filter")))
        last.add_child(Node.u8("rank_sort", lastdict.get_int("rank_sort")))
        last.add_child(Node.u8("combo_disp", lastdict.get_int("combo_disp")))

        item = Node.void("item")
        player.add_child(item)
        item.add_child(Node.u32_array("secret_list", self.create_owned_items(owned_secrets, 2)))
        item.add_child(Node.u32("marker_list", profile.get_int("marker_list")))
        item.add_child(Node.u8("theme_list", profile.get_int("theme_list")))
        item.add_child(Node.u32_array("title_list", self.create_owned_items(owned_titles, 20)))
        new = Node.void("new")
        item.add_child(new)
        new.add_child(Node.u32_array("secret_list", profile.get_int_array("secret_new", 2, [0] * 2)))
        new.add_child(Node.u32("marker_list", profile.get_int("marker_new")))
        new.add_child(Node.u8("theme_list", profile.get_int("theme_new")))
        new.add_child(Node.u32_array("title_list", profile.get_int_array("title_new", 20, [0] * 20)))

        news = Node.void("news")
        player.add_child(news)
        news.add_child(Node.s16("checked", profile.get_int("news_checked")))

        mynews = Node.void("mynews")
        player.add_child(mynews)
        mynews.set_attribute("count", "0")

        friendnews = Node.void("friendnews")
        player.add_child(friendnews)
        friendnews.set_attribute("count", "0")

        friendlist = Node.void("friendlist")
        player.add_child(friendlist)
        friendlist.set_attribute("count", "0")

        sns = Node.void("sns")
        player.add_child(sns)
        sns.add_child(Node.u8("playlog", 0))

        today_music = Node.void("today_music")
        player.add_child(today_music)
        today_music.add_child(Node.u32("music_id", 0))
        today_music.add_child(Node.float("rate", 1.0))

        player.add_child(self.get_scores_by_extid(profile.extid, 1, 0))

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        newprofile.replace_bool("saved", True)
        data = request.child("data")

        player = data.child("player")

        last = newprofile.get_dict("last")
        last.replace_int("play_time", Time.now())
        last.replace_str("shopname", player.child_value("shop"))
        last.replace_str("areaname", player.child_value("pref"))

        newprofile.replace_int("grade", player.child_value("grade"))
        newprofile.replace_int("grade_point", player.child_value("grade_point"))
        newprofile.replace_int("news_checked", player.child_value("checked"))
        newprofile.replace_int("theme_list", player.child_value("theme_list"))
        newprofile.replace_int("marker_list", player.child_value("marker_list"))
        newprofile.replace_int_array("title_new", 20, player.child_value("title_new"))
        newprofile.replace_int("theme_new", player.child_value("theme_new"))
        newprofile.replace_int_array("secret_new", 2, player.child_value("secret_new"))
        newprofile.replace_int("marker_new", player.child_value("marker_new"))

        owned_secrets = self.calculate_owned_items(player.child_value("secret_list"))
        owned_titles = self.calculate_owned_items(player.child_value("title_list"))

        for index in owned_secrets:
            self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                index,
                "secret",
                {}
            )

        for index in owned_titles:
            self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                index,
                "title",
                {}
            )

        result = data.child("result")
        if result is not None:
            for tune in result.children:
                if tune.name != "tune":
                    continue
                result = tune.child("player")

                last.replace_int("marker", tune.child_value("marker"))
                last.replace_int("title", tune.child_value("title"))
                last.replace_int("theme", tune.child_value("theme"))
                last.replace_int("sort", tune.child_value("sort"))
                last.replace_int("filter", tune.child_value("filter"))
                last.replace_int("rank_sort", tune.child_value("rank_sort"))
                last.replace_int("combo_disp", tune.child_value("combo_disp"))

                songid = tune.child_value("music")
                entry = int(tune.attribute("id"))
                timestamp = Time.now()
                chart = int(tune.child("music").attribute("seq"))
                points = result.child_value("score")
                flags = int(result.child("score").attribute("clear"))
                combo = int(result.child("score").attribute("combo"))
                ghost = result.child_value("mbar")

                last.replace_int("music_id", songid)
                last.replace_int("seq_id", chart)

                mapping = {
                    self.GAME_FLAG_BIT_CLEARED: self.PLAY_MEDAL_CLEARED,
                    self.GAME_FLAG_BIT_FULL_COMBO: self.PLAY_MEDAL_FULL_COMBO,
                    self.GAME_FLAG_BIT_EXCELLENT: self.PLAY_MEDAL_EXCELLENT,
                    self.GAME_FLAG_BIT_NEARLY_FULL_COMBO: self.PLAY_MEDAL_NEARLY_FULL_COMBO,
                    self.GAME_FLAG_BIT_NEARLY_EXCELLENT: self.PLAY_MEDAL_NEARLY_EXCELLENT,
                }

                medal = self.PLAY_MEDAL_FAILED
                for bit in mapping:
                    if flags & bit > 0:
                        medal = max(medal, mapping[bit])

                self.update_score(userid, timestamp, songid, chart, points, medal, combo, ghost)

        newprofile.replace_dict("last", last)

        self.update_play_statistics(userid)

        return newprofile

    def format_scores(self, userid: UserID, profile: Profile, scores: List[Score]) -> Node:
        playdata = Node.void("playdata")

        music = ValidatedDict()
        for score in scores:
            if score.chart not in {
                self.CHART_TYPE_BASIC,
                self.CHART_TYPE_ADVANCED,
                self.CHART_TYPE_EXTREME,
            }:
                continue

            data = music.get_dict(str(score.id))
            points = data.get_int_array("points", 3)
            clear_flags = data.get_int_array("clear_flags", 3)

            points[score.chart] = score.points

            clear_flags[score.chart] = self.GAME_FLAG_BIT_PLAYED
            if score.data.get_int("clear_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_CLEARED
            if score.data.get_int("full_combo_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_FULL_COMBO
            if score.data.get_int("excellent_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_EXCELLENT

            data.replace_int_array("points", 3, points)
            data.replace_int_array("clear_flags", 3, clear_flags)

            ghost = data.get("ghost", [None, None, None])
            ghost[score.chart] = score.data.get("ghost")
            data["ghost"] = ghost

            music.replace_dict(str(score.id), data)

        for scoreid in music:
            scoredata = music[scoreid]
            musicdata = Node.void("musicdata")
            playdata.add_child(musicdata)
            musicdata.set_attribute("music_id", scoreid)
            musicdata.add_child(Node.s32_array("score", scoredata.get_int_array("points", 3)))
            musicdata.add_child(Node.u8_array("clear", scoredata.get_int_array("clear_flags", 3)))

            ghosts = scoredata.get("ghost", [None, None, None])
            for i in range(len(ghosts)):
                ghost = ghosts[i]
                if ghost is None:
                    continue

                bar = Node.u8_array("bar", ghost)
                musicdata.add_child(bar)
                bar.set_attribute("seq", str(i))

        return playdata
