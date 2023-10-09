from bemani.backend.beatstream.base import BeatstreamBase

from bemani.common import Profile, ValidatedDict, VersionConstants, ID, Time
from bemani.data import UserID
from bemani.protocol import Node

class Beatstream(BeatstreamBase):
    name: str = "Beatstream"
    version: int = VersionConstants.BEATSTREAM

    def handle_pcb_boot_request(self, request: Node) -> Node:
        shop_id = ID.parse_machine_id(request.child_value("lid"))
        machine = self.get_machine_by_id(shop_id)
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

        root = Node.void("pcb")
        sinfo = Node.void("sinfo")
        root.add_child(sinfo)
        sinfo.add_child(Node.string("nm", machine_name))
        sinfo.add_child(Node.bool("cl_enbl", close))
        sinfo.add_child(Node.u8("cl_h", hour))
        sinfo.add_child(Node.u8("cl_m", minute))

        return root
    
    def handle_shop_info_write_request(self, request: Node) -> Node:
        self.update_machine_name(request.child_value("sinfo/nm"))
        self.update_machine_data({
            "close": request.child_value("sinfo/cl_enbl"),
            "hour": request.child_value("sinfo/cl_h"),
            "minute": request.child_value("sinfo/cl_m"),
            "pref": request.child_value("sinfo/prf")
        })

        return Node.void("shop")
    
    def handle_info_common_request(self, request: Node) -> Node:
        root = Node.void("info")

        return root
    
    def handle_info_music_count_read_request(self, request: Node) -> Node:
        root = Node.void("info")
        record = Node.void("record")
        root.add_child(record)

        return root
    
    def handle_info_music_ranking_read_request(self, request: Node) -> Node:
        root = Node.void("info")
        ranking = Node.void("ranking")
        root.add_child(ranking)

        return root

    def handle_player_start_request(self, request: Node) -> Node:
        root = Node.void("player")

        refid = request.child_value("rid")
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            self.data.local.lobby.put_play_session_info(
                self.game,
                self.version,
                userid,
                {
                    "ga": request.child_value("ga"),
                    "gp": request.child_value("gp"),
                    "la": request.child_value("la"),
                },
            )
            info = self.data.local.lobby.get_play_session_info(
                self.game,
                self.version,
                userid,
            )
            if info is not None:
                play_id = info.get_int("id")
            else:
                play_id = 0
        else:
            play_id = 0

        root.add_child(Node.s32("plyid", play_id))
        root.add_child(Node.u64("start_time", Time.now() * 1000))

        return root
    
    def handle_player_end_request(self, request: Node) -> Node:
        refid = request.child_value("rid")
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            lobby = self.data.local.lobby.get_lobby(
                self.game,
                self.version,
                userid
            )
            if lobby is not None:
                self.data.local.lobby.destroy_lobby(lobby.get_int("id"))
            self.data.local.lobby.destroy_play_session_info(
                self.game,
                self.version,
                userid
            )

        return Node.void("player")
    
    def handle_player_read_request(self, request: Node) -> Node:
        refid = request.child_value("rid")
        profile = self.get_profile_by_refid(refid)
        if profile is None:
            return Node.void("player")
        
        return profile

    def handle_player_write_request(self, request: Node) -> Node:
        refid = request.child_value("pdata/account/rid")
        profile = self.put_profile_by_refid(refid, request)
        root = Node.void("player")

        if profile is None:
            root.add_child(Node.s32("uid", 0))
        else:
            root.add_child(Node.s32("uid", profile.extid))
        
        return root

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("player")
        pdata = Node.void("pdata")
        root.add_child(pdata)

        statistics = self.get_play_statistics(userid)
        game_config = self.get_game_config()
        achievements = self.data.local.user.get_achievements(
            self.game, self.version, userid
        )

        account = Node.void("account")
        pdata.add_child(account)
        account.add_child(Node.s32("usrid", profile.extid))
        account.add_child(Node.s32("tpc", statistics.total_plays))
        account.add_child(Node.s32("dpc", statistics.today_plays))
        account.add_child(Node.s32("crd", 1))
        account.add_child(Node.s32("brd", 1))
        account.add_child(Node.s32("tdc", statistics.total_days))
        account.add_child(Node.s32("intrvld", 0))
        account.add_child(Node.s16("ver", 0))
        account.add_child(Node.u64("pst", 0))
        account.add_child(Node.u64("st", Time.now() * 1000))
        account.add_child(Node.bool("ea", True))

        base = Node.void("base")
        pdata.add_child(base)
        base.add_child(Node.string("name", profile.get_str("name", "PLAYER")))
        base.add_child(Node.s8("brnk", profile.get_int("brnk")))
        base.add_child(Node.s8("bcnum", profile.get_int("bcnum")))
        base.add_child(Node.s8("lcnum", profile.get_int("lcnum")))
        base.add_child(Node.s32("volt", profile.get_int("volt")))
        base.add_child(Node.s32("gold", profile.get_int("gold")))
        base.add_child(Node.s32("lmid", profile.get_int("last_music_id")))
        base.add_child(Node.s8("lgrd", profile.get_int("last_chart")))
        base.add_child(Node.s8("lsrt", profile.get_int("last_sort")))
        base.add_child(Node.s8("ltab", profile.get_int("last_tab")))
        base.add_child(Node.s8("splv", profile.get_int("splv")))
        base.add_child(Node.s8("pref", profile.get_int("pref")))

        base2 = Node.void("base2")
        pdata.add_child(base2)
        base2.add_child(Node.s32("lcid", profile.get_int("lcid")))
        base2.add_child(Node.s32("hat", profile.get_int("hat", -1)))

        opened = Node.void("opened")
        pdata.add_child(opened)

        survey = Node.void("survey")
        pdata.add_child(survey)
        survey.add_child(Node.s8("motivate", profile.get_int("survey_motivate", -1)))

        itemnode = Node.void("item")
        pdata.add_child(item)
        for item in achievements:
            if item.type[:5] != "item_":
                continue
            itemtype = int(item.type[5:])
            if game_config.get_bool("force_unlock_songs") and itemtype == 0:
                continue

            info = Node.void("info")
            itemnode.add_child(info)
            info.add_child(Node.u8("type", itemtype))
            info.add_child(Node.u16("id", item.id))
            info.add_child(Node.u16("param", item.data.get_int("param")))
            info.add_child(Node.u16("count", item.data.get_int("count")))

        customize = Node.void("customize")
        pdata.add_child(customize)
        customize.add_child(Node.u8_array("custom", profile.get_int_array("customize", 16, [0] * 16)))

        hacker = Node.void("hacker")
        pdata.add_child(hacker)

        bisco = Node.void("bisco")
        pdata.add_child(bisco)
        pinfo = Node.void("pinfo")
        bisco.add_child(pinfo)
        pinfo.add_child(Node.s32("bnum", 0))
        pinfo.add_child(Node.s32("jbox", 0))
        minfo = Node.void("minfo")
        bisco.add_child(minfo)
        minfo.add_child(Node.s32("mid", 0))
        minfo.add_child(Node.s64("cbit", 0))
        minfo.add_child(Node.bool("clr", 0))
        minfo.add_child(Node.s32("stime", 0))
        minfo.add_child(Node.s16("c_0", 0))
        minfo.add_child(Node.s16("c_1", 0))
        minfo.add_child(Node.s16("c_2", 0))
        minfo.add_child(Node.s16("c_3", 0))
        minfo.add_child(Node.s16("c_4", 0))
        minfo.add_child(Node.s16("c_5", 0))
        minfo.add_child(Node.s16("c_6", 0))
        minfo.add_child(Node.s16("c_7", 0))
        minfo.add_child(Node.s16("c_8", 0))
        minfo.add_child(Node.s16("c_9", 0))
        minfo.add_child(Node.s16("c_10", 0))
        minfo.add_child(Node.s16("c_11", 0))
        minfo.add_child(Node.s16("c_12", 0))
        minfo.add_child(Node.s16("c_13", 0))
        minfo.add_child(Node.s16("c_14", 0))
        minfo.add_child(Node.s16("c_15", 0))
        minfo.add_child(Node.s16("c_16", 0))
        minfo.add_child(Node.s16("c_17", 0))
        minfo.add_child(Node.s16("c_18", 0))
        minfo.add_child(Node.s16("c_19", 0))
        minfo.add_child(Node.s16("p_0", 0))
        minfo.add_child(Node.s16("p_1", 0))
        minfo.add_child(Node.s16("p_2", 0))
        minfo.add_child(Node.s16("p_3", 0))
        minfo.add_child(Node.s16("p_4", 0))
        minfo.add_child(Node.s16("p_5", 0))
        minfo.add_child(Node.s16("p_6", 0))
        minfo.add_child(Node.s16("p_7", 0))
        minfo.add_child(Node.s16("p_8", 0))
        minfo.add_child(Node.s16("p_9", 0))
        minfo.add_child(Node.s16("p_10", 0))
        minfo.add_child(Node.s16("p_11", 0))
        minfo.add_child(Node.s16("p_12", 0))
        minfo.add_child(Node.s16("p_13", 0))
        minfo.add_child(Node.s16("p_14", 0))
        minfo.add_child(Node.s16("p_15", 0))
        minfo.add_child(Node.s16("p_16", 0))
        minfo.add_child(Node.s16("p_17", 0))
        minfo.add_child(Node.s16("p_18", 0))
        minfo.add_child(Node.s16("p_19", 0))

        record = Node.void("record")
        pdata.add_child(record)

        course = Node.void("course")
        pdata.add_child(course)

        return root

    def unformat_profile(
        self, userid: UserID, request: Node, oldprofile: Profile
    ) -> Profile:
        game_config = self.get_game_config()
        newprofile = oldprofile.clone()

        base = request.child("pdata/base")
        newprofile.replace_str("name", base.child_value("name"))
        newprofile.replace_int("brnk", base.child_value("brnk"))
        newprofile.replace_int("bcnum", base.child_value("bcnum"))
        newprofile.replace_int("lcnum", base.child_value("lcnum"))
        newprofile.replace_int("volt", base.child_value("volt"))
        newprofile.replace_int("gold", base.child_value("gold"))
        newprofile.replace_int("last_music_id", base.child_value("lmid"))
        newprofile.replace_int("last_chart", base.child_value("lgrd"))
        newprofile.replace_int("last_sort", base.child_value("lsrt"))
        newprofile.replace_int("last_tab", base.child_value("ltab"))
        newprofile.replace_int("splv", base.child_value("splv"))
        newprofile.replace_int("pref", base.child_value("pref"))

        base2 = request.child("pdata/base2")
        newprofile.replace_int("lcid", base2.child_value("lcid"))
        newprofile.replace_int("hat", base2.child_value("hat"))

        survey = request.child("pdata/survey")
        newprofile.replace_int("survey_motivate", survey.child_value("motivate"))

        item = request.child("pdata/item")
        if item:
            for child in item.children:
                if child.name != "info":
                    continue

                item_type = child.child_value("type")
                item_id = child.child_value("id")
                param = child.child_value("param")
                count = child.child_value("count")
                if game_config.get_bool("force_unlock_songs") and item_type == 0:
                    continue

                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    item_id,
                    f"item_{item_type}",
                    {
                        "param": param,
                        "count": count,
                    }
                )

        customize = request.child("pdata/customize")
        if customize:
            newprofile.replace_int_array("customize", 16, customize.child_value("custom"))

        self.update_play_statistics(userid)

        return newprofile
