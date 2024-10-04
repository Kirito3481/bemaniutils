# vim: set fileencoding=utf-8
import random
from typing import Any, Dict, List, Optional, Set, Tuple
from typing_extensions import Final

from bemani.backend.jubeat.base import JubeatBase
from bemani.backend.jubeat.common import (
    JubeatDemodataGetHitchartHandler,
    JubeatDemodataGetNewsHandler,
    JubeatGamendRegisterHandler,
    JubeatGametopGetMeetingHandler,
    JubeatLobbyCheckHandler,
    JubeatLoggerReportHandler,
)
from bemani.backend.jubeat.qubell import JubeatQubell

from bemani.backend.base import Status
from bemani.common import Time, Profile, ValidatedDict, VersionConstants
from bemani.data import Data, Achievement, Score, Song, UserID
from bemani.protocol import Node


class JubeatClan(
    JubeatDemodataGetHitchartHandler,
    JubeatDemodataGetNewsHandler,
    JubeatGamendRegisterHandler,
    JubeatGametopGetMeetingHandler,
    JubeatLobbyCheckHandler,
    JubeatLoggerReportHandler,
    JubeatBase,
):
    name: str = "Jubeat Clan"
    version: int = VersionConstants.JUBEAT_CLAN

    JBOX_EMBLEM_NORMAL: Final[int] = 1
    JBOX_EMBLEM_PREMIUM: Final[int] = 2

    EVENT_STATUS_OPEN: Final[int] = 0x1
    EVENT_STATUS_COMPLETE: Final[int] = 0x2

    EVENTS: Dict[int, Dict[str, bool]] = {
        5: {
            "enabled": False,
        },
        6: {
            "enabled": False,
        },
        15: {
            "enabled": True,
        },
        22: {
            "enabled": False,
        },
        23: {
            "enabled": False,
        },
        34: {
            "enabled": False,
        },
    }

    FIVE_PLAYS_UNLOCK_EVENT_SONG_IDS: Set[int] = set(range(80000301, 80000348))

    COURSE_STATUS_SEEN: Final[int] = 0x01
    COURSE_STATUS_PLAYED: Final[int] = 0x02
    COURSE_STATUS_CLEARED: Final[int] = 0x04

    COURSE_TYPE_PERMANENT: Final[int] = 1
    COURSE_TYPE_TIME_BASED: Final[int] = 2

    COURSE_CLEAR_SCORE: Final[int] = 1
    COURSE_CLEAR_COMBINED_SCORE: Final[int] = 2
    COURSE_CLEAR_HAZARD: Final[int] = 3

    COURSE_HAZARD_EXC1: Final[int] = 1
    COURSE_HAZARD_EXC2: Final[int] = 2
    COURSE_HAZARD_EXC3: Final[int] = 3
    COURSE_HAZARD_FC1: Final[int] = 4
    COURSE_HAZARD_FC2: Final[int] = 5
    COURSE_HAZARD_FC3: Final[int] = 6

    DROP_RAINBOW: Final[int] = 1
    DROP_RED: Final[int] = 2
    DROP_CYAN: Final[int] = 3
    DROP_GREEN: Final[int] = 4
    DROP_PLUM: Final[int] = 5

    DROP_GRADE_NORMAL: Final[int] = 1
    DROP_GRADE_SILVER: Final[int] = 2
    DROP_GRADE_GOLD: Final[int] = 3
    DROP_GRADE_RAINBOW: Final[int] = 4

    REWARD_MUSIC: Final[int] = 1
    REWARD_TITLE: Final[int] = 2
    REWARD_MARKER: Final[int] = 3
    REWARD_BACKGROUND: Final[int] = 4
    REWARD_JUBIBELL: Final[int] = 5
    REWARD_OMIYAGE: Final[int] = 6
    REWARD_OMIYAGE_LEVEL: Final[int] = 7
    REWARD_ETC: Final[int] = 8
    REWARD_JBOX_PIECE: Final[int] = 9
    REWARD_OMIYAGE_SET: Final[int] = 10
    REWARD_BONUS_TUNE_GAUGE: Final[int] = 11
    REWARD_TITLE_PARTS: Final[int] = 12

    # drop id  rainbow: 1, red: 2, cyan: 3, green: 4, purple: 5
    # drop grade  normal: 1, silver: 2, gold: 3, rainbow: 4

    # Reward Type 1 music
    # value: music id

    # Reward Type 2 title
    # value: title id

    # Reward Type 3 marker
    # value: marker id

    # Reward Type 4 background
    # value: background id

    # Reward Type 5 jubibell
    # value: bell id

    # Reward Type 6 OMIYAGE
    # value: 갯수 뒤에 두자리는 OMIYAGE 종류 그뒤 4자리는 OMIYAGE 등급
    # ex) 50040001 -> 50: 갯수, 04: OMIYAGE 종류, 0001: OMIYAGE 등급

    # Reward Type 7 OMIYAGE LEVEL
    # value: 갯수 뒤에 4자리는 모르겠음
    # ex) 2000001 -> 200: Exp, 0001: 모름

    # Reward Type 8 기타 아이템
    # value: 갯수 뒤에 4자리는 모르겠음
    # ex) 104 -> 1: Exp, 04: 모름

    # Reward Type 9 jbox piece
    # value: pieces

    # Reward Type 10 OMIYAGE SET
    # value: 갯수 뒤에 두자리는 OMIYAGE 등급 그뒤 4자리는 0으로 고정
    # ex) 50040000 -> 50: 갯수, 04: OMIYAGE 등급, 0000: 0000 고정

    # Reward Type 11 BONUS TUNE GAUGE
    # value: tens

    # Reward Type 12 title parts
    # value: parts id

    def previous_version(self) -> Optional[JubeatBase]:
        return JubeatQubell(self.data, self.config, self.model)

    @classmethod
    def run_scheduled_work(cls, data: Data, config: Dict[str, Any]) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Insert daily FC challenges into the DB.
        """
        events = []
        if data.local.network.should_schedule(cls.game, cls.version, "fc_challenge", "daily"):
            # Generate a new list of two FC challenge songs. Skip a particular song range since these are all a single song ID.
            # Jubeat Clan has an unlock event where you have to play different charts for the same song, and the charts are
            # loaded in based on the cabinet's prefecture. So, no matter where you are, you will only see one song within this
            # range, but it will be a different ID depending on the prefecture set in settings. This means its not safe to send
            # these song IDs, so we explicitly exclude them.
            start_time, end_time = data.local.network.get_schedule_duration("daily")
            all_songs = list(
                set(
                    song.id
                    for song in data.local.music.get_all_songs(cls.game, cls.version)
                    if song.id not in cls.FIVE_PLAYS_UNLOCK_EVENT_SONG_IDS
                )
            )
            if len(all_songs) >= 2:
                daily_songs = random.sample(all_songs, 2)
                data.local.game.put_time_sensitive_settings(
                    cls.game,
                    cls.version,
                    "fc_challenge",
                    {
                        "start_time": start_time,
                        "end_time": end_time,
                        "today": daily_songs[0],
                        "whim": daily_songs[1],
                    },
                )
                events.append(
                    (
                        "jubeat_fc_challenge_charts",
                        {
                            "version": cls.version,
                            "today": daily_songs[0],
                            "whim": daily_songs[1],
                        },
                    )
                )

                # Mark that we did some actual work here.
                data.local.network.mark_scheduled(cls.game, cls.version, "fc_challenge", "daily")
        return events

    @classmethod
    def get_settings(cls) -> Dict[str, Any]:
        """
        Return all of our front-end modifiably settings.
        """
        return {
            "bools": [
                {
                    "name": "Force Unlock All Songs",
                    "tip": "Forces all songs to be available by default",
                    "category": "game_config",
                    "setting": "force_song_unlock",
                },
            ],
            "ints": [
                {
                    "name": "Union Battle",
                    "tip": "jubeat clan street fight event",
                    "category": "game_config",
                    "setting": "union_battle",
                    "values": {
                        0: "No Event",
                        1: "1st",
                    },
                },
            ],
        }

    def __get_course_list(self) -> List[Dict[str, Any]]:
        return [
            # Papricapcap courses
            {
                "id": 1,
                "name": "Thank You Merry Christmas",
                "course_type": self.COURSE_TYPE_TIME_BASED,
                "end_time": Time.end_of_this_week() + Time.SECONDS_IN_WEEK,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 3,
                "score": 700000,
                "music": [
                    [(50000077, 0), (50000077, 1), (50000077, 2)],
                    [(80000080, 0), (80000080, 1), (80000080, 2)],
                    [(50000278, 0), (50000278, 1), (50000278, 2)],
                ],
            },
            {
                "id": 2,
                "name": "はじめての山道",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 1,
                "score": 700000,
                "music": [
                    [(20000002, 0), (20000022, 0), (30000108, 0)],
                    [(70000035, 0), (70000069, 0), (80000020, 0)],
                    [(50000116, 0), (50000120, 0), (50000383, 0)],
                ],
            },
            {
                "id": 3,
                "name": "NOBOLOT検定 第1の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 1,
                "score": 700000,
                "music": [
                    [(20000109, 0), (50000218, 0), (60000100, 0)],
                    [(50000228, 0), (70000125, 0)],
                    [(70000109, 0)],
                ],
            },
            {
                "id": 4,
                "name": "アニメハイキング",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 2,
                "score": 750000,
                "music": [
                    [(70000028, 0)],
                    [(70000030, 0)],
                    [(80001009, 0)],
                ],
            },
            {
                "id": 5,
                "name": "しりとり山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 3,
                "score": 750000,
                "music": [
                    [(10000068, 0), (50000089, 0), (60000078, 0)],
                    [(50000059, 0), (50000147, 0), (50000367, 0)],
                    [(50000202, 0), (70000144, 0), (70000156, 0)],
                ],
            },
            {
                "id": 6,
                "name": "NOBOLOT検定 第2の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 3,
                "score": 800000,
                "music": [
                    [(50000268, 0), (70000039, 0), (70000160, 0)],
                    [(60000080, 1), (80000014, 0)],
                    [(60000053, 0)],
                ],
            },
            # Harapenya-na courses
            {
                "id": 11,
                "name": "おためし！い~あみゅちゃん",
                "course_type": self.COURSE_TYPE_TIME_BASED,
                "end_time": Time.end_of_this_week() + Time.SECONDS_IN_WEEK,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 4,
                "score": 700000,
                "music": [
                    [(50000207, 0), (50000207, 1), (50000207, 2)],
                    [(50000111, 0), (50000111, 1), (50000111, 2)],
                    [(60000009, 0), (60000009, 1), (60000009, 2)],
                ],
            },
            {
                "id": 12,
                "name": "NOBOLOT検定 第3の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 4,
                "score": 850000,
                "music": [
                    [(40000110, 1), (70000059, 1), (70000131, 1)],
                    [(30000004, 1), (80000035, 1)],
                    [(40000051, 1)],
                ],
            },
            {
                "id": 13,
                "name": "頂上から見えるお月様",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 5,
                "score": 850000,
                "music": [
                    [(50000245, 1)],
                    [(60000051, 1)],
                    [(80001011, 1)],
                ],
            },
            {
                "id": 14,
                "name": "ヒッチハイクでGO!GO!",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 5,
                "score": 850000,
                "music": [
                    [(10000053, 1), (80000038, 1)],
                    [(30000123, 1), (50000086, 1), (70000119, 1)],
                    [(50000196, 1), (60000006, 1), (70000153, 1)],
                ],
            },
            {
                "id": 15,
                "name": "今日の一文字",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 6,
                "score": 2600000,
                "music": [
                    [(50000071, 1)],
                    [(40000053, 1)],
                    [(70000107, 1)],
                ],
            },
            {
                "id": 16,
                "name": "NOBOLOT検定 第4の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 6,
                "score": 2650000,
                "music": [
                    [(50000085, 2), (50000176, 2), (70000055, 2)],
                    [(50000157, 2), (60001008, 2)],
                    [(10000068, 2)],
                ],
            },
            # Tillhorn courses
            {
                "id": 21,
                "name": "ちくわの山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 7,
                "score": 870000,
                "music": [
                    [(70000099, 2)],
                    [(50000282, 2), (60000106, 2), (80000041, 2)],
                    [(50000234, 2)],
                ],
            },
            {
                "id": 22,
                "name": "NOBOLOT検定 第5の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 7,
                "score": 2650000,
                "music": [
                    [(50000233, 2), (50000242, 1), (80000032, 2)],
                    [(60000027, 2), (60000045, 2)],
                    [(20000038, 2)],
                ],
            },
            {
                "id": 23,
                "name": "初めてのHARD MODE",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "hard": True,
                "difficulty": 8,
                "score": 835000,
                "music": [
                    [(50000247, 2)],
                    [(70000071, 2)],
                    [(20000042, 2)],
                ],
            },
            {
                "id": 24,
                "name": "雪山の上のお姫様",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 8,
                "score": 2700000,
                "music": [
                    [(50000101, 2)],
                    [(50000119, 2), (50000174, 2), (60000009, 2)],
                    [(80001010, 2)],
                ],
            },
            {
                "id": 25,
                "name": "なが~い山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 9,
                "score": 2800000,
                "music": [
                    [(70000170, 2), (80000013, 2)],
                    [(70000161, 2), (80000057, 2)],
                    [(80000043, 2)],
                ],
            },
            {
                "id": 26,
                "name": "NOBOLOT検定 第6の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 9,
                "score": 2750000,
                "music": [
                    [(50000034, 2), (50000252, 2), (50000347, 2)],
                    [(70000117, 2), (70000138, 2)],
                    [(50000078, 2)],
                ],
            },
            # Bahaneroy courses
            {
                "id": 31,
                "name": "挑戦！い~あみゅちゃん",
                "course_type": self.COURSE_TYPE_TIME_BASED,
                "end_time": Time.end_of_this_week() + Time.SECONDS_IN_WEEK,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 12,
                "score": 2823829,
                "music": [
                    [(50000207, 2)],
                    [(50000111, 2)],
                    [(60001006, 2)],
                ],
            },
            {
                "id": 32,
                "name": "更なる高みを目指して",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "difficulty": 10,
                "score": 920000,
                "music": [
                    [(50000210, 2)],
                    [(50000122, 2)],
                    [(70000022, 2)],
                ],
            },
            {
                "id": 33,
                "name": "NOBOLOT検定 第7の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 10,
                "score": 2800000,
                "music": [
                    [(60000059, 2), (60000079, 2), (70000006, 2)],
                    [(50000060, 2), (50000127, 2)],
                    [(60000073, 2)],
                ],
            },
            {
                "id": 34,
                "name": "崖っぷち! スリーチャレンジ!",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_HAZARD,
                "hazard_type": self.COURSE_HAZARD_FC3,
                "difficulty": 11,
                "music": [
                    [(10000036, 2), (30000049, 2), (50000172, 2)],
                    [(30000044, 2), (40000044, 2), (60000028, 2)],
                    [(60000074, 2)],
                ],
            },
            {
                "id": 35,
                "name": "芽吹いて咲いて",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 11,
                "score": 2800000,
                "music": [
                    [(60001003, 2)],
                    [(70000097, 2)],
                    [(80001013, 2)],
                ],
            },
            {
                "id": 36,
                "name": "1! 2! Party Night!",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 12,
                "score": 2800000,
                "music": [
                    [(70000174, 2)],
                    [(60000081, 2)],
                    [(30000048, 2)],
                ],
            },
            {
                "id": 37,
                "name": "NOBOLOT検定 第8の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 12,
                "score": 2820000,
                "music": [
                    [(50000124, 2)],
                    [(50000291, 2)],
                    [(60000065, 2)],
                ],
            },
            # Jolokili courses
            {
                "id": 41,
                "name": "The 7th KAC 1st Stage 個人部門",
                "course_type": self.COURSE_TYPE_TIME_BASED,
                "end_time": Time.end_of_this_week() + Time.SECONDS_IN_WEEK,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "hard": True,
                "difficulty": 13,
                "score": 700000,
                "music": [
                    [(80000076, 2)],
                    [(80000025, 2)],
                    [(60000073, 2)],
                ],
            },
            {
                "id": 42,
                "name": "The 7th KAC 2nd Stage 個人部門",
                "course_type": self.COURSE_TYPE_TIME_BASED,
                "end_time": Time.end_of_this_week() + Time.SECONDS_IN_WEEK,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "hard": True,
                "difficulty": 13,
                "score": 700000,
                "music": [
                    [(80000081, 2)],
                    [(70000145, 2)],
                    [(80001013, 2)],
                ],
            },
            {
                "id": 43,
                "name": "The 7th KAC 団体部門",
                "course_type": self.COURSE_TYPE_TIME_BASED,
                "end_time": Time.end_of_this_week() + Time.SECONDS_IN_WEEK,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "hard": True,
                "difficulty": 13,
                "score": 700000,
                "music": [
                    [(70000162, 2)],
                    [(70000134, 2)],
                    [(70000173, 1)],
                ],
            },
            {
                "id": 44,
                "name": "ハードモード de ホームラン?!",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 13,
                "score": 2750000,
                "music": [
                    [(50000259, 2)],
                    [(50000255, 2)],
                    [(50000266, 2)],
                ],
            },
            {
                "id": 45,
                "name": "NOBOLOT検定 第9の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "difficulty": 13,
                "score": 2830000,
                "music": [
                    [(50000022, 2)],
                    [(50000023, 2)],
                    [(50000323, 2)],
                ],
            },
            {
                "id": 46,
                "name": "崖っぷちスリーチャレンジ!その2",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_HAZARD,
                "hazard_type": self.COURSE_HAZARD_EXC3,
                "difficulty": 14,
                "music": [
                    [(50000024, 2), (50000160, 2), (70000065, 2)],
                    [(30000122, 2), (50000178, 2), (50000383, 2)],
                    [(50000122, 2), (50000261, 2), (80000010, 2)],
                ],
            },
            {
                "id": 47,
                "name": "もう一つの姿を求めて",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_SCORE,
                "hard": True,
                "difficulty": 14,
                "score": 920000,
                "music": [
                    [(60001009, 2)],
                    [(80001006, 2)],
                    [(80001015, 2)],
                ],
            },
            {
                "id": 48,
                "name": "NOBOLOT検定 第10の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 14,
                "score": 2820000,
                "music": [
                    [(50000202, 2), (50000203, 2), (70000108, 2)],
                    [(40000046, 2), (40000057, 2)],
                    [(50000134, 2)],
                ],
            },
            # Calorest courses
            {
                "id": 51,
                "name": "流れに身を任せて",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 15,
                "score": 2850000,
                "music": [
                    [(60000001, 2)],
                    [(80000022, 2)],
                    [(50000108, 2)],
                ],
            },
            {
                "id": 52,
                "name": "【挑戦】NOBOLOT検定 神の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 15,
                "score": 2850000,
                "music": [
                    [(40000057, 2)],
                    [(60000076, 2)],
                    [(50000102, 2)],
                ],
            },
            {
                "id": 53,
                "name": "伝説の伝導師の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 16,
                "score": 2960000,
                "music": [
                    [(80000028, 2)],
                    [(80000023, 2)],
                    [(80000087, 2)],
                ],
            },
            {
                "id": 54,
                "name": "EXCELLENT MASTER",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_HAZARD,
                "hazard_type": self.COURSE_HAZARD_EXC1,
                "difficulty": 16,
                "music": [
                    [(20000125, 2), (50000330, 2), (40000060, 2)],
                    [(30000127, 2), (50000206, 2), (50000253, 2)],
                    [(70000011, 2)],
                ],
            },
            {
                "id": 55,
                "name": "【挑戦】NOBOLOT検定 英雄の山",
                "course_type": self.COURSE_TYPE_PERMANENT,
                "clear_type": self.COURSE_CLEAR_COMBINED_SCORE,
                "hard": True,
                "difficulty": 16,
                "score": 2980000,
                "music": [
                    [(50000100, 2)],
                    [(70000110, 2)],
                    [(50000208, 2)],
                ],
            },
        ]

    def __get_global_info(self) -> Node:
        info = Node.void("info")

        # Event info.
        event_info = Node.void("event_info")
        info.add_child(event_info)
        # for event in self.EVENTS:
        #     evt = Node.void("event")
        #     event_info.add_child(evt)
        #     evt.set_attribute("type", str(event))
        #     evt.add_child(Node.u8("state", 1 if self.EVENTS[event]["enabled"] else 0))

        # Each of the following two sections should have zero or more child nodes (no
        # particular name) which look like the following:
        #     <node>
        #         <id __type="s32">songid</id>
        #         <stime __type="str">start time?</stime>
        #         <etime __type="str">end time?</etime>
        #     </node>
        # Share music?
        share_music = Node.void("share_music")
        info.add_child(share_music)

        genre_def_music = Node.void("genre_def_music")
        info.add_child(genre_def_music)

        info.add_child(Node.s32_array("black_jacket_list", [0] * 64))

        # Some sort of music DB whitelist
        info.add_child(Node.s32_array("white_music_list", [-1] * 64))

        info.add_child(
            Node.s32_array(
                "white_marker_list",
                [-1, 8191] + [0] * 14
            )
        )

        info.add_child(
            Node.s32_array(
                "white_theme_list",
                [2047] + [0] * 15
            )
        )

        info.add_child(
            Node.s32_array(
                "open_music_list",
                [-2013265951, -102760493, 1711275733, -1579088899, -108536, -227069, -33554401, 16383, 0, -1377473, -402653185, -2097153, -1231036417, -786433, -444727297, -1, 980541439, -33357824, 1077928957, 133988323, 1075838048, -32706, -234907777, -196609, 33138687, -2097152, -907557381, -2, -201326705, -34734081, -524293, -2147042049, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            )
        )

        # A list of songs you can share with others
        info.add_child(Node.s32_array("shareable_music_list", [0] * 64))

        jbox = Node.void("jbox")
        info.add_child(jbox)
        jbox.add_child(Node.s32("point", 0))
        emblem = Node.void("emblem")
        jbox.add_child(emblem)
        normal = Node.void("normal")
        emblem.add_child(normal)
        premium = Node.void("premium")
        emblem.add_child(premium)
        normal.add_child(Node.s16("index", 0))
        premium.add_child(Node.s16("index", 18))

        born = Node.void("born")
        info.add_child(born)
        born.add_child(Node.s8("status", 0))
        born.add_child(Node.s16("year", 0))

        # S Collection event
        # You can earn additional dig points by achieving a rank of S or higher.
        #
        # Collection list values should look like:
        #     <rating>
        #         <id __type="s32">songid</id>
        #         <stime __type="str">start time?</stime>
        #         <etime __type="str">end time?</etime>
        #     </node>
        collection = Node.void("collection")
        info.add_child(collection)
        collection.add_child(Node.void("rating_s"))

        expert_option = Node.void("expert_option")
        info.add_child(expert_option)
        expert_option.add_child(Node.bool("is_available", True))

        all_music_matching = Node.void("all_music_matching")
        info.add_child(all_music_matching)
        all_music_matching.add_child(Node.bool("is_available", True))
        team = Node.void("team")
        all_music_matching.add_child(team)
        team.add_child(Node.s32("default_flag", 0))
        team.add_child(Node.s32("redbelk_flag", 0))
        team.add_child(Node.s32("cyanttle_flag", 0))
        team.add_child(Node.s32("greenesia_flag", 0))
        team.add_child(Node.s32("plumpark_flag", 0))

        # Question list ? Maybe for surveys?
        question_list = Node.void("question_list")
        info.add_child(question_list)

        # question = Node.void("question")
        # question_list.add_child(question)
        # question.set_attribute("release_code", "2018081401")
        # question.set_attribute("data_version", "0")
        # question.set_attribute("id", "1")
        # question.add_child(Node.s32("type", 1))
        # question.add_child(Node.u8("dest", 1))  # dest 1: japan, 2: asia, 3: korea
        # text_line_list = Node.void("text_line_list")
        # question.add_child(text_line_list)
        # text_line_list.add_child(Node.string("text_line", "Hello"))
        # text_line_list.add_child(Node.string("text_line", "Hello2"))
        # text_line_list.add_child(Node.string("text_line", "Hello3"))
        # # Maybe bottom selection buttons?
        # query_list = Node.void("query_list")
        # question.add_child(query_list)
        # query = Node.void("query")
        # query_list.add_child(query)
        # query.set_attribute("id", "1")
        # query.add_child(Node.s32("priority", 1))
        # query.add_child(Node.s64("stime", 0))
        # query.add_child(Node.s64("etime", 0))
        # query_text_line_list = Node.void("text_line_list")
        # query.add_child(query_text_line_list)
        # query_text_line_list.add_child(Node.string("text_line", "Hello"))
        # query_text_line_list.add_child(Node.string("text_line", "Hello2"))
        # query_text_line_list.add_child(Node.string("text_line", "Hello3"))
        # query.add_child(Node.s32("target", 1))

        # Drop ID
        # 1: rainbow, 2: red, 3: cyan, 4: green, 5: purple
        # 6: event drop
        # Maximum 10
        drop_list = Node.void("drop_list")
        info.add_child(drop_list)

        drops = [1, 2, 3, 4, 5, 6]
        for drop in drops:
            dropnode = Node.void("drop")
            drop_list.add_child(dropnode)
            dropnode.set_attribute("release_code", "2017072604")
            dropnode.set_attribute("data_version", "0")
            dropnode.set_attribute("id", str(drop))
            dropnode.add_child(Node.s32("rate", 4))

        daily_bonus_list = Node.void("daily_bonus_list")
        info.add_child(daily_bonus_list)

        # daily_bonus = Node.void("daily_bonus")
        # daily_bonus_list.add_child(daily_bonus)
        # daily_bonus.set_attribute("release_code", "2018081401")
        # daily_bonus.set_attribute("data_version", "0")
        # daily_bonus.set_attribute("id", "1")
        # daily_bonus.set_attribute("tex_number", "1")
        # daily_bonus.add_child(Node.string("stime", "2024-09-01Z00:00"))
        # daily_bonus.add_child(Node.string("etime", "2024-09-30Z23:59"))

        # day_list = Node.void("day_list")
        # daily_bonus.add_child(day_list)

        # for i in range(1, 30):
        #     day = Node.void("day")
        #     day_list.add_child(day)
        #     day.set_attribute("day", str(i))
        #     day.set_attribute("type", "9")  # Reward Type: Music
        #     day.add_child(Node.s32("value", 200))

        shop_list = [
            {
                "id": 1,
                "name": "PACKAGE 01",
                "priority": "1",
                "items": [
                    {
                        "name": "みたらしプラトニック (feat. nicamoq)",
                        "type": "1",
                        "priority": "5",
                        "value": 80000027,
                        "is_secret": False,
                        "drops": [
                            {
                                "id": "1",
                                "grade": "1",
                                "num": 10,
                            }
                        ]
                    },
                    {
                        "name": "Welcome!!",
                        "type": "1",
                        "priority": "4",
                        "value": 80000026,
                        "is_secret": False,
                        "drops": [
                            {
                                "id": "1",
                                "grade": "1",
                                "num": 10,
                            }
                        ]
                    },
                    {
                        "name": "アドレナリン",
                        "type": "1",
                        "priority": "3",
                        "value": 80000024,
                        "is_secret": False,
                        "drops": [
                            {
                                "id": "1",
                                "grade": "1",
                                "num": 10,
                            }
                        ]
                    },
                    {
                        "name": "CandyPop★Showcase",
                        "type": "1",
                        "priority": "2",
                        "value": 80000038,
                        "is_secret": False,
                        "drops": [
                            {
                                "id": "1",
                                "grade": "1",
                                "num": 10,
                            }
                        ]
                    },
                    {
                        "name": "レゾンデートル、前線より",
                        "type": "1",
                        "priority": "1",
                        "value": 80000008,
                        "is_secret": False,
                        "drops": [
                            {
                                "id": "1",
                                "grade": "1",
                                "num": 10,
                            }
                        ]
                    },
                ],
            },
            {
                "id": 2,
                "name": "jubeat SHOP",
                "priority": "2",
                "conditions": [],
                "items": [],
            },
            {
                "id": 3,
                "name": "OMIYAGE CENTER",
                "priority": "3",
                "conditions": [],
                "items": [
                    {
                        "name": "TEST",
                        "type": "2",
                        "priority": "6",
                        "value": 11933,
                        "is_secret": False,
                        "drops": [
                            {
                                "id": "1",
                                "grade": "1",
                                "num": 10,
                            }
                        ]
                    },
                ],
            },
            # {
            #     "id": 5,
            #     "name": "PACKAGE 02",
            #     "release_code": "2018081401",
            #     "data_version": "0",
            #     "priority": "2",
            #     "conditions": [],
            #     "items": [],
            # },
        ]

        department = Node.void("department")
        info.add_child(department)
        pack_list = Node.void("pack_list")
        department.add_child(pack_list)

        for shop in shop_list:
            shopnode = Node.void("shop")
            pack_list.add_child(shopnode)
            shopnode.set_attribute("id", str(shop["id"]))
            shopnode.set_attribute("release_code", "2017072604")
            shopnode.set_attribute("data_version", "0")
            shopnode.set_attribute("priority", str(shop["priority"]))
            if shop.get("stime"):
                shopnode.add_child(Node.string("stime", shop["stime"]))
            if shop.get("etime"):
                shopnode.add_child(Node.string("etime", shop["etime"]))
            if shop.get("formatted_time"):
                shopnode.add_child(Node.string("formatted_time", shop["formatted_time"]))
            if shop.get("conditions"):
                condition_list = Node.void("condition_list")
                shopnode.add_child(condition_list)
            item_list = Node.void("item_list")
            shopnode.add_child(item_list)
            for order, item in enumerate(shop["items"]):
                itemnode = Node.void("item")
                item_list.add_child(itemnode)
                itemnode.set_attribute("id", str(order + 1))
                itemnode.set_attribute("type", str(item["type"]))
                itemnode.set_attribute("priority", str(item["priority"]))
                itemnode.add_child(Node.s32("value", item["value"]))
                itemnode.add_child(Node.bool("is_secret", item["is_secret"]))
                if item.get("conditions"):
                    condition_list = Node.void("condition_list")
                    itemnode.add_child(condition_list)
                drop_list = Node.void("drop_list")
                itemnode.add_child(drop_list)
                for drop in item["drops"]:
                    dropnode = Node.void("drop")
                    drop_list.add_child(dropnode)
                    dropnode.set_attribute("id", drop["id"])
                    dropnode.set_attribute("grade", drop["grade"])
                    dropnode.add_child(Node.s32("num", drop["num"]))

            # package_1 = [80000027, 80000026, 80000024, 80000038, 80000008]
            # drop id  rainbow: 1, red: 2, cyan: 3, green: 4, purple: 5
            # drop grade  normal: 1, silver: 2, gold: 3, rainbow: 4

        # Package 01
        # package = Node.void("package")
        # pack_list.add_child(package)
        # package.set_attribute("id", "1")
        # package.set_attribute("release_code", "2018081401")
        # package.set_attribute("data_version", "0")
        # package.set_attribute("priority", "1")
        # package.add_child(Node.string("stime", "2024-09-01Z00:00"))
        # package.add_child(Node.string("etime", "2024-09-30Z23:59"))
        # package.add_child(Node.string("formatted_time", ""))
        # condition_list = Node.void("condition_list")
        # package.add_child(condition_list)
        # item_list = Node.void("item_list")
        # package.add_child(item_list)

        game_config = self.get_game_config()
        # current_union_battle = game_config.get_int("union_battle")
        current_union_battle = 1

        union_battles: List[Dict[str, Any]] = [
            {
                "id": 1,
                "state": 1,
                "end_time": Time.end_of_this_month(),
                "unions": [
                    {
                        "id": 1,
                        "name": "Redbelk , Greenesia",
                        "teams": [1, 3]
                    },
                    {
                        "id": 2,
                        "name": "Cyanttle , Plumpark",
                        "teams": [2, 4]
                    },
                ],
                "player_rewards": [
                    # type, power, value, is_special
                    [self.REWARD_OMIYAGE_SET, 50, 3020000, False],
                    [self.REWARD_OMIYAGE, 50, 5020001, True],
                    [self.REWARD_BONUS_TUNE_GAUGE, 50, 150, False],
                    [self.REWARD_OMIYAGE_SET, 50, 15010000, False],
                    [self.REWARD_JBOX_PIECE, 50, 100, False],
                    [self.REWARD_MUSIC, 50, 80001014, True],
                    [self.REWARD_BONUS_TUNE_GAUGE, 50, 200, False],
                    [self.REWARD_OMIYAGE_SET, 50, 15010000, False],
                    [self.REWARD_JBOX_PIECE, 50, 100, False],
                    [self.REWARD_OMIYAGE, 50, 1030001, True],
                    [self.REWARD_OMIYAGE, 100, 2030002, False],
                    [self.REWARD_OMIYAGE, 100, 2030003, False],
                    [self.REWARD_OMIYAGE, 100, 2030004, False],
                    [self.REWARD_OMIYAGE, 100, 2030005, False],
                    [self.REWARD_MUSIC, 100, 80000022, True],
                    [self.REWARD_BONUS_TUNE_GAUGE, 100, 200, False],
                    [self.REWARD_OMIYAGE_SET, 100, 5020000, False],
                    [self.REWARD_JBOX_PIECE, 100, 100, False],
                    [self.REWARD_OMIYAGE_SET, 100, 5020000, False],
                    [self.REWARD_OMIYAGE_SET, 100, 1040000, True],

                    # Repeat
                    [self.REWARD_OMIYAGE, 300, 3020002, False],
                    [self.REWARD_OMIYAGE, 300, 3020003, False],
                    [self.REWARD_OMIYAGE, 300, 3020004, False],
                    [self.REWARD_OMIYAGE, 300, 3020005, False],
                    [self.REWARD_OMIYAGE_SET, 300, 1020000, False],
                    [self.REWARD_OMIYAGE, 300, 1020001, False],
                ],
                "basic_rewards": [
                    [self.REWARD_OMIYAGE_SET, 1030000, False],
                    [self.REWARD_OMIYAGE_SET, 10020000, False],
                    [self.REWARD_OMIYAGE_SET, 20010000, False],
                ],
                "win_rewards": [
                    [self.REWARD_OMIYAGE_SET, 1030000, False],
                    [self.REWARD_OMIYAGE_SET, 10020000, False],
                    [self.REWARD_OMIYAGE_SET, 20010000, False],
                ],
                "themes": [
                    {
                        "id": 1,
                        "name": "キュート",
                        "musics": [50000122, 80000061, 70000106, 50000265, 70000125, 90001019, 70000052, 50000214, 20000049, 70000028, 10000067, 50000011, 60000066, 50000038, 70000163, 70000039, 60000096, 70000174, 50000150, 50000247, 50000349, 60000047, 60000012, 50000387, 50000049],
                    },
                    {
                        "id": 2,
                        "name": "クール",
                        "musics": [10000039, 20000040, 60000064, 50000089, 70000055, 70000111, 20000109, 30000123, 80000033, 60000088, 50000156, 70000119, 60000014, 70000160, 50000200, 50000118, 70000026, 50000024, 50000097, 50000064, 50000059, 50000251, 50000050, 40000015, 70000053],
                    },
                ],
            }
        ]

        if current_union_battle > 0:
            battle = union_battles[current_union_battle - 1]
            union_battle = Node.void("union_battle")
            info.add_child(union_battle)
            union_battle.set_attribute("release_code", "2017072604")
            union_battle.set_attribute("data_version", "0")
            union_battle.set_attribute("id", "1")
            union_battle.add_child(Node.u8("state", battle["state"]))  # 1 - enable, 2 - end
            union_battle.add_child(Node.u64("etime", battle["end_time"] * 1000))
            union_list = Node.void("union_list")
            union_battle.add_child(union_list)
            union_list.add_child(Node.u64("time", Time.now()))
            union_list.add_child(Node.bool("is_display", True))

            for union in battle["unions"]:
                unionnode = Node.void("union")
                union_list.add_child(unionnode)
                unionnode.set_attribute("id", str(union["id"]))
                unionnode.add_child(Node.s32("power", 0))
                team_list = Node.void("team_list")
                unionnode.add_child(team_list)
                for team in union["teams"]:
                    teamnode = Node.void("team")
                    team_list.add_child(teamnode)
                    teamnode.set_attribute("id", str(team))

            player_reward = Node.void("player_reward")
            union_battle.add_child(player_reward)
            player_reward_list = Node.void("reward_list")
            player_reward.add_child(player_reward_list)

            for reward in battle["player_rewards"]:
                rewardnode = Node.void("reward")
                player_reward_list.add_child(rewardnode)
                rewardnode.set_attribute("type", str(reward[0]))
                rewardnode.set_attribute("power", str(reward[1]))
                rewardnode.add_child(Node.s32("value", reward[2]))
                rewardnode.add_child(Node.bool("is_special", reward[3]))

            win_reward = Node.void("win_reward")
            union_battle.add_child(win_reward)
            win_reward_list = Node.void("reward_list")
            win_reward.add_child(win_reward_list)
            for reward in battle["win_rewards"]:
                rewardnode = Node.void("reward")
                win_reward_list.add_child(rewardnode)
                rewardnode.set_attribute("type", str(reward[0]))
                rewardnode.add_child(Node.s32("value", reward[1]))
                rewardnode.add_child(Node.bool("is_special", reward[2]))
            basic_reward = Node.void("basic_reward")
            union_battle.add_child(basic_reward)
            basic_reward_list = Node.void("reward_list")
            basic_reward.add_child(basic_reward_list)
            for reward in battle["basic_rewards"]:
                rewardnode = Node.void("reward")
                basic_reward_list.add_child(rewardnode)
                rewardnode.set_attribute("type", str(reward[0]))
                rewardnode.add_child(Node.s32("value", reward[1]))
                rewardnode.add_child(Node.bool("is_special", reward[2]))

            theme_list = Node.void("theme_list")
            union_battle.add_child(theme_list)
            for theme in battle["themes"]:
                themenode = Node.void("theme")
                theme_list.add_child(themenode)
                themenode.set_attribute("id", str(theme["id"]))
                themenode.add_child(Node.string("name", theme["name"]))
                bonus_music_list = Node.void("bonus_music_list")
                themenode.add_child(bonus_music_list)
                for music in theme["musics"]:
                    bonus_music = Node.void("bonus_music")
                    bonus_music_list.add_child(bonus_music)
                    bonus_music.set_attribute("id", str(music))

        if current_union_battle > 0:
            battle = union_battles[current_union_battle - 1]
            if battle["state"] >= 2:
                union_battle_reward = Node.void("union_battle_reward")
                info.add_child(union_battle_reward)
                union_battle_reward.set_attribute("release_code", "2017072604")
                union_battle_reward.set_attribute("data_version", "0")
                union_battle_reward.set_attribute("id", "1")
                union_list = Node.void("union_list")
                union_battle_reward.add_child(union_list)
                for union in battle["unions"]:
                    unionnode = Node.void("union")
                    union_list.add_child(unionnode)
                    unionnode.set_attribute("id", str(union["id"]))
                    unionnode.add_child(Node.s32("power", 100 if union["id"] == 1 else 0))
                    team_list = Node.void("team_list")
                    unionnode.add_child(team_list)
                    for team in union["teams"]:
                        teamnode = Node.void("team")
                        team_list.add_child(teamnode)
                        teamnode.set_attribute("id", str(team))
                win_reward = Node.void("win_reward")
                union_battle_reward.add_child(win_reward)
                win_reward_list = Node.void("reward_list")
                win_reward.add_child(win_reward_list)
                for reward in battle["win_rewards"]:
                    rewardnode = Node.void("reward")
                    win_reward_list.add_child(rewardnode)
                    rewardnode.set_attribute("type", str(reward[0]))
                    rewardnode.add_child(Node.s32("value", reward[1]))
                    rewardnode.add_child(Node.bool("is_special", reward[2]))
                basic_reward = Node.void("basic_reward")
                union_battle_reward.add_child(basic_reward)
                basic_reward_list = Node.void("reward_list")
                basic_reward.add_child(basic_reward_list)
                for reward in battle["basic_rewards"]:
                    rewardnode = Node.void("reward")
                    basic_reward_list.add_child(rewardnode)
                    rewardnode.set_attribute("type", str(reward[0]))
                    rewardnode.add_child(Node.s32("value", reward[1]))
                    rewardnode.add_child(Node.bool("is_special", reward[2]))

        # Set up NOBOLOT course requirements
        clan_course_list = Node.void("clan_course_list")
        info.add_child(clan_course_list)

        # valid_courses: Set[int] = set()
        # for course in self.__get_course_list():
        #     if course["id"] < 1:
        #         raise Exception(f"Invalid course ID {course['id']} found in course list!")
        #     if course["id"] in valid_courses:
        #         raise Exception(f"Duplicate ID {course['id']} found in course list!")
        #     if course["clear_type"] == self.COURSE_CLEAR_HAZARD and "hazard_type" not in course:
        #         raise Exception(f"Need 'hazard_type' set in course {course['id']}!")
        #     if course["course_type"] == self.COURSE_TYPE_TIME_BASED and "end_time" not in course:
        #         raise Exception(f"Need 'end_time' set in course {course['id']}!")
        #     if (
        #         course["clear_type"] in [self.COURSE_CLEAR_SCORE, self.COURSE_CLEAR_COMBINED_SCORE]
        #         and "score" not in course
        #     ):
        #         raise Exception(f"Need 'score' set in course {course['id']}!")
        #     if course["clear_type"] == self.COURSE_CLEAR_SCORE and course["score"] > 1000000:
        #         raise Exception(f"Invalid per-coure score in course {course['id']}!")
        #     if course["clear_type"] == self.COURSE_CLEAR_COMBINED_SCORE and course["score"] <= 1000000:
        #         raise Exception(f"Invalid combined score in course {course['id']}!")
        #     valid_courses.add(course["id"])

        #     # Basics
        #     clan_course = Node.void("clan_course")
        #     clan_course_list.add_child(clan_course)
        #     clan_course.set_attribute("release_code", "2017062600")
        #     clan_course.set_attribute("version_id", "0")
        #     clan_course.set_attribute("id", str(course["id"]))
        #     clan_course.set_attribute("course_type", str(course["course_type"]))
        #     clan_course.add_child(Node.s32("difficulty", course["difficulty"]))
        #     clan_course.add_child(Node.u64("etime", (course["end_time"] if "end_time" in course else 0) * 1000))
        #     clan_course.add_child(Node.string("name", course["name"]))

        #     # List of included songs
        #     tune_list = Node.void("tune_list")
        #     clan_course.add_child(tune_list)
        #     for order, charts in enumerate(course["music"]):
        #         tune = Node.void("tune")
        #         tune_list.add_child(tune)
        #         tune.set_attribute("no", str(order + 1))

        #         seq_list = Node.void("seq_list")
        #         tune.add_child(seq_list)

        #         for songid, chart in charts:
        #             seq = Node.void("seq")
        #             seq_list.add_child(seq)
        #             seq.add_child(Node.s32("music_id", songid))
        #             seq.add_child(Node.s32("difficulty", chart))
        #             seq.add_child(Node.bool("is_secret", False))

        #     # Clear criteria
        #     clear = Node.void("clear")
        #     clan_course.add_child(clear)
        #     ex_option = Node.void("ex_option")
        #     clear.add_child(ex_option)
        #     ex_option.add_child(Node.bool("is_hard", course["hard"] if "hard" in course else False))
        #     ex_option.add_child(
        #         Node.s32(
        #             "hazard_type",
        #             course["hazard_type"] if "hazard_type" in course else 0,
        #         )
        #     )
        #     clear.set_attribute("type", str(course["clear_type"]))
        #     clear.add_child(Node.s32("score", course["score"] if "score" in course else 0))

        #     reward_list = Node.void("reward_list")
        #     clear.add_child(reward_list)

        # Set up NOBOLOT category display
        category_list = Node.void("category_list")
        clan_course_list.add_child(category_list)

        # Each category has one of the following nodes
        # categories: List[Tuple[int, int]] = [
        #     (1, 3),
        #     (4, 6),
        #     (7, 9),
        #     (10, 12),
        #     (13, 14),
        #     (15, 16),
        # ]
        # for categoryid, (min_level, max_level) in enumerate(categories):
        #     category = Node.void("category")
        #     category_list.add_child(category)
        #     category.set_attribute("id", str(categoryid + 1))
        #     category.add_child(Node.bool("is_secret", False))
        #     category.add_child(Node.s32("level_min", min_level))
        #     category.add_child(Node.s32("level_max", max_level))

        return info

    def handle_shopinfo_regist_request(self, request: Node) -> Node:
        # Update the name of this cab for admin purposes
        self.update_machine_name(request.child_value("shop/name"))

        shopinfo = Node.void("shopinfo")

        data = Node.void("data")
        shopinfo.add_child(data)
        data.add_child(Node.u32("cabid", 1))
        data.add_child(Node.string("locationid", "nowhere"))
        data.add_child(Node.u8("tax_phase", 1))

        facility = Node.void("facility")
        data.add_child(facility)
        facility.add_child(Node.u32("exist", 1))

        data.add_child(self.__get_global_info())

        return shopinfo

    def handle_demodata_get_info_request(self, request: Node) -> Node:
        root = Node.void("demodata")
        data = Node.void("data")
        root.add_child(data)
        info = Node.void("info")
        data.add_child(info)
        info.add_child(Node.s32_array("black_jacket_list", [0] * 64))
        return root

    def handle_demodata_get_jbox_list_request(self, request: Node) -> Node:
        root = Node.void("demodata")
        return root

    def handle_jbox_get_agreement_request(self, request: Node) -> Node:
        root = Node.void("jbox")
        root.add_child(Node.bool("is_agreement", True))
        return root

    def handle_jbox_get_list_request(self, request: Node) -> Node:
        root = Node.void("jbox")
        root.add_child(Node.void("selection_list"))
        return root

    def handle_recommend_get_recommend_request(self, request: Node) -> Node:
        recommend = Node.void("recommend")
        data = Node.void("data")
        recommend.add_child(data)

        player = Node.void("player")
        data.add_child(player)
        music_list = Node.void("music_list")
        player.add_child(music_list)

        # TODO: Might be a way to figure out who plays what song and then offer
        # recommendations based on that. There should be 12 songs returned here.
        recommended_songs: List[Song] = []
        for i, song in enumerate(recommended_songs):
            music = Node.void("music")
            music_list.add_child(music)
            music.set_attribute("order", str(i))
            music.add_child(Node.s32("music_id", song.id))
            music.add_child(Node.s8("seq", song.chart))

        return recommend

    def handle_gametop_get_info_request(self, request: Node) -> Node:
        root = Node.void("gametop")
        data = Node.void("data")
        root.add_child(data)
        data.add_child(self.__get_global_info())

        return root

    def handle_gametop_regist_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/refid")
        name = request.child_value("data/player/name")
        root = self.new_profile_by_refid(refid, name)
        return root

    def handle_gametop_get_pdata_request(self, request: Node) -> Node:
        refid = request.child_value("data/player/refid")
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

    def handle_gameend_final_request(self, request: Node) -> Node:
        player = request.child("data/player")

        if player is not None:
            refid = player.child_value("refid")
        else:
            refid = None

        if refid is not None:
            userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            profile = self.get_profile(userid)

            # Grab unlock progress
            item = player.child("item")
            if item is not None:
                owned_emblems = self.calculate_owned_items(item.child_value("emblem_list"))
                for index in owned_emblems:
                    self.data.local.user.put_achievement(
                        self.game,
                        self.version,
                        userid,
                        index,
                        "emblem",
                        {},
                    )

            # jbox stuff
            jbox = player.child("jbox")
            jboxdict = profile.get_dict("jbox")
            if jbox is not None:
                jboxdict.replace_int("point", jbox.child_value("point"))
                emblemtype = jbox.child_value("emblem/type")
                index = jbox.child_value("emblem/index")
                if emblemtype == self.JBOX_EMBLEM_NORMAL:
                    jboxdict.replace_int("normal_index", index)
                elif emblemtype == self.JBOX_EMBLEM_PREMIUM:
                    jboxdict.replace_int("premium_index", index)
            profile.replace_dict("jbox", jboxdict)

            # Born stuff
            born = player.child("born")
            if born is not None:
                profile.replace_int("born_status", born.child_value("status"))
                profile.replace_int("born_year", born.child_value("year"))
        else:
            profile = None

        if userid is not None and profile is not None:
            self.put_profile(userid, profile)

        return Node.void("gameend")

    def format_scores(self, userid: UserID, profile: Profile, scores: List[Score]) -> Node:
        root = Node.void("gametop")
        datanode = Node.void("data")
        root.add_child(datanode)
        player = Node.void("player")
        datanode.add_child(player)
        player.add_child(Node.s32("jid", profile.extid))
        playdata = Node.void("mdata_list")
        player.add_child(playdata)

        music = ValidatedDict()
        for score in scores:
            # Ignore festo-and-above chart types.
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

            # Replace data for this chart type
            play_cnt[score.chart] = score.plays
            clear_cnt[score.chart] = score.data.get_int("clear_count")
            fc_cnt[score.chart] = score.data.get_int("full_combo_count")
            ex_cnt[score.chart] = score.data.get_int("excellent_count")
            points[score.chart] = score.points

            # Format the clear flags
            clear_flags[score.chart] = self.GAME_FLAG_BIT_PLAYED
            if score.data.get_int("clear_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_CLEARED
            if score.data.get_int("full_combo_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_FULL_COMBO
            if score.data.get_int("excellent_count") > 0:
                clear_flags[score.chart] |= self.GAME_FLAG_BIT_EXCELLENT

            # Save chart data back
            data.replace_int_array("play_cnt", 3, play_cnt)
            data.replace_int_array("clear_cnt", 3, clear_cnt)
            data.replace_int_array("clear_flags", 3, clear_flags)
            data.replace_int_array("fc_cnt", 3, fc_cnt)
            data.replace_int_array("ex_cnt", 3, ex_cnt)
            data.replace_int_array("points", 3, points)

            # Update the ghost (untyped)
            ghost = data.get("ghost", [None, None, None])
            ghost[score.chart] = score.data.get("ghost")
            data["ghost"] = ghost

            # Save it back
            if score.id in self.FIVE_PLAYS_UNLOCK_EVENT_SONG_IDS:
                # Mirror it to every version so the score shows up regardless of
                # prefecture setting.
                for prefecture_id in self.FIVE_PLAYS_UNLOCK_EVENT_SONG_IDS:
                    music.replace_dict(str(prefecture_id), data)
            else:
                # Regular copy.
                music.replace_dict(str(score.id), data)

        for scoreid in music:
            scoredata = music.get_dict(scoreid)
            musicdata = Node.void("musicdata")
            playdata.add_child(musicdata)

            musicdata.set_attribute("music_id", scoreid)
            musicdata.add_child(Node.s32_array("play_cnt", scoredata.get_int_array("play_cnt", 3)))
            musicdata.add_child(Node.s32_array("clear_cnt", scoredata.get_int_array("clear_cnt", 3)))
            musicdata.add_child(Node.s32_array("fc_cnt", scoredata.get_int_array("fc_cnt", 3)))
            musicdata.add_child(Node.s32_array("ex_cnt", scoredata.get_int_array("ex_cnt", 3)))
            musicdata.add_child(Node.s32_array("score", scoredata.get_int_array("points", 3)))
            musicdata.add_child(Node.s8_array("clear", scoredata.get_int_array("clear_flags", 3)))

            for i, ghost in enumerate(scoredata.get("ghost", [None, None, None])):
                if ghost is None:
                    continue

                bar = Node.u8_array("bar", ghost)
                musicdata.add_child(bar)
                bar.set_attribute("seq", str(i))

        return root

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("gametop")
        data = Node.void("data")
        root.add_child(data)

        # Figure out if we're force-unlocking songs.
        game_config = self.get_game_config()
        force_unlock = game_config.get_bool("force_song_unlock")

        # Calculate all of our achievement-backed entities.
        achievements = self.data.local.user.get_achievements(self.game, self.version, userid)
        owned_songs: Set[int] = set()
        owned_secrets: Set[int] = set()
        event_completion: Dict[int, bool] = {}
        course_completion: Dict[int, ValidatedDict] = {}
        owned_emblems: Set[int] = set()
        for achievement in achievements:
            if achievement.type == "event":
                event_completion[achievement.id] = achievement.data.get_bool("is_completed")
            elif achievement.type == "course":
                course_completion[achievement.id] = achievement.data
            elif achievement.type == "emblem":
                owned_emblems.add(achievement.id)
            elif achievement.type == "song":
                owned_songs.add(achievement.id)
            elif achievement.type == "secret":
                owned_secrets.add(achievement.id)

        # Make sure we grant ownership of default main parts.
        default_emblems = self.default_select_jbox()
        owned_emblems.update(default_emblems)
        default_main = next(iter(default_emblems)) if default_emblems else 0

        # Jubeat Clan appears to allow full event overrides per-player
        data.add_child(self.__get_global_info())

        player = Node.void("player")
        data.add_child(player)

        # Basic profile info
        player.add_child(Node.string("name", profile.get_str("name", "なし")))
        player.add_child(Node.s32("jid", profile.extid))

        # Miscelaneous crap
        player.add_child(Node.s32("session_id", 1))
        player.add_child(Node.u64("event_flag", profile.get_int("event_flag")))

        # Player info and statistics
        info = Node.void("info")
        player.add_child(info)
        info.add_child(Node.s32("tune_cnt", profile.get_int("tune_cnt")))
        info.add_child(Node.s32("save_cnt", profile.get_int("save_cnt")))
        info.add_child(Node.s32("saved_cnt", profile.get_int("saved_cnt")))
        info.add_child(Node.s32("fc_cnt", profile.get_int("fc_cnt")))
        info.add_child(Node.s32("ex_cnt", profile.get_int("ex_cnt")))
        info.add_child(Node.s32("clear_cnt", profile.get_int("clear_cnt")))
        info.add_child(Node.s32("match_cnt", profile.get_int("match_cnt")))
        info.add_child(Node.s32("beat_cnt", profile.get_int("beat_cnt")))
        info.add_child(Node.s32("mynews_cnt", profile.get_int("mynews_cnt")))
        info.add_child(Node.s32("bonus_tune_points", profile.get_int("bonus_tune_points")))
        info.add_child(Node.bool("is_bonus_tune_played", profile.get_bool("is_bonus_tune_played")))

        # Looks to be set to true when there's an old profile, stops tutorial from
        # happening on first load.
        info.add_child(
            Node.bool(
                "inherit",
                profile.get_bool("has_old_version") and not profile.get_bool("saved"),
            )
        )

        # Not saved, but loaded
        info.add_child(Node.s32("mtg_entry_cnt", 123))
        info.add_child(Node.s32("mtg_hold_cnt", 456))
        info.add_child(Node.u8("mtg_result", 10))

        # Last played data, for showing cursor and such
        lastdict = profile.get_dict("last")
        last = Node.void("last")
        player.add_child(last)
        last.add_child(Node.s64("play_time", lastdict.get_int("play_time")))
        last.add_child(Node.string("shopname", lastdict.get_str("shopname")))
        last.add_child(Node.string("areaname", lastdict.get_str("areaname")))
        last.add_child(Node.s32("music_id", lastdict.get_int("music_id")))
        last.add_child(Node.s8("seq_id", lastdict.get_int("seq_id")))
        last.add_child(Node.s8("sort", lastdict.get_int("sort")))
        last.add_child(Node.s8("category", lastdict.get_int("category")))
        last.add_child(Node.s8("expert_option", lastdict.get_int("expert_option")))

        settings = Node.void("settings")
        last.add_child(settings)
        settings.add_child(Node.s8("marker", lastdict.get_int("marker")))
        settings.add_child(Node.s8("theme", lastdict.get_int("theme")))
        settings.add_child(Node.s16("title", lastdict.get_int("title")))
        settings.add_child(Node.s16("parts", lastdict.get_int("parts")))
        settings.add_child(Node.s8("rank_sort", lastdict.get_int("rank_sort")))
        settings.add_child(Node.s8("combo_disp", lastdict.get_int("combo_disp")))
        settings.add_child(Node.s8("matching", lastdict.get_int("matching")))
        settings.add_child(Node.s8("hard", lastdict.get_int("hard")))
        settings.add_child(Node.s8("hazard", lastdict.get_int("hazard")))

        # Hack to make the default emblem appear properly.
        partslist = lastdict.get_int_array("emblem", 5, [0, default_main, 0, 0, 0])
        if partslist[1] == 0:
            partslist[1] = default_main
        settings.add_child(Node.s16_array("emblem", partslist))

        # Secret unlocks
        item = Node.void("item")
        player.add_child(item)
        item.add_child(
            Node.s32_array(
                "music_list",
                [-2013265951, -102760493, 1711275733, -1579088899, -108536, -227069, -33554401, 16383, 0, -1377473, -402653185, -2097153, -1231036417, -786433, -444727297, -1, 980541439, -33357824, 1077928957, 133988323, 1075838048, -32706, -234907777, -196609, 33138687, -2097152, -907557381, -2, -201326705, -34734081, -524293, -2147042049, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            )
        )
        item.add_child(
            Node.s32_array(
                "secret_list",
                [0] * 64,
            )
        )
        item.add_child(Node.s32_array("theme_list", profile.get_int_array("theme_list", 16, [0] * 16)))
        item.add_child(Node.s32_array("marker_list", profile.get_int_array("marker_list", 16, [0] * 16)))
        item.add_child(Node.s32_array("title_list", profile.get_int_array("title_list", 160, [0] * 160)))
        item.add_child(Node.s32_array("parts_list", profile.get_int_array("parts_list", 160, [0] * 160)))
        item.add_child(Node.s32_array("emblem_list", [0] * 96))
        item.add_child(Node.s32_array("commu_list", profile.get_int_array("commu_list", 16, [0] * 16)))

        new = Node.void("new")
        item.add_child(new)
        new.add_child(
            Node.s32_array(
                "secret_list",
                ([0] * 64) if force_unlock else self.create_owned_items(owned_secrets, 64),
            )
        )
        new.add_child(Node.s32_array("theme_list", profile.get_int_array("theme_list_new", 16, [0] * 16)))
        new.add_child(Node.s32_array("marker_list", profile.get_int_array("marker_list_new", 16, [0] * 16)))

        # Add rivals to profile.
        rivallist = Node.void("rivallist")
        player.add_child(rivallist)

        links = self.data.local.user.get_links(self.game, self.version, userid)
        rivalcount = 0
        for link in links:
            if link.type != "rival":
                continue

            rprofile = self.get_profile(link.other_userid)
            if rprofile is None:
                continue

            rival = Node.void("rival")
            rivallist.add_child(rival)
            rival.add_child(Node.s32("jid", rprofile.extid))
            rival.add_child(Node.string("name", rprofile.get_str("name")))

            # This looks like a carry-over from prop's career and isn't displayed.
            career = Node.void("career")
            rival.add_child(career)
            career.add_child(Node.s16("level", 1))

            # Lazy way of keeping track of rivals, since we can only have 3
            # or the game with throw up.
            rivalcount += 1
            if rivalcount >= 3:
                break

        rivallist.set_attribute("count", str(rivalcount))

        lab_edit_seq = Node.void("lab_edit_seq")
        player.add_child(lab_edit_seq)
        lab_edit_seq.set_attribute("count", "0")

        # Full combo challenge
        entry = self.data.local.game.get_time_sensitive_settings(self.game, self.version, "fc_challenge")
        if entry is None:
            entry = ValidatedDict()

        # Figure out if we've played these songs
        start_time, end_time = self.data.local.network.get_schedule_duration("daily")
        today_attempts = self.data.local.music.get_all_attempts(
            self.game,
            self.music_version,
            userid,
            entry.get_int("today", -1),
            timelimit=start_time,
        )
        whim_attempts = self.data.local.music.get_all_attempts(
            self.game,
            self.music_version,
            userid,
            entry.get_int("whim", -1),
            timelimit=start_time,
        )

        fc_challenge = Node.void("fc_challenge")
        player.add_child(fc_challenge)
        today = Node.void("today")
        fc_challenge.add_child(today)
        today.add_child(Node.s32("music_id", entry.get_int("today", -1)))
        today.add_child(Node.u8("state", 0x40 if len(today_attempts) > 0 else 0x0))
        whim = Node.void("whim")
        fc_challenge.add_child(whim)
        whim.add_child(Node.s32("music_id", entry.get_int("whim", -1)))
        whim.add_child(Node.u8("state", 0x40 if len(whim_attempts) > 0 else 0x0))

        # No news, ever.
        official_news = Node.void("official_news")
        player.add_child(official_news)
        news_list = Node.void("news_list")
        official_news.add_child(news_list)

        # Sane defaults for unknown/who cares nodes
        history = Node.void("history")
        player.add_child(history)
        history.set_attribute("count", "0")

        free_first_play = Node.void("free_first_play")
        player.add_child(free_first_play)
        free_first_play.add_child(Node.bool("is_available", False))

        # Player status for events
        event_info = Node.void("event_info")
        player.add_child(event_info)
        for eventid, eventdata in self.EVENTS.items():
            # There are two significant bits here, bit 0 and bit 1, I think the first
            # one is whether the event is started, second is if its finished?
            event = Node.void("event")
            event_info.add_child(event)
            event.set_attribute("type", str(eventid))

            state = 0x0
            state |= self.EVENT_STATUS_OPEN if eventdata["enabled"] else 0
            state |= self.EVENT_STATUS_COMPLETE if event_completion.get(eventid, False) else 0
            event.add_child(Node.u8("state", state))

        # JBox stuff
        jbox = Node.void("jbox")
        jboxdict = profile.get_dict("jbox")
        player.add_child(jbox)
        jbox.add_child(Node.s32("point", jboxdict.get_int("point")))
        emblem = Node.void("emblem")
        jbox.add_child(emblem)
        normal = Node.void("normal")
        emblem.add_child(normal)
        premium = Node.void("premium")
        emblem.add_child(premium)

        # Calculate a random index for normal and premium to give to player
        # as a gatcha.
        normalindex, premiumindex = self.random_select_jbox(owned_emblems)
        normal.add_child(Node.s16("index", normalindex))
        premium.add_child(Node.s16("index", premiumindex))

        # New Music stuff
        new_music = Node.void("new_music")
        player.add_child(new_music)

        navi = Node.void("navi")
        player.add_child(navi)
        navi.add_child(Node.u64("flag", profile.get_int("navi_flag")))

        # Gift list, maybe from other players?
        gift_list = Node.void("gift_list")
        player.add_child(gift_list)
        # If we had gifts, they look like this:
        #     <gift reason="??" kind="??">
        #         <id __type="s32">??</id>
        #     </gift>
        # gift = Node.void("gift")
        # gift_list.add_child(gift)
        # gift.set_attribute("kind", "1")  # only 1
        # gift.set_attribute("reason", "1")  # doesn't matter
        # gift.add_child(Node.s32("id", 80000027))

        # Birthday event?
        born = Node.void("born")
        player.add_child(born)
        born.add_child(Node.s8("status", profile.get_int("born_status")))
        born.add_child(Node.s16("year", profile.get_int("born_year")))

        # More crap
        question_list = Node.void("question_list")
        player.add_child(question_list)

        # Player Jubility
        jubility = Node.void("jubility")
        player.add_child(jubility)
        jubility.set_attribute("param", str(profile.get_int("jubility")))
        target_music_list = Node.void("target_music_list")
        jubility.add_child(target_music_list)

        # Calculate top 30 songs contributing to jubility.
        jubeat_entries: List[ValidatedDict] = []
        for achievement in achievements:
            if achievement.type != "jubility":
                continue

            # Figure out for each song, what's the highest value jubility and
            # keep that.
            bestentry = ValidatedDict()
            for chart in [0, 1, 2]:
                entry = achievement.data.get_dict(str(chart))
                if entry.get_int("value") >= bestentry.get_int("value"):
                    bestentry = entry.clone()
                    bestentry.replace_int("songid", achievement.id)
                    bestentry.replace_int("chart", chart)
            jubeat_entries.append(bestentry)
        jubeat_entries = sorted(jubeat_entries, key=lambda entry: entry.get_int("value"), reverse=True)

        # Now, give the game the list.
        for i, entry in enumerate(jubeat_entries):
            # The game only reads the top 30 anyway, so skip extra network traffic.
            if i >= 30:
                break

            target_music = Node.void("target_music")
            target_music_list.add_child(target_music)
            target_music.add_child(Node.s32("music_id", entry.get_int("songid")))
            target_music.add_child(Node.s8("seq", entry.get_int("chart")))
            target_music.add_child(Node.s32("score", entry.get_int("score")))
            target_music.add_child(Node.s32("value", entry.get_int("value")))
            target_music.add_child(Node.bool("is_hard_mode", entry.get_bool("hard_mode")))

        # Team stuff
        team = Node.void("team")
        teamdict = profile.get_dict("team")
        player.add_child(team)
        team.set_attribute("id", str(teamdict.get_int("id")))
        team.add_child(Node.s32("section", teamdict.get_int("section")))
        team.add_child(Node.s32("street", teamdict.get_int("street")))
        team.add_child(Node.s32("house_number_1", teamdict.get_int("house_1")))
        team.add_child(Node.s32("house_number_2", teamdict.get_int("house_2")))

        # Set up where the player moves to (random) after their first play
        move = Node.void("move")
        team.add_child(move)
        # 1 - Redbelk, 2 - Cyantle, 3 - Greenesia, 4 - Plumpark
        move.set_attribute("id", str(random.choice([1, 2, 3, 4])))
        move.set_attribute("section", str(random.choice([1, 2, 3, 4, 5])))
        move.set_attribute("street", str(random.choice([1, 2, 3, 4, 5, 6])))
        move.set_attribute("house_number_1", str(random.choice(range(10, 100))))
        move.set_attribute("house_number_2", str(random.choice(range(10, 100))))

        # Union Battle
        union_battle = Node.void("union_battle")
        player.add_child(union_battle)
        union_battle.set_attribute("id", "1")
        union_battle.add_child(Node.s32("power", -1))

        # Some server node
        server = Node.void("server")
        player.add_child(server)

        # Another unknown gift list?
        eamuse_gift_list = Node.void("eamuse_gift_list")
        player.add_child(eamuse_gift_list)

        gift = Node.void("gift")
        eamuse_gift_list.add_child(gift)
        gift.add_child(Node.string("content_id", "1"))
        detail = Node.void("detail")
        gift.add_child(detail)
        detail.set_attribute("type", "6")
        detail.add_child(Node.s32("value", 6))
        detail.add_child(Node.bool("is_special", False))
        # reward = Node.void("reward")
        # gift.add_child(reward)
        # reward.set_attribute("type", "6")  # 6, 7, 8, 10
        # reward.add_child(Node.s32("value", 1))

        # Clan Course List Progress
        clan_course_list = Node.void("clan_course_list")
        player.add_child(clan_course_list)

        # Each course that we have completed has one of the following nodes.
        for course in self.__get_course_list():
            status_dict = course_completion.get(course["id"], ValidatedDict())
            status = 0
            status |= self.COURSE_STATUS_SEEN if status_dict.get_bool("seen") else 0
            status |= self.COURSE_STATUS_PLAYED if status_dict.get_bool("played") else 0
            status |= self.COURSE_STATUS_CLEARED if status_dict.get_bool("cleared") else 0

            clan_course = Node.void("clan_course")
            clan_course_list.add_child(clan_course)
            clan_course.set_attribute("id", str(course["id"]))
            clan_course.add_child(Node.s8("status", status))

        category_list = Node.void("category_list")
        player.add_child(category_list)

        # Each category has one of the following nodes
        for categoryid in range(1, 7):
            category = Node.void("category")
            category_list.add_child(category)
            category.set_attribute("id", str(categoryid))
            category.add_child(Node.bool("is_display", True))

        # Drop list
        drop_list = Node.void("drop_list")
        player.add_child(drop_list)

        dropachievements: Dict[int, Achievement] = {}
        for achievement in achievements:
            if achievement.type == "drop":
                dropachievements[achievement.id] = achievement

        for dropid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            if dropid in dropachievements:
                dropdata = dropachievements[dropid].data
            else:
                dropdata = ValidatedDict()

            drop = Node.void("drop")
            drop_list.add_child(drop)
            drop.set_attribute("id", str(dropid))
            drop.add_child(Node.s32("exp", dropdata.get_int("exp", -1)))
            drop.add_child(Node.s32("flag", dropdata.get_int("flag", 0)))

            item_list = Node.void("item_list")
            drop.add_child(item_list)

            for itemid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                item = Node.void("item")
                item_list.add_child(item)
                item.set_attribute("id", str(itemid))
                item.add_child(Node.s32("num", 99))  # dropdata.get_int(f"item_{itemid}")

        # Fill in category
        fill_in_category = Node.void("fill_in_category")
        player.add_child(fill_in_category)
        fill_in_category.add_child(
            Node.s32_array(
                "no_gray_flag_list",
                profile.get_int_array("no_gray_flag_list", 16, [0] * 16),
            )
        )
        fill_in_category.add_child(
            Node.s32_array(
                "all_yellow_flag_list",
                profile.get_int_array("all_yellow_flag_list", 16, [0] * 16),
            )
        )
        fill_in_category.add_child(
            Node.s32_array(
                "full_combo_flag_list",
                profile.get_int_array("full_combo_flag_list", 16, [0] * 16),
            )
        )
        fill_in_category.add_child(
            Node.s32_array(
                "excellent_flag_list",
                profile.get_int_array("excellent_flag_list", 16, [0] * 16),
            )
        )

        # Daily Bonus
        daily_bonus_list = Node.void("daily_bonus_list")
        player.add_child(daily_bonus_list)

        # daily_bonus = Node.void("daily_bonus")
        # daily_bonus_list.add_child(daily_bonus)
        # daily_bonus.set_attribute("id", "1")
        # daily_bonus.add_child(Node.s32("accepted_day", 0))
        # daily_bonus.add_child(Node.s32("now_day", 1))

        # Tickets
        ticket_list = Node.void("ticket_list")
        player.add_child(ticket_list)

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        newprofile.replace_bool("saved", True)
        data = request.child("data")

        # Figure out if we're force-unlocking songs. If we are, we don't want to persist
        # secret stuff otherwise the game will accidentally unlock everything in the profile.
        game_config = self.get_game_config()
        force_unlock = game_config.get_bool("force_song_unlock")

        # Grab system information
        sysinfo = data.child("info")

        # Grab player information
        player = data.child("player")

        # Grab result information
        result = data.child("result")

        # Grab last information. Lots of this will be filled in while grabbing scores
        last = newprofile.get_dict("last")
        if sysinfo is not None:
            last.replace_int("play_time", sysinfo.child_value("time_gameend"))
            last.replace_str("shopname", sysinfo.child_value("shopname"))
            last.replace_str("areaname", sysinfo.child_value("areaname"))

        # Grab player info for echoing back
        info = player.child("info")
        if info is not None:
            newprofile.replace_int("tune_cnt", info.child_value("tune_cnt"))
            newprofile.replace_int("save_cnt", info.child_value("save_cnt"))
            newprofile.replace_int("saved_cnt", info.child_value("saved_cnt"))
            newprofile.replace_int("fc_cnt", info.child_value("fc_cnt"))
            newprofile.replace_int("ex_cnt", info.child_value("ex_cnt"))
            newprofile.replace_int("clear_cnt", info.child_value("clear_cnt"))
            newprofile.replace_int("match_cnt", info.child_value("match_cnt"))
            newprofile.replace_int("beat_cnt", info.child_value("beat_cnt"))
            newprofile.replace_int("mynews_cnt", info.child_value("mynews_cnt"))

            newprofile.replace_int("bonus_tune_points", info.child_value("bonus_tune_points"))
            newprofile.replace_bool("is_bonus_tune_played", info.child_value("is_bonus_tune_played"))

        # Grab last settings
        lastnode = player.child("last")
        if lastnode is not None:
            last.replace_int("expert_option", lastnode.child_value("expert_option"))
            last.replace_int("sort", lastnode.child_value("sort"))
            last.replace_int("category", lastnode.child_value("category"))

            settings = lastnode.child("settings")
            if settings is not None:
                last.replace_int("matching", settings.child_value("matching"))
                last.replace_int("hazard", settings.child_value("hazard"))
                last.replace_int("hard", settings.child_value("hard"))
                last.replace_int("marker", settings.child_value("marker"))
                last.replace_int("theme", settings.child_value("theme"))
                last.replace_int("title", settings.child_value("title"))
                last.replace_int("parts", settings.child_value("parts"))
                last.replace_int("rank_sort", settings.child_value("rank_sort"))
                last.replace_int("combo_disp", settings.child_value("combo_disp"))
                last.replace_int_array("emblem", 5, settings.child_value("emblem"))

        # Grab unlock progress
        item = player.child("item")
        if item is not None:
            newprofile.replace_int_array("music_list", 64, item.child_value("music_list"))
            newprofile.replace_int_array("theme_list", 16, item.child_value("theme_list"))
            newprofile.replace_int_array("marker_list", 16, item.child_value("marker_list"))
            newprofile.replace_int_array("title_list", 160, item.child_value("title_list"))
            newprofile.replace_int_array("parts_list", 160, item.child_value("parts_list"))
            newprofile.replace_int_array("commu_list", 16, item.child_value("commu_list"))

            if not force_unlock:
                # Don't persist if we're force-unlocked, this data will be bogus.
                owned_songs = self.calculate_owned_items(item.child_value("secret_list"))
                for index in owned_songs:
                    self.data.local.user.put_achievement(
                        self.game,
                        self.version,
                        userid,
                        index,
                        "song",
                        {},
                    )

            owned_emblems = self.calculate_owned_items(item.child_value("emblem_list"))
            for index in owned_emblems:
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    index,
                    "emblem",
                    {},
                )

            newitem = item.child("new")
            if newitem is not None:
                newprofile.replace_int_array("theme_list_new", 16, newitem.child_value("theme_list"))
                newprofile.replace_int_array("marker_list_new", 16, newitem.child_value("marker_list"))

                if not force_unlock:
                    # Don't persist if we're force-unlocked, this data will be bogus.
                    owned_secrets = self.calculate_owned_items(newitem.child_value("secret_list"))
                    for index in owned_secrets:
                        self.data.local.user.put_achievement(
                            self.game,
                            self.version,
                            userid,
                            index,
                            "secret",
                            {},
                        )

        # Grab categories stuff
        fill_in_category = player.child("fill_in_category")
        if fill_in_category is not None:
            newprofile.replace_int_array(
                "no_gray_flag_list",
                16,
                fill_in_category.child_value("no_gray_flag_list"),
            )
            newprofile.replace_int_array(
                "all_yellow_flag_list",
                16,
                fill_in_category.child_value("all_yellow_flag_list"),
            )
            newprofile.replace_int_array(
                "full_combo_flag_list",
                16,
                fill_in_category.child_value("full_combo_flag_list"),
            )
            newprofile.replace_int_array(
                "excellent_flag_list",
                16,
                fill_in_category.child_value("excellent_flag_list"),
            )

        # jbox stuff
        jbox = player.child("jbox")
        jboxdict = newprofile.get_dict("jbox")
        if jbox is not None:
            jboxdict.replace_int("point", jbox.child_value("point"))
            emblemtype = jbox.child_value("emblem/type")
            index = jbox.child_value("emblem/index")
            if emblemtype == self.JBOX_EMBLEM_NORMAL:
                jboxdict.replace_int("normal_index", index)
            elif emblemtype == self.JBOX_EMBLEM_PREMIUM:
                jboxdict.replace_int("premium_index", index)
        newprofile.replace_dict("jbox", jboxdict)

        # Team stuff
        team = player.child("team")
        teamdict = newprofile.get_dict("team")
        if team is not None:
            teamdict.replace_int("id", int(team.attribute("id")))
            teamdict.replace_int("section", team.child_value("section"))
            teamdict.replace_int("street", team.child_value("street"))
            teamdict.replace_int("house_1", team.child_value("house_number_1"))
            teamdict.replace_int("house_2", team.child_value("house_number_2"))
        newprofile.replace_dict("team", teamdict)

        # Drop list
        drop_list = player.child("drop_list")
        if drop_list is not None:
            for drop in drop_list.children:
                try:
                    dropid = int(drop.attribute("id"))
                except TypeError:
                    # Unrecognized drop
                    continue
                exp = drop.child_value("exp")
                flag = drop.child_value("flag")
                items: Dict[int, int] = {}

                item_list = drop.child("item_list")
                if item_list is not None:
                    for item in item_list.children:
                        try:
                            itemid = int(item.attribute("id"))
                        except TypeError:
                            # Unrecognized item
                            continue
                        items[itemid] = item.child_value("num")

                olddrop = self.data.local.user.get_achievement(
                    self.game,
                    self.version,
                    userid,
                    dropid,
                    "drop",
                )

                if olddrop is None:
                    # Create a new event structure for this
                    olddrop = ValidatedDict()

                olddrop.replace_int("exp", exp)
                olddrop.replace_int("flag", flag)
                for itemid, num in items.items():
                    olddrop.replace_int(f"item_{itemid}", num)

                # Save it as an achievement
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    dropid,
                    "drop",
                    olddrop,
                )

        # event stuff
        newprofile.replace_int("event_flag", player.child_value("event_flag"))
        event_info = player.child("event_info")
        if event_info is not None:
            for child in event_info.children:
                try:
                    eventid = int(child.attribute("type"))
                except TypeError:
                    # Event is empty
                    continue
                is_completed = child.child_value("is_completed")

                # Figure out if we should update the rating/scores or not
                oldevent = self.data.local.user.get_achievement(
                    self.game,
                    self.version,
                    userid,
                    eventid,
                    "event",
                )

                if oldevent is None:
                    # Create a new event structure for this
                    oldevent = ValidatedDict()

                oldevent.replace_bool("is_completed", is_completed)

                # Save it as an achievement
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    eventid,
                    "event",
                    oldevent,
                )

        # Still don't know what this is for lol
        newprofile.replace_int("navi_flag", player.child_value("navi/flag"))

        # Grab scores and save those
        if result is not None:
            for tune in result.children:
                if tune.name != "tune":
                    continue
                result = tune.child("player")

                # Fix mapping to song IDs for the song with seven billion charts
                # due to the prefecture unlock event.
                songid = tune.child_value("music")
                if songid in self.FIVE_PLAYS_UNLOCK_EVENT_SONG_IDS:
                    songid = 80000301

                timestamp = tune.child_value("timestamp") / 1000
                chart = int(result.child("score").attribute("seq"))
                points = result.child_value("score")
                flags = int(result.child("score").attribute("clear"))
                combo = int(result.child("score").attribute("combo"))
                ghost = result.child_value("mbar")

                stats = {
                    "perfect": result.child_value("nr_perfect"),
                    "great": result.child_value("nr_great"),
                    "good": result.child_value("nr_good"),
                    "poor": result.child_value("nr_poor"),
                    "miss": result.child_value("nr_miss"),
                }

                # Miscelaneous last data for echoing to profile get
                last.replace_int("music_id", songid)
                last.replace_int("seq_id", chart)

                mapping = {
                    self.GAME_FLAG_BIT_CLEARED: self.PLAY_MEDAL_CLEARED,
                    self.GAME_FLAG_BIT_FULL_COMBO: self.PLAY_MEDAL_FULL_COMBO,
                    self.GAME_FLAG_BIT_EXCELLENT: self.PLAY_MEDAL_EXCELLENT,
                    self.GAME_FLAG_BIT_NEARLY_FULL_COMBO: self.PLAY_MEDAL_NEARLY_FULL_COMBO,
                    self.GAME_FLAG_BIT_NEARLY_EXCELLENT: self.PLAY_MEDAL_NEARLY_EXCELLENT,
                }

                # Figure out the highest medal based on bits passed in
                medal = self.PLAY_MEDAL_FAILED
                for bit in mapping:
                    if flags & bit > 0:
                        medal = max(medal, mapping[bit])

                self.update_score(userid, timestamp, songid, chart, points, medal, combo, ghost, stats)

        # Born stuff
        born = player.child("born")
        if born is not None:
            newprofile.replace_int("born_status", born.child_value("status"))
            newprofile.replace_int("born_year", born.child_value("year"))

        # Save jubility
        jubility = player.child("jubility")
        if jubility is not None:
            newprofile.replace_int("jubility", int(jubility.attribute("param")))
            target_music_list = jubility.child("target_music_list")
            if target_music_list is not None:
                for target_music in target_music_list.children:
                    if target_music.name != "target_music":
                        continue

                    songid = target_music.child_value("music_id")
                    chart = target_music.child_value("seq")
                    score = target_music.child_value("score")
                    value = target_music.child_value("value")
                    hard_mode = target_music.child_value("is_hard_mode")

                    # Update jubility value tracking
                    oldjubility = self.data.local.user.get_achievement(
                        self.game,
                        self.version,
                        userid,
                        songid,
                        "jubility",
                    )

                    if oldjubility is None:
                        # Create a new jubility structure for this
                        oldjubility = ValidatedDict()

                    # Grab the entry for this sequence
                    entry = oldjubility.get_dict(str(chart))
                    if value >= entry.get_int("value"):
                        entry.replace_int("score", score)
                        entry.replace_int("value", value)
                        entry.replace_bool("hard_mode", hard_mode)
                    oldjubility.replace_dict(str(chart), entry)

                    # Save it as an achievement
                    self.data.local.user.put_achievement(
                        self.game,
                        self.version,
                        userid,
                        songid,
                        "jubility",
                        oldjubility,
                    )

        # Clan course saving
        clan_course_list = player.child("clan_course_list")
        if clan_course_list is not None:
            for course in clan_course_list.children:
                if course.name != "clan_course":
                    continue

                courseid = int(course.attribute("id"))
                status = course.child_value("status")
                is_seen = (status & self.COURSE_STATUS_SEEN) != 0
                is_played = (status & self.COURSE_STATUS_PLAYED) != 0

                # Update seen status and played status
                oldcourse = self.data.local.user.get_achievement(
                    self.game,
                    self.version,
                    userid,
                    courseid,
                    "course",
                )

                if oldcourse is None:
                    # Create a new course structure for this
                    oldcourse = ValidatedDict()

                oldcourse.replace_bool("seen", oldcourse.get_bool("seen") or is_seen)
                oldcourse.replace_bool("played", oldcourse.get_bool("played") or is_played)

                # Save it as an achievement
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    courseid,
                    "course",
                    oldcourse,
                )

        select_course = player.child("select_course")
        if select_course is not None:
            try:
                courseid = int(select_course.attribute("id"))
            except Exception:
                courseid = 0
            cleared = select_course.child_value("is_cleared")

            if courseid > 0 and cleared:
                # Update course cleared status
                oldcourse = self.data.local.user.get_achievement(
                    self.game,
                    self.version,
                    userid,
                    courseid,
                    "course",
                )

                if oldcourse is None:
                    # Create a new course structure for this
                    oldcourse = ValidatedDict()

                oldcourse.replace_bool("cleared", True)

                # Save it as an achievement
                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    courseid,
                    "course",
                    oldcourse,
                )

        # Save back last information gleaned from results
        newprofile.replace_dict("last", last)

        # Keep track of play statistics
        self.update_play_statistics(userid)

        return newprofile
