from typing import Dict, List, Optional, Set

from bemani.backend.base import Status
from bemani.backend.jubeat.base import JubeatBase
from bemani.backend.jubeat.common import JubeatGametopGetMeetingHandler, JubeatGamendRegisterHandler
from bemani.backend.jubeat.ripplesappend import JubeatRipplesAppend
from bemani.common import Profile, ValidatedDict, VersionConstants, Time
from bemani.data import Score, UserID
from bemani.protocol import Node


class JubeatKnit(
    JubeatGametopGetMeetingHandler,
    JubeatGamendRegisterHandler,
    JubeatBase
):
    name: str = "Jubeat Knit"
    version: int = VersionConstants.JUBEAT_KNIT

    extra_services: List[str] = [
        "netlog",
    ]

    def previous_version(self) -> Optional[JubeatBase]:
        return JubeatRipplesAppend(self.data, self.config, self.model)
    
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

    def handle_demodata_get_news_request(self, request: Node) -> Node:
        root = Node.void("demodata")
        data = Node.void("data")
        root.add_child(data)
        
        officialnews = Node.void("officialnews")
        data.add_child(officialnews)
        officialnews.set_attribute("count", "0")

        return root
    
    def handle_demodata_get_hitchart_request(self, request: Node) -> Node:
        root = Node.void("demodata")
        data = Node.void("data")
        root.add_child(data)
        
        hitchart = Node.void("hitchart")
        data.add_child(hitchart)
        hitchart.set_attribute("count", "0")
        hitchart.add_child(Node.string("update", ""))

        hitchart = Node.void("hitchart_lic")
        data.add_child(hitchart)
        hitchart.set_attribute("count", "0")

        hitchart = Node.void("hitchart_org")
        data.add_child(hitchart)
        hitchart.set_attribute("count", "0")
        
        return root
    
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
    
    def handle_netlog_send_request(self, request: Node) -> Node:
        return Node.void("netlog")
    
    def handle_gametop_regist_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/pass/refid")
        name = request.child_value("data/player/name")
        root = self.new_profile_by_refid(refid, name)
        return root
    
    def handle_gametop_get_pdata_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/pass/refid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("gametop")
            root.set_attribute("status", str(Status.NO_PROFILE))
        return root
    
    def handle_gametop_get_mdata_request(self, request: Node) -> Node:
        extid = request.child_value("data/player/jid")
        mdata_ver = request.child_value("data/player/mdata_ver")
        root = self.get_scores_by_extid(extid, mdata_ver, 3)
        if root is None:
            root = Node.void("gametop")
            root.set_attribute("status", str(Status.NO_PROFILE))
        return root
    
    def handle_gameend_log_request(self, request: Node) -> Node:
        # Record guest play later
        return Node.void("gameend")
    
    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("gametop")
        data = Node.void("data")
        root.add_child(data)

        achievements = self.data.local.user.get_achievements(self.game, self.version, userid)
        owned_secrets: Set[int] = set()
        owned_markers: Set[int] = set()
        owned_titles: Set[int] = set()
        for achievement in achievements:
            if achievement.type == "secret":
                owned_secrets.add(achievement.id)
            elif achievement.type == "marker":
                owned_markers.add(achievement.id)
            elif achievement.type == "title":
                owned_titles.add(achievement.id)

        player = Node.void("player")
        data.add_child(player)

        player.add_child(Node.s32("session_id", 1))
        player.add_child(Node.s32("jid", profile.extid))
        player.add_child(Node.string("name", profile.get_str("name", "PLAYER")))
        player.add_child(Node.string("refid", profile.refid))


        info = Node.void("info")
        player.add_child(info)
        info.add_child(
            Node.bool(
                "inherit",
                profile.get_bool("has_old_version") and not profile.get_bool("saved"),
            )
        )
        info.add_child(Node.s16("jubility", profile.get_int("jubility")))
        info.add_child(Node.s16("jubility_yday", profile.get_int("jubility_yday")))
        info.add_child(Node.s8("acv_prog", profile.get_int("acv_prog")))
        info.add_child(Node.s8("acv_wool", profile.get_int("acv_wool")))
        info.add_child(Node.s8_array("acv_route_prog", profile.get_int_array("acv_route_prog", 4, [0, 0, 0, 0])))
        info.add_child(Node.s32("acv_point", profile.get_int("acv_point")))
        info.add_child(Node.s32("tune_cnt", profile.get_int("tune_cnt")))
        info.add_child(Node.s32("save_cnt", profile.get_int("save_cnt")))
        info.add_child(Node.s32("saved_cnt", profile.get_int("saved_cnt")))
        info.add_child(Node.s32("fc_cnt", profile.get_int("fc_cnt")))
        info.add_child(Node.s32("ex_cnt", profile.get_int("ex_cnt")))
        info.add_child(Node.s32("match_cnt", profile.get_int("match_cnt")))
        info.add_child(Node.s32("beat_cnt", profile.get_int("beat_cnt")))
        info.add_child(Node.s32("mynews_cnt", profile.get_int("mynews_cnt")))
        info.add_child(Node.s32("con_sel_cnt", profile.get_int("con_sel_cnt")))
        info.add_child(Node.s32("tag_cnt", profile.get_int("tag_cnt")))
        info.add_child(Node.s32("mtg_entry_cnt", profile.get_int("mtg_entry_cnt")))
        info.add_child(Node.s32("tag_entry_cnt", profile.get_int("tag_entry_cnt")))
        info.add_child(Node.s32("mtg_hold_cnt", profile.get_int("mtg_hold_cnt")))
        info.add_child(Node.s32("tag_hold_cnt", profile.get_int("tag_hold_cnt")))
        info.add_child(Node.u8("mtg_result", profile.get_int("mtg_result")))

        lastdict = profile.get_dict("last")
        last = Node.void("last")
        player.add_child(last)
        last.add_child(Node.s64("play_time", lastdict.get_int("play_time")))
        last.add_child(Node.string("shopname", lastdict.get_str("shopname")))
        last.add_child(Node.string("areaname", lastdict.get_str("areaname")))
        last.add_child(Node.s16("title", lastdict.get_int("title")))
        last.add_child(Node.s8("theme", lastdict.get_int("theme")))
        last.add_child(Node.s8("marker", lastdict.get_int("marker")))
        last.add_child(Node.s8("rank_sort", lastdict.get_int("rank_sort")))
        last.add_child(Node.s8("combo_disp", lastdict.get_int("combo_disp")))
        last.add_child(Node.s32("music_id", lastdict.get_int("music_id")))
        last.add_child(Node.s8("seq_id", lastdict.get_int("seq_id")))
        last.add_child(Node.s8("sort", lastdict.get_int("sort")))
        last.add_child(Node.s32("filter", lastdict.get_int("filter")))
        last.add_child(Node.s8("msel_stat", lastdict.get_int("msel_stat")))
        last.add_child(Node.s8("con_suggest_id", lastdict.get_int("con_suggest_id")))

        item = Node.void("item")
        player.add_child(item)
        item.add_child(Node.s32_array("secret_list", self.create_owned_items(owned_secrets, 2)))
        item.add_child(Node.s16("theme_list", profile.get_int("theme_list")))
        item.add_child(Node.s32_array("marker_list", self.create_owned_items(owned_markers, 2)))
        item.add_child(Node.s32_array("title_list", self.create_owned_items(owned_titles, 24)))
        new = Node.void("new")
        item.add_child(new)
        new.add_child(Node.s32_array("secret_list", profile.get_int_array("secret_new", 2, [0, 0])))
        new.add_child(Node.s16("theme_list", profile.get_int("theme_new")))
        new.add_child(Node.s32_array("marker_list", profile.get_int_array("marker_new", 2, [0, 0])))
        new.add_child(Node.s32_array("title_list", profile.get_int_array("title_new", 24, [0] * 24)))

        today_music = Node.void("today_music")
        player.add_child(today_music)
        today_music.add_child(Node.s32("music_id", -1))

        lucky_music = Node.void("lucky_music")
        player.add_child(lucky_music)
        lucky_music.add_child(Node.s32("music_id", -1))

        news = Node.void("news")
        player.add_child(news)
        news.add_child(Node.s16("checked", profile.get_int("news_checked")))

        friendlist = Node.void("friendlist")
        player.add_child(friendlist)
        friendlist.set_attribute("count", "0")

        mylist = Node.void("mylist")
        player.add_child(mylist)
        mylist.set_attribute("count", "0")

        group = Node.void("group")
        player.add_child(group)
        group.add_child(Node.s32("group_id", -1))

        bingo = Node.void("bingo")
        player.add_child(bingo)
        reward = Node.void("reward")
        bingo.add_child(reward)
        reward.add_child(Node.s32("total", profile.get_int("jubingo_total")))
        reward.add_child(Node.s32("point",  profile.get_int("jubingo_point")))

        collabo = Node.void("collabo")
        player.add_child(collabo)
        collabo.add_child(Node.bool("success", profile.get_bool("collabo_success")))
        collabo.add_child(Node.bool("completed", profile.get_bool("collabo_completed")))

        history = Node.void("history")
        data.add_child(history)

        play_hist = Node.void("play_hist")
        history.add_child(play_hist)
        play_hist.set_attribute("count", "0")

        match_hist = Node.void("match_hist")
        history.add_child(match_hist)
        match_hist.set_attribute("count", "0")

        return root
    
    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        newprofile.replace_bool("saved", True)
        data = request.child("data")

        player = data.child("player")

        last = newprofile.get_dict("last")
        last.replace_int("play_time", Time.now())
        last.replace_str("shopname", player.child_value("shopname"))
        last.replace_str("areaname", player.child_value("areaname"))

        info = player.child("info")
        if info is not None:
            newprofile.replace_int("jubility", info.child_value("jubility"))
            newprofile.replace_int("jubility_yday", info.child_value("jubility_yday"))
            newprofile.replace_int("acv_prog", info.child_value("acv_prog"))
            newprofile.replace_int("acv_point", info.child_value("acv_point"))
            newprofile.replace_int("acv_wool", info.child_value("acv_wool"))
            newprofile.replace_int_array("acv_route_prog", 4, info.child_value("acv_route_prog"))
            newprofile.replace_int("tune_cnt", info.child_value("tune_cnt"))
            newprofile.replace_int("save_cnt", info.child_value("save_cnt"))
            newprofile.replace_int("saved_cnt", info.child_value("saved_cnt"))
            newprofile.replace_int("fc_cnt", info.child_value("fc_cnt"))
            newprofile.replace_int("fc_seq_cnt", info.child_value("fc_seq_cnt"))
            newprofile.replace_int("ex_cnt", info.child_value("exc_cnt"))
            newprofile.replace_int("ex_seq_cnt", info.child_value("exc_seq_cnt"))
            newprofile.replace_int("match_cnt", info.child_value("match_cnt"))
            newprofile.replace_int("beat_cnt", info.child_value("beat_cnt"))
            newprofile.replace_int("con_sel_cnt", info.child_value("con_sel_cnt"))
            newprofile.replace_int("tag_cnt", info.child_value("tag_cnt"))
            last.replace_int("con_suggest_id", info.child_value("con_suggest_id"))
            newprofile.replace_int("mynews_cnt", info.child_value("mynews_cnt"))

        item = player.child("item")
        if item is not None:
            newprofile.replace_int("theme_list", item.child_value("theme_list"))
            newprofile.replace_int_array("secret_new", 2, item.child_value("secret_new"))
            newprofile.replace_int("theme_new", item.child_value("theme_new"))
            newprofile.replace_int_array("marker_new", 2, item.child_value("marker_new"))
            newprofile.replace_int_array("title_new", 24, item.child_value("title_new"))

            owned_secrets = self.calculate_owned_items(item.child_value("secret_list"))
            owned_markers = self.calculate_owned_items(item.child_value("marker_list"))
            owned_titles = self.calculate_owned_items(item.child_value("title_list"))

            for index in owned_secrets:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    index,
                    "secret",
                    {}
                )

            for index in owned_markers:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    index,
                    "marker",
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

        news = player.child("news")
        if news is not None:
            newprofile.replace_int("news_checked", news.child_value("checked"))

        group = player.child("group")
        if group is not None:
            newprofile.replace_int("group_id", group.child_value("group_id"))

        collabo = player.child("collabo")
        if collabo is not None:
            newprofile.replace_bool("collabo_success", collabo.child_value("success"))
            newprofile.replace_bool("collabo_completed", collabo.child_value("completed"))

        jubingo = player.child("jubingo")
        if jubingo is not None:
            newprofile.replace_int("jubingo_total", jubingo.child_value("total"))
            newprofile.replace_int("jubingo_point", jubingo.child_value("point"))

        timestamps: Dict[int, int] = {}
        history = player.child("history")
        if history is not None:
            for tune in history.children:
                if tune.name != "tune":
                    continue
                entry = tune.child_value("log_id")
                ts = int(tune.child_value("timestamp") / 1000)
                timestamps[entry] = ts

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
                last.replace_int("msel_stat", tune.child_value("msel_stat"))

                songid = tune.child_value("music")
                entry = int(tune.attribute("id"))
                timestamp = timestamps.get(entry, Time.now())
                chart = int(result.child("score").attribute("seq"))
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
        root = Node.void("gametop")
        data = Node.void("data")
        root.add_child(data)
        player = Node.void("player")
        data.add_child(player)

        playdata = Node.void("playdata")
        player.add_child(playdata)
        playdata.set_attribute("count", str(len(scores)))

        music = ValidatedDict()
        for score in scores:
            if score.chart not in {
                self.CHART_TYPE_BASIC,
                self.CHART_TYPE_ADVANCED,
                self.CHART_TYPE_EXTREME,
            }:
                continue

            data = music.get_dict(str(score.id))
            play_cnt = data.get_int_array("play_cnt", 3)
            clear_cnt = data.get_int_array("clear_cnt", 3)
            clear_flags = data.get_int_array("clear_flags", 3)
            fc_cnt = data.get_int_array("fc_cnt", 3)
            ex_cnt = data.get_int_array("ex_cnt", 3)
            points = data.get_int_array("points", 3)

            play_cnt[score.chart] = score.plays
            clear_cnt[score.chart] = score.data.get_int("clear_count")
            fc_cnt[score.chart] = score.data.get_int("full_combo_count")
            ex_cnt[score.chart] = score.data.get_int("excellent_count")
            points[score.chart] = score.points

            clear_flags[score.chart] = self.GAME_FLAG_BIT_PLAYED
            if score.data.get_int("clear_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_CLEARED
            if score.data.get_int("full_combo_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_FULL_COMBO
            if score.data.get_int("excellent_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_EXCELLENT

            data.replace_int_array("play_cnt", 3, play_cnt)
            data.replace_int_array("clear_cnt", 3, clear_cnt)
            data.replace_int_array("clear_flags", 3, clear_flags)
            data.replace_int_array("fc_cnt", 3, fc_cnt)
            data.replace_int_array("ex_cnt", 3, ex_cnt)
            data.replace_int_array("points", 3, points)

            ghost = data.get("ghost", [None, None, None])
            ghost[score.chart] = score.data.get("ghost")
            data["ghost"] = ghost

            music.replace_dict(str(score.id), data)

        for scoreid in music:
            scoredata = music[scoreid]
            musicdata = Node.void("musicdata")
            playdata.add_child(musicdata)
            musicdata.set_attribute("music_id", scoreid)
            musicdata.add_child(Node.s32_array("play_cnt", scoredata.get_int_array("play_cnt", 3)))
            musicdata.add_child(Node.s32_array("clear_cnt", scoredata.get_int_array("clear_cnt", 3)))
            musicdata.add_child(Node.s32_array("fc_cnt", scoredata.get_int_array("fc_cnt", 3)))
            musicdata.add_child(Node.s32_array("ex_cnt", scoredata.get_int_array("ex_cnt", 3)))
            musicdata.add_child(Node.s8_array("clear", scoredata.get_int_array("clear_flags", 3)))
            musicdata.add_child(Node.s32_array("score", scoredata.get_int_array("points", 3)))

            ghosts = scoredata.get("ghost", [None, None, None])
            for i in range(len(ghosts)):
                ghost = ghosts[i]
                if ghost is None:
                    continue

                bar = Node.u8_array("bar", ghost)
                musicdata.add_child(bar)
                bar.set_attribute("seq", str(i))

        return root
