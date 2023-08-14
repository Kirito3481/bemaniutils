# vim: set fileencoding=utf-8
from typing import Any, Dict, List, Optional, Set, Tuple
from typing_extensions import Final
from bemani.backend.jubeat.base import JubeatBase
from bemani.backend.jubeat.common import (
    JubeatDemodataGetHitchartHandler,
    JubeatDemodataGetNewsHandler,
    JubeatGamendRegisterHandler,
    JubeatGametopGetMeetingHandler,
    JubeatLobbyCheckHandler,
    JubeatLoggerReportHandler
)
from bemani.backend.jubeat.festo import JubeatFesto

from bemani.backend.base import Status
from bemani.common import Profile, Time, ValidatedDict, VersionConstants
from bemani.data import Score, UserID
from bemani.protocol import Node


class JubeatAvenue(
        JubeatDemodataGetHitchartHandler,
        JubeatDemodataGetNewsHandler,
        JubeatGamendRegisterHandler,
        JubeatGametopGetMeetingHandler,
        JubeatLobbyCheckHandler,
        JubeatLoggerReportHandler,
        JubeatBase):
    name: str = "Jubeat Avenue"
    version: int = VersionConstants.JUBEAT_AVENUE

    JBOX_EMBLEM_NORMAL: Final[int] = 1
    JBOX_EMBLEM_PREMIUM: Final[int] = 2

    GAME_CHART_TYPE_BASIC: Final[int] = 0
    GAME_CHART_TYPE_ADVANCED: Final[int] = 1
    GAME_CHART_TYPE_EXTREME: Final[int] = 2

    def previous_version(self) -> Optional[JubeatBase]:
        return JubeatFesto(self.data, self.config, self.model)

    def game_to_db_chart(self, game_chart: int, hard_mode: bool) -> int:
        if hard_mode:
            return {
                self.GAME_CHART_TYPE_BASIC: self.CHART_TYPE_HARD_BASIC,
                self.GAME_CHART_TYPE_ADVANCED: self.CHART_TYPE_HARD_ADVANCED,
                self.GAME_CHART_TYPE_EXTREME: self.CHART_TYPE_HARD_EXTREME,
            }[game_chart]
        else:
            return {
                self.GAME_CHART_TYPE_BASIC: self.CHART_TYPE_BASIC,
                self.GAME_CHART_TYPE_ADVANCED: self.CHART_TYPE_ADVANCED,
                self.GAME_CHART_TYPE_EXTREME: self.CHART_TYPE_EXTREME,
            }[game_chart]

    def db_to_game_chart(self, db_chart: int) -> int:
        return {
            self.CHART_TYPE_BASIC: self.GAME_CHART_TYPE_BASIC,
            self.CHART_TYPE_ADVANCED: self.GAME_CHART_TYPE_ADVANCED,
            self.CHART_TYPE_EXTREME: self.GAME_CHART_TYPE_EXTREME,
            self.CHART_TYPE_HARD_BASIC: self.GAME_CHART_TYPE_BASIC,
            self.CHART_TYPE_HARD_ADVANCED: self.GAME_CHART_TYPE_ADVANCED,
            self.CHART_TYPE_HARD_EXTREME: self.GAME_CHART_TYPE_EXTREME,
        }[db_chart]

    def __get_lightchat_list(self) -> List[Dict[str, Any]]:
        class RewardType:
            Music: Final[int] = 1
            Title: Final[int] = 2
            Parts: Final[int] = 10
            BonusTuneGauge: Final[int] = 11

        class MissionType:
            CategorySongPlay: Final[int] = 1
            PlaySongWithCondition: Final[int] = 2
            PlaySong: Final[int] = 3
            LevelScore: Final[int] = 6
            LevelCombo: Final[int] = 7
            MatchingSelect: Final[int] = 8
            RandomSelect: Final[int] = 9
            DailyFirstPlay: Final[int] = 12

        class BonusType:
            JWATT: Final[int] = 1
            L: Final[int] = 2

        return [
            {
                "id": 1,
                "events": [
                    # SMITH
                    {
                        "id": 1,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "なし",
                        "unlock_text": "なし",
                        "conditions": [],
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "00ec00",
                                "required_jwatt": 10,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000011,
                                "dialogue": "jubeat Ave.へようこそ！",
                                "missions": []
                            }
                        ]
                    },

                    # MARINE
                    {
                        "id": 2,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "SMITH解禁",
                        "unlock_text": "SMITHと心が通じあった",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [{
                                    "id": 1,
                                    "condition_type": 1,
                                    "params": [1, 0, 0],
                                    "precondition_ids": [0]
                                }]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "03b700",
                                "required_jwatt": 500,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13572,
                                "dialogue": "暑いね~",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 100
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "09e6c0",
                                "required_jwatt": 2000,
                                "reward_type": RewardType.Title,
                                "reward_param": 7995,
                                "dialogue": "こんな日はソーダが飲みたいよ",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 3
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "3b76d0",
                                "required_jwatt": 1450,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000021,
                                "dialogue": "え！？くれるの？ありがとう！",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 750
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [6, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 4
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 600
                                    },
                                ]
                            },
                        ]
                    },

                    # MET
                    {
                        "id": 3,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "Clear SMITH",
                        "unlock_text": "SMITHと心が通じあった",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [{
                                    "id": 1,
                                    "condition_type": 1,
                                    "params": [1, 0, 0],
                                    "precondition_ids": [0]
                                }]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "036d00",
                                "required_jwatt": 500,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13573,
                                "dialogue": "あわわわわ",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 100
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 600
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "067ec0",
                                "required_jwatt": 2000,
                                "reward_type": RewardType.Title,
                                "reward_param": 7994,
                                "dialogue": "地面を掘ってたらなんか出てきた！",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [3, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 3
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "1bdbb0",
                                "required_jwatt": 1450,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000002,
                                "dialogue": "なーんだ。お面か。キミにあげる",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 750
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [3, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 4
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 600
                                    },
                                ]
                            },
                        ]
                    },

                    # GAU
                    {
                        "id": 4,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "Clear MARINE",
                        "unlock_text": "MARINEと心が通じあった",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [{
                                    "id": 1,
                                    "condition_type": 1,
                                    "params": [2, 0, 0],
                                    "precondition_ids": [0]
                                }]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "01db00",
                                "required_jwatt": 600,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13574,
                                "dialogue": "うーん",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [11000021, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySong,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "39b6f0",
                                "required_jwatt": 6000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "うーーん",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [3, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [11, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "07b780",
                                "required_jwatt": 1000,
                                "reward_type": RewardType.Title,
                                "reward_param": 7996,
                                "dialogue": "うーーーん",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 750
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [2, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "f9e7dc",
                                "required_jwatt": 1200,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000010,
                                "dialogue": "ゴメン気づかなかった、どうして夜が暗いか考えていたんだ",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [4, 900000, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelScore,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                        ]
                    },

                    # CAPELI
                    {
                        "id": 5,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "Clear MARINE",
                        "unlock_text": "MARINEと心が通じあった",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [{
                                    "id": 1,
                                    "condition_type": 1,
                                    "params": [2, 0, 0],
                                    "precondition_ids": [0]
                                }]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "01db00",
                                "required_jwatt": 600,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13575,
                                "dialogue": "ようこそ！",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [11000021, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySong,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "39b6f0",
                                "required_jwatt": 6000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "紫の花ばっかりだねって？",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [2, 100, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelCombo,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [14, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "07b780",
                                "required_jwatt": 1000,
                                "reward_type": RewardType.Title,
                                "reward_param": 7997,
                                "dialogue": "それはね…",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [3, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "f9e7dc",
                                "required_jwatt": 1200,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000005,
                                "dialogue": "キミもそのうち分かる日が来るよ",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [5, 850000, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelScore,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                        ]
                    },

                    # HUNG
                    {
                        "id": 6,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "Clear MET",
                        "unlock_text": "METと心が通じあった",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [{
                                    "id": 1,
                                    "condition_type": 1,
                                    "params": [3, 0, 0],
                                    "precondition_ids": [0]
                                }]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "01db00",
                                "required_jwatt": 600,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13576,
                                "dialogue": "... (I'm not suspicious at all)",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [11000002, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySong,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "39b6f0",
                                "required_jwatt": 6000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "... (Why do I have a sickle?)",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [6, 100, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelCombo,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [11, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "07b780",
                                "required_jwatt": 1000,
                                "reward_type": RewardType.Title,
                                "reward_param": 7998,
                                "dialogue": "... (I was asked to mow the grass)",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [4, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "f9e7dc",
                                "required_jwatt": 1200,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000020,
                                "dialogue": "... (Will you be Tomotachi?)",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [2, 950000, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelScore,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                        ]
                    },

                    # STRAW
                    {
                        "id": 7,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "Clear MET",
                        "unlock_text": "METと心が通じあった",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [{
                                    "id": 1,
                                    "condition_type": 1,
                                    "params": [3, 0, 0],
                                    "precondition_ids": [0]
                                }]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "01db00",
                                "required_jwatt": 600,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13577,
                                "dialogue": "Welcome!",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [11000002, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySong,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "39b6f0",
                                "required_jwatt": 6000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "Perfect for this season!",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [4, 200, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelCombo,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [12, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "07b780",
                                "required_jwatt": 1000,
                                "reward_type": RewardType.Title,
                                "reward_param": 7999,
                                "dialogue": "I's not strawberry",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [7, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "f9e7dc",
                                "required_jwatt": 1200,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000003,
                                "dialogue": "If you don't mind, go ahead!",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [2, 980000, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.LevelScore,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                        ]
                    },

                    # BONNY
                    {
                        "id": 8,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "Let's clear the thank you song from HUNG and STRAW",
                        "unlock_text": "Clear the 2 title songs and achieve jubility 2,000",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [6, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 1,
                                        "params": [7, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 3,
                                        "condition_type": 3,
                                        "params": [11000020, 5, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 4,
                                        "condition_type": 3,
                                        "params": [11000003, 5, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 5,
                                        "condition_type": 6,
                                        "params": [20000, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                ]
                            }
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "0e7980",
                                "required_jwatt": 1500,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13578,
                                "dialogue": "How can I help you?",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [14, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "3b7b70",
                                "required_jwatt": 2000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "Then to the right there",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "6e7edc",
                                "required_jwatt": 7200,
                                "reward_type": RewardType.Title,
                                "reward_param": 8000,
                                "dialogue": "What? Are they different?",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [15, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 6
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "0de9c0",
                                "required_jwatt": 1000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "Actually, I have no sense of direction",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 200
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [26, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 5,
                                "tube_text": "edddbc",
                                "required_jwatt": 1800,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000013,
                                "dialogue": "Please come this way as an apology",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 400
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [12, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 400
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                        ]
                    },

                    # SUNVA
                    {
                        "id": 9,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "I think there's something good about connecting zigzags",
                        "unlock_text": "Achieve jubility 3,000 and play ZIGZAG COWBOY full combo or 100 TUNES",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [4, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 6,
                                        "params": [30000, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 3,
                                        "condition_type": 4,
                                        "params": [10000010, 5, 0],
                                        "precondition_ids": [0]
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [4, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 6,
                                        "params": [30000, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 3,
                                        "condition_type": 7,
                                        "params": [100, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                ]
                            },
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "0e7980",
                                "required_jwatt": 1500,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13579,
                                "dialogue": "hey hey",
                                # 부스트 미션
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [12, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "3b7b70",
                                "required_jwatt": 2000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "ワンチャンあると思う？",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [4, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "6e7edc",
                                "required_jwatt": 7250,
                                "reward_type": RewardType.Title,
                                "reward_param": 8001,
                                "dialogue": "脈ありですか？マジですか？",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [50000038, 5, 980000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 6
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "0de9c0",
                                "required_jwatt": 1500,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "Actually, I have no sense of direction",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 200
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [25, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                            {
                                "id": 5,
                                "tube_text": "edddbc",
                                "required_jwatt": 2500,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000004,
                                "dialogue": "リベンジ全開~ッ！",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 400
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [13, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 400
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 150
                                    },
                                ]
                            },
                        ]
                    },
                ]
            },

            # Concierge
            {
                "id": 99,
                "events": [
                    {
                        "id": 1,
                        "event_type": 3,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "なし",
                        "unlock_text": "なし",
                        "conditions": [],
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "0e7640",
                                "required_jwatt": 300,
                                "reward_type": 11,
                                "reward_param": 100,
                                "dialogue": "This way, please！",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [56, 0, 0],
                                        "repeatable": True,
                                        "mission_type": 1,
                                        "bonus_type": 1,
                                        "bonus_param": 100
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

    def __get_global_info(self) -> Node:
        info = Node.void("info")
# region
        # Event info.
        event_info = Node.void("event_info")
        info.add_child(event_info)

        # Share music.
        share_music = Node.void("share_music")
        info.add_child(share_music)

        # Genre default music.
        genre_def_music = Node.void("genre_def_music")
        info.add_child(genre_def_music)

        info.add_child(Node.s32_array("black_jacket_list", [0] * 64))

        # Weekly music.
        weekly_music = Node.void("weekly_music")
        info.add_child(weekly_music)

        info.add_child(Node.s32_array("white_music_list", [-1] * 64))

        info.add_child(Node.s32_array("white_marker_list", [-1] * 16))

        info.add_child(Node.s32_array("white_theme_list", [-1] * 16))

        info.add_child(Node.s32_array("add_default_music_list", [0] * 64))

        info.add_child(Node.s32_array("open_music_list", [0] * 64))

        info.add_child(Node.s32_array("shareable_music_list", [0] * 64))

        info.add_child(Node.s32_array("inf_ojisan_music_list", [0] * 64))

        info.add_child(Node.s32_array("hot_music_list", [0] * 64))

        jbox = Node.void("jbox")
        info.add_child(jbox)
        jbox.add_child(Node.s32("point", 0))
        emblem = Node.void("emblem")
        jbox.add_child(emblem)
        normal = Node.void("normal")
        emblem.add_child(normal)
        premium = Node.void("premium")
        emblem.add_child(premium)
        normal.add_child(Node.s16("index", 2))
        premium.add_child(Node.s16("index", 1))

        born = Node.void("born")
        info.add_child(born)
        born.add_child(Node.s8("status", 1))

        expert_option = Node.void("expert_option")
        info.add_child(expert_option)
        expert_option.add_child(Node.bool("is_available", True))

        game_config = self.get_game_config()

        konami_logo_50th = Node.void("konami_logo_50th")
        info.add_child(konami_logo_50th)
        konami_logo_50th.add_child(
            Node.bool("is_available", game_config.get_bool("50th_anniversary"))
        )

        all_music_matching = Node.void("all_music_matching")
        info.add_child(all_music_matching)
        all_music_matching.add_child(Node.bool("is_available", True))

        question_list = Node.void("question_list")
        info.add_child(question_list)

        department = Node.void("department")
        info.add_child(department)
        department.add_child(Node.void("shop_list"))

        team_battle = Node.void("team_battle")
        info.add_child(team_battle)

        qr = Node.void("qr")
        info.add_child(qr)
        qr.add_child(Node.s32("flag", 0))

        course_list = Node.void("course_list")
        info.add_child(course_list)

        # emo_list = Node.void("emo_list")
        # info.add_child(emo_list)

        hike_event = Node.void("hike_event")
        info.add_child(hike_event)

        tip_list = Node.void("tip_list")
        info.add_child(tip_list)

        if game_config.get_bool("festo_dungeon"):
            festo_dungeon = Node.void("festo_dungeon")
            info.add_child(festo_dungeon)
            festo_dungeon.add_child(
                Node.u64("etime", (Time.now() + Time.SECONDS_IN_WEEK) * 1000)
            )

        travel = Node.void("travel")
        info.add_child(travel)

        lightchat = Node.void("lightchat")
        info.add_child(lightchat)
        map_list = Node.void("map_list")
        lightchat.add_child(map_list)
# endregion
        for map in self.__get_lightchat_list():
            mapnode = Node.void("map")
            map_list.add_child(mapnode)
            mapnode.set_attribute("id", str(map['id']))

            event_list = Node.void("event_list")
            mapnode.add_child(event_list)

            if "events" in map:
                for event in map['events']:
                    eventnode = Node.void("event")
                    event_list.add_child(eventnode)
                    eventnode.set_attribute("id", str(event['id']))
                    eventnode.add_child(
                        Node.s32("event_type", event['event_type']))
                    eventnode.add_child(Node.u64("stime", event['start_time']))
                    eventnode.add_child(Node.u64("etime", event['end_time']))
                    eventnode.add_child(Node.bool("is_open", event['is_open']))
                    eventnode.add_child(Node.string("hint", event['hint']))
                    eventnode.add_child(
                        Node.string("unlock_text", event['unlock_text']))

                    condition_list = Node.void("condition_list")
                    eventnode.add_child(condition_list)

                    if "conditions" in event:
                        for condition in event['conditions']:
                            conditionnode = Node.void("condition")
                            condition_list.add_child(conditionnode)
                            conditionnode.set_attribute(
                                "id", str(condition['id']))

                            if "conditions" in condition:
                                for condition2 in condition['conditions']:
                                    conditionnode2 = Node.void("condition")
                                    conditionnode.add_child(conditionnode2)
                                    conditionnode2.set_attribute(
                                        "id", str(condition2['id']))
                                    conditionnode2.add_child(
                                        Node.s32("condition_type", condition2['condition_type']))
                                    conditionnode2.add_child(
                                        Node.s32_array("param_list", condition2['params']))
                                    conditionnode2.add_child(
                                        Node.s32_array("precondition_id_list", condition2['precondition_ids']))

                    section_list = Node.void("section_list")
                    eventnode.add_child(section_list)

                    if "sections" in event:
                        for section in event['sections']:
                            sectionnode = Node.void("section")
                            section_list.add_child(sectionnode)
                            sectionnode.set_attribute("id", str(section['id']))

                            sectionnode.add_child(Node.string(
                                "tube_text", section['tube_text']))
                            sectionnode.add_child(
                                Node.s32("required_jwatt", section['required_jwatt']))
                            sectionnode.add_child(
                                Node.s32("reward_type", section['reward_type']))
                            sectionnode.add_child(
                                Node.s32("reward_param", section['reward_param']))
                            sectionnode.add_child(Node.string(
                                "dialogue", section['dialogue']))

                            mission_list = Node.void("mission_list")
                            sectionnode.add_child(mission_list)

                            if "missions" in section:
                                for mission in section['missions']:
                                    missionnode = Node.void("mission")
                                    mission_list.add_child(missionnode)
                                    missionnode.set_attribute(
                                        "id", str(mission['id']))

                                    missionnode.add_child(Node.s32_array(
                                        "mission_param_list", mission['mission_params']))
                                    missionnode.add_child(
                                        Node.bool("repeatable", mission['repeatable']))
                                    missionnode.add_child(
                                        Node.s32("mission_type", mission['mission_type']))
                                    missionnode.add_child(
                                        Node.s32("bonus_type", mission['bonus_type']))
                                    missionnode.add_child(
                                        Node.s32("bonus_param", mission['bonus_param']))

        stamp = Node.void("stamp")
        info.add_child(stamp)

        return info

    def handle_shopinfo_ave_regist_request(self, request: Node) -> Node:
        self.update_machine_name(request.child_value("shop/name"))

        shopinfo = Node.void("shopinfo_ave")

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

    def handle_demodata_ave_get_info_request(self, request: Node) -> Node:
        root = Node.void("demodata_ave")
        data = Node.void("data")
        root.add_child(data)

        info = Node.void("info")
        data.add_child(info)

        info.add_child(Node.s32_array("black_jacket_list", [0] * 64))

        return root

    def handle_demodata_ave_get_jbox_list_request(self, request: Node) -> Node:
        root = Node.void("demodata_ave")
        selection_list = Node.void("selection_list")
        root.add_child(selection_list)

        return root

    def handle_jbox_ave_get_agreement_request(self, request: Node) -> Node:
        root = Node.void("jbox_ave")
        root.add_child(Node.bool("is_agreement", True))
        return root

    def handle_jbox_ave_get_list_request(self, request: Node) -> Node:
        root = Node.void("jbox_ave")
        root.add_child(Node.void("selection_list"))
        return root

    def handle_recommend_ave_get_recommend_request(self, request: Node) -> Node:
        root = Node.void("recommend_ave")
        data = Node.void("data")
        root.add_child(data)

        player = Node.void("player")
        data.add_child(player)
        music_list = Node.void("music_list")
        player.add_child(music_list)

        return root

    def handle_gametop_ave_get_info_request(self, request: Node) -> Node:
        root = Node.void("gametop")
        data = Node.void("data")
        root.add_child(data)
        data.add_child(self.__get_global_info())

        return root

    def handle_gametop_ave_regist_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")
        refid = player.child_value("refid")
        name = player.child_value("name")

        root = self.new_profile_by_refid(refid, name)

        return root

    def handle_gametop_ave_get_pdata_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")
        refid = player.child_value("refid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("gametop")
            root.set_attribute("status", str(Status.NO_PROFILE))
        return root

    def handle_gametop_ave_get_mdata_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")
        extid = player.child_value("jid")
        mdata_ver = player.child_value(
            "mdata_ver"
        )  # Game requests mdata 3 times per profile for some reason
        if mdata_ver != 1:
            root = Node.void("gametop_ave")
            datanode = Node.void("data")
            root.add_child(datanode)
            player = Node.void("player")
            datanode.add_child(player)
            player.add_child(Node.s32("jid", extid))
            playdata = Node.void("mdata_list")
            player.add_child(playdata)
            return root
        root = self.get_scores_by_extid(extid)
        if root is None:
            root = Node.void("gametop_ave")
            root.set_attribute("status", str(Status.NO_PROFILE))
        return root

    def handle_gameend_ave_final_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")

        if player is not None:
            refid = player.child_value("refid")
        else:
            refid = None

        if refid is not None:
            userid = self.data.remote.user.from_refid(
                self.game, self.version, refid)
        else:
            userid = None

        if userid is not None:
            profile = self.get_profile(userid)

            # Grab unlock progress
            item = player.child("item")
            if item is not None:
                owned_emblems = self.calculate_owned_items(
                    item.child_value("emblem_list")
                )
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

        return Node.void("gameend_ave")

    def format_scores(self, userid: UserID, profile: Profile, scores: List[Score]) -> Node:
        root = Node.void("gametop_ave")
        datanode = Node.void("data")
        root.add_child(datanode)
        player = Node.void("player")
        datanode.add_child(player)
        player.add_child(Node.s32("jid", profile.extid))
        playdata = Node.void("mdata_list")
        player.add_child(playdata)

        music = ValidatedDict()
        for score in scores:
            chart = self.db_to_game_chart(score.chart)
            if score.chart in {
                self.CHART_TYPE_HARD_BASIC,
                self.CHART_TYPE_HARD_ADVANCED,
                self.CHART_TYPE_HARD_EXTREME,
            }:
                prefix = "hard"
            else:
                prefix = "normal"

            data = music.get_dict(str(score.id))
            play_cnt = data.get_int_array(f"{prefix}_play_cnt", 3)
            clear_cnt = data.get_int_array(f"{prefix}_clear_cnt", 3)
            clear_flags = data.get_int_array(f"{prefix}_clear_flags", 3)
            fc_cnt = data.get_int_array(f"{prefix}_fc_cnt", 3)
            ex_cnt = data.get_int_array(f"{prefix}_ex_cnt", 3)
            points = data.get_int_array(f"{prefix}_points", 3)
            music_rate = data.get_int_array(f"{prefix}_music_rate", 3)

            play_cnt[chart] = score.plays
            clear_cnt[chart] = score.data.get_int("clear_count")
            fc_cnt[chart] = score.data.get_int("full_combo_count")
            ex_cnt[chart] = score.data.get_int("excellent_count")
            points[chart] = score.points
            music_rate[chart] = score.data.get_int("music_rate")

            clear_flags[chart] = self.GAME_FLAG_BIT_PLAYED
            if score.data.get_int("clear_count") > 0:
                clear_flags[chart] |= self.GAME_FLAG_BIT_CLEARED
            if score.data.get_int("full_combo_count") > 0:
                clear_flags[chart] |= self.GAME_FLAG_BIT_FULL_COMBO
            if score.data.get_int("excellent_count") > 0:
                clear_flags[chart] |= self.GAME_FLAG_BIT_EXCELLENT

            data.replace_int_array(f"{prefix}_play_cnt", 3, play_cnt)
            data.replace_int_array(f"{prefix}_clear_cnt", 3, clear_cnt)
            data.replace_int_array(f"{prefix}_clear_flags", 3, clear_flags)
            data.replace_int_array(f"{prefix}_fc_cnt", 3, fc_cnt)
            data.replace_int_array(f"{prefix}_ex_cnt", 3, ex_cnt)
            data.replace_int_array(f"{prefix}_points", 3, points)
            data.replace_int_array(f"{prefix}_music_rate", 3, music_rate)

            ghost = data.get(f"{prefix}_ghost", [None, None, None])
            ghost[chart] = score.data.get("ghost")
            data[f"{prefix}_ghost"] = ghost

            music.replace_dict(str(score.id), data)

        for scoreid in music:
            scoredata = music.get_dict(scoreid)
            musicdata = Node.void("musicdata")
            playdata.add_child(musicdata)
            musicdata.set_attribute("music_id", scoreid)

            if scoredata.get_int_array("normal_play_cnt", 3) != [0, 0, 0]:
                normalnode = Node.void("normal")
                musicdata.add_child(normalnode)

                normalnode.add_child(Node.s32_array(
                    "play_cnt", scoredata.get_int_array("normal_play_cnt", 3)))
                normalnode.add_child(Node.s32_array(
                    "clear_cnt", scoredata.get_int_array("normal_clear_cnt", 3)))
                normalnode.add_child(Node.s32_array(
                    "fc_cnt", scoredata.get_int_array("normal_fc_cnt", 3)))
                normalnode.add_child(Node.s32_array(
                    "ex_cnt", scoredata.get_int_array("normal_ex_cnt", 3)))
                normalnode.add_child(Node.s32_array(
                    "score", scoredata.get_int_array("normal_points", 3)))
                normalnode.add_child(Node.s8_array(
                    "clear", scoredata.get_int_array("normal_clear_flags", 3)))
                normalnode.add_child(Node.s32_array(
                    "music_rate", scoredata.get_int_array("normal_music_rate", 3)))

                for i, ghost in enumerate(
                    scoredata.get("normal_ghost", [None, None, None])
                ):
                    if ghost is None:
                        continue

                    bar = Node.u8_array("bar", ghost)
                    normalnode.add_child(bar)
                    bar.set_attribute("seq", str(i))

            if scoredata.get_int_array("hard_play_cnt", 3) != [0, 0, 0]:
                hardnode = Node.void("hard")
                musicdata.add_child(hardnode)

                hardnode.add_child(Node.s32_array(
                    "play_cnt", scoredata.get_int_array("hard_play_cnt", 3)))
                hardnode.add_child(Node.s32_array(
                    "clear_cnt", scoredata.get_int_array("hard_clear_cnt", 3)))
                hardnode.add_child(Node.s32_array(
                    "fc_cnt", scoredata.get_int_array("hard_fc_cnt", 3)))
                hardnode.add_child(Node.s32_array(
                    "ex_cnt", scoredata.get_int_array("hard_ex_cnt", 3)))
                hardnode.add_child(Node.s32_array(
                    "score", scoredata.get_int_array("hard_points", 3)))
                hardnode.add_child(Node.s8_array(
                    "clear", scoredata.get_int_array("hard_clear_flags", 3)))
                hardnode.add_child(Node.s32_array(
                    "music_rate", scoredata.get_int_array("hard_music_rate", 3)))

                for i, ghost in enumerate(
                    scoredata.get("hard_ghost", [None, None, None])
                ):
                    if ghost is None:
                        continue

                    bar = Node.u8_array("bar", ghost)
                    hardnode.add_child(bar)
                    bar.set_attribute("seq", str(i))

        return root

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("gametop_ave")
        data = Node.void("data")
        root.add_child(data)

        game_config = self.get_game_config()
        force_unlock = game_config.get_bool("force_song_unlock")

        achievements = self.data.local.user.get_achievements(
            self.game, self.version, userid
        )
        owned_songs: Set[int] = set()
        owned_secrets: Set[int] = set()
        owned_emblems: Set[int] = set()
        event_completion: Dict[int, bool] = {}
        course_completion: Dict[int, ValidatedDict] = {}
        for achievement in achievements:
            if achievement.type == "event":
                event_completion[achievement.id] = achievement.data.get_bool(
                    "is_completed"
                )
            elif achievement.type == "course":
                course_completion[achievement.id] = achievement.data
            elif achievement.type == "emblem":
                owned_emblems.add(achievement.id)
            elif achievement.type == "song":
                owned_songs.add(achievement.id)
            elif achievement.type == "secret":
                owned_secrets.add(achievement.id)

        default_emblems = self.default_select_jbox()
        owned_emblems.update(default_emblems)
        default_main = next(iter(default_emblems)) if default_emblems else 0

        data.add_child(self.__get_global_info())

        player = Node.void("player")
        data.add_child(player)

        # Basic profile info
        player.add_child(Node.s32("jid", profile.extid))
        player.add_child(Node.s32("session_id", 1))
        player.add_child(Node.string(
            "name", profile.get_str("name", "PLAYER")))
        player.add_child(Node.u64("event_flag", profile.get_int("event_flag")))

        info = Node.void("info")
        player.add_child(info)
        info.add_child(
            Node.bool(
                "inherit",
                profile.get_bool(
                    "has_old_version") and not profile.get_bool("saved"),
            )
        )
        info.add_child(Node.s32("tune_cnt", profile.get_int("tune_cnt")))
        info.add_child(Node.s32("save_cnt", profile.get_int("save_cnt")))
        info.add_child(Node.s32("saved_cnt", profile.get_int("saved_cnt")))
        info.add_child(Node.s32("fc_cnt", profile.get_int("fc_cnt")))
        info.add_child(Node.s32("ex_cnt", profile.get_int("ex_cnt")))
        info.add_child(Node.s32("clear_cnt", profile.get_int("clear_cnt")))
        info.add_child(Node.s32("match_cnt", profile.get_int("match_cnt")))
        info.add_child(Node.s32("beat_cnt", profile.get_int("beat_cnt")))
        info.add_child(Node.s32("mynews_cnt", profile.get_int("mynews_cnt")))
        info.add_child(
            Node.s32("mtg_entry_cnt", profile.get_int("mtg_entry_cnt")))
        info.add_child(
            Node.s32("mtg_hold_cnt", profile.get_int("mtg_hold_cnt")))
        info.add_child(Node.u8("mtg_result", profile.get_int("mtg_result")))
        info.add_child(
            Node.s32("bonus_tune_points", profile.get_int("bonus_tune_points"))
        )
        info.add_child(
            Node.bool("is_bonus_tune_played",
                      profile.get_bool("is_bonus_tune_played"))
        )

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
        last.add_child(
            Node.s8("expert_option", lastdict.get_int("expert_option")))

        settings = Node.void("settings")
        last.add_child(settings)
        settings.add_child(Node.s8("marker", lastdict.get_int("marker")))
        settings.add_child(Node.s8("theme", lastdict.get_int("theme")))
        settings.add_child(Node.s16("title", lastdict.get_int("title")))
        settings.add_child(Node.s16("parts", lastdict.get_int("parts")))
        settings.add_child(Node.s8("rank_sort", lastdict.get_int("rank_sort")))
        settings.add_child(
            Node.s8("combo_disp", lastdict.get_int("combo_disp")))
        settings.add_child(
            Node.s32("target_type", lastdict.get_int("target_type")))
        partslist = lastdict.get_int_array(
            "emblem", 5, [0, default_main, 0, 0, 0])
        if partslist[1] == 0:
            partslist[1] = default_main
        settings.add_child(Node.s16_array("emblem", partslist))
        settings.add_child(Node.s8("matching", lastdict.get_int("matching")))
        settings.add_child(Node.s8("hard", lastdict.get_int("hard")))
        settings.add_child(Node.s8("hazard", lastdict.get_int("hazard")))

        item = Node.void("item")
        player.add_child(item)
        item.add_child(Node.s32_array(
            "music_list", profile.get_int_array("music_list", 64, [-1] * 64)))
        item.add_child(
            Node.s32_array(
                "secret_list",
                ([-1] * 64)
                if force_unlock
                else self.create_owned_items(owned_songs, 64),
            )
        )
        item.add_child(Node.s32_array("theme_list", ([-1] * 16)))
        item.add_child(Node.s32_array("marker_list", ([-1] * 16)))
        item.add_child(Node.s32_array("title_list", ([-1] * 160)))
        item.add_child(Node.s32_array("parts_list", ([-1] * 160)))
        item.add_child(
            Node.s32_array(
                "emblem_list", self.create_owned_items(owned_emblems, 96))
        )
        item.add_child(
            Node.s32_array(
                "commu_list", profile.get_int_array(
                    "commu_list", 16, [-1] * 16)
            )
        )

        new = Node.void("new")
        item.add_child(new)
        new.add_child(
            Node.s32_array(
                "secret_list",
                ([-1] * 64)
                if force_unlock
                else self.create_owned_items(owned_secrets, 64),
            )
        )
        new.add_child(
            Node.s32_array(
                "theme_list", profile.get_int_array(
                    "theme_list_new", 16, [-1] * 16)
            )
        )
        new.add_child(
            Node.s32_array(
                "marker_list", profile.get_int_array(
                    "marker_list_new", 16, [-1] * 16)
            )
        )

        rivallist = Node.void("rivallist")
        player.add_child(rivallist)

        lab_edit_seq = Node.void("lab_edit_seq")
        player.add_child(lab_edit_seq)
        lab_edit_seq.set_attribute("count", "0")

        entry = self.data.local.game.get_time_sensitive_settings(
            self.game, self.version, "fc_challenge"
        )
        if entry is None:
            entry = ValidatedDict()

        start_time, end_time = self.data.local.network.get_schedule_duration(
            "daily")
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
        today.add_child(
            Node.u8("state", 0x40 if len(today_attempts) > 0 else 0x0))
        whim = Node.void("whim")
        fc_challenge.add_child(whim)
        whim.add_child(Node.s32("music_id", entry.get_int("whim", -1)))
        whim.add_child(
            Node.u8("state", 0x40 if len(whim_attempts) > 0 else 0x0))

        official_news = Node.void("official_news")
        player.add_child(official_news)
        news_list = Node.void("news_list")
        official_news.add_child(news_list)

        history = Node.void("history")
        player.add_child(history)
        history.set_attribute("count", "0")

        free_first_play = Node.void("free_first_play")
        player.add_child(free_first_play)
        free_first_play.add_child(
            Node.bool("is_available", profile.get_bool("is_first_play", True)))

        event_info = Node.void("event_info")
        player.add_child(event_info)

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

        normalindex, premiumindex = self.random_select_jbox(owned_emblems)
        normal.add_child(Node.s16("index", normalindex))
        premium.add_child(Node.s16("index", premiumindex))

        new_music = Node.void("new_music")
        player.add_child(new_music)

        navi = Node.void("navi")
        player.add_child(navi)
        navi.add_child(Node.u64("flag", profile.get_int("navi_flag")))

        gift_list = Node.void("gift_list")
        player.add_child(gift_list)

        born = Node.void("born")
        player.add_child(born)
        born.add_child(Node.s8("status", profile.get_int("born_status", 3)))
        born.add_child(Node.s16("year", profile.get_int("born_year")))

        question_list = Node.void("question_list")
        player.add_child(question_list)

        server = Node.void("server")
        player.add_child(server)

        course_list = Node.void("course_list")
        player.add_child(course_list)

        category_list = Node.void("category_list")
        course_list.add_child(category_list)
        for categoryid in range(1, 7):
            category = Node.void("category")
            category_list.add_child(category)
            category.set_attribute("id", str(categoryid))
            category.add_child(Node.bool("is_display", True))

        fill_in_category = Node.void("fill_in_category")
        player.add_child(fill_in_category)

        normal = Node.void("normal")
        fill_in_category.add_child(normal)
        normal.add_child(
            Node.s32_array(
                "no_gray_flag_list",
                profile.get_int_array(
                    "normal_no_gray_flag_list", 16, [0] * 16),
            )
        )
        normal.add_child(
            Node.s32_array(
                "all_yellow_flag_list",
                profile.get_int_array(
                    "normal_all_yellow_flag_list", 16, [0] * 16),
            )
        )
        normal.add_child(
            Node.s32_array(
                "full_combo_flag_list",
                profile.get_int_array(
                    "normal_full_combo_flag_list", 16, [0] * 16),
            )
        )
        normal.add_child(
            Node.s32_array(
                "excellent_flag_list",
                profile.get_int_array(
                    "normal_excellent_flag_list", 16, [0] * 16),
            )
        )

        hard = Node.void("hard")
        fill_in_category.add_child(hard)
        hard.add_child(
            Node.s32_array(
                "no_gray_flag_list",
                profile.get_int_array("hard_no_gray_flag_list", 16, [0] * 16),
            )
        )
        hard.add_child(
            Node.s32_array(
                "all_yellow_flag_list",
                profile.get_int_array(
                    "hard_all_yellow_flag_list", 16, [0] * 16),
            )
        )
        hard.add_child(
            Node.s32_array(
                "full_combo_flag_list",
                profile.get_int_array(
                    "hard_full_combo_flag_list", 16, [0] * 16),
            )
        )
        hard.add_child(
            Node.s32_array(
                "excellent_flag_list",
                profile.get_int_array(
                    "hard_excellent_flag_list", 16, [0] * 16),
            )
        )

        eamuse_gift_list = Node.void("eamuse_gift_list")
        player.add_child(eamuse_gift_list)

        lightchat = Node.void("lightchat")
        player.add_child(lightchat)
        lightchat.add_child(
            Node.s32("current_map_id", profile.get_int("lightchat_current_map_id", -1)))
        lightchat.add_child(Node.s32("current_event_id",
                            profile.get_int("lightchat_current_event_id", -1)))

        map_list = Node.void("map_list")
        lightchat.add_child(map_list)

        for map in self.__get_lightchat_list():
            lightchat_map = self.data.local.user.get_achievement(
                self.game, self.version, userid, map['id'], "lightchat"
            )

            if lightchat_map is None:
                lightchat_map = ValidatedDict()

            mapnode = Node.void("map")
            map_list.add_child(mapnode)
            mapnode.set_attribute("id", str(map['id']))

            mapnode.add_child(
                Node.s32("tune_count", lightchat_map.get_int("tune_count")))
            mapnode.add_child(Node.u64("last_daily_bonus_time",
                              lightchat_map.get_int("last_daily_bonus_time")))

            event_list = Node.void("event_list")
            mapnode.add_child(event_list)

            if 'events' in map:
                for event in map['events']:
                    eventdict = lightchat_map.get_dict(f"event_{event['id']}")

                    eventnode = Node.void("event")
                    event_list.add_child(eventnode)
                    eventnode.set_attribute("id", str(event['id']))

                    eventnode.add_child(
                        Node.s32("display_state", eventdict.get_int("display_state")))

                    condition_list = Node.void("condition_list")
                    eventnode.add_child(condition_list)

                    if 'conditions' in event:
                        for condition in event['conditions']:
                            conditiondatadict = eventdict.get_dict(
                                f"condition_data_{condition['id']}")
                            conditionnode = Node.void("condition")
                            condition_list.add_child(conditionnode)
                            conditionnode.set_attribute(
                                "id", str(condition['id']))

                            if 'conditions' in condition:
                                for condition2 in condition['conditions']:
                                    conditiondict = conditiondatadict.get_dict(
                                        f"condition_{condition2['id']}")
                                    conditionnode2 = Node.void("condition")
                                    conditionnode.add_child(conditionnode2)
                                    conditionnode2.set_attribute(
                                        "id", str(condition2['id']))

                                    conditionnode2.add_child(
                                        Node.bool("is_cleared", conditiondict.get_bool("is_cleared")))
                                    conditionnode2.add_child(
                                        Node.s32("progress", conditiondict.get_int("progress")))

                    section_list = Node.void("section_list")
                    eventnode.add_child(section_list)

                    if 'sections' in event:
                        for section in event['sections']:
                            sectiondict = eventdict.get_dict(
                                f"section_{section['id']}")

                            sectionnode = Node.void("section")
                            section_list.add_child(sectionnode)
                            sectionnode.set_attribute("id", str(section['id']))

                            sectionnode.add_child(
                                Node.s32("acquired_jwatt", sectiondict.get_int("acquired_jwatt")))

                            mission_list = Node.void("mission_list")
                            sectionnode.add_child(mission_list)

                            if 'missions' in section:
                                for mission in section['missions']:
                                    missiondict = sectiondict.get_dict(
                                        f"mission_{mission['id']}")

                                    missionnode = Node.void("mission")
                                    mission_list.add_child(missionnode)
                                    missionnode.set_attribute(
                                        "id", str(mission['id']))

                                    missionnode.add_child(
                                        Node.bool("is_cleared", missiondict.get_bool("is_cleared")))
                                    missionnode.add_child(
                                        Node.s32("progress", missiondict.get_int("progress")))

        stamp = Node.void("stamp")
        player.add_child(stamp)
        stamp.add_child(Node.void("sheet_list"))

        return root

    def unformat_profile(self, userid: UserID, request: Node, oldprofile: Profile) -> Profile:
        newprofile = oldprofile.clone()
        newprofile.replace_bool("saved", True)
        data = request.child("data")

        game_config = self.get_game_config()
        force_unlock = game_config.get_bool("force_song_unlock")

        sysinfo = data.child("info")

        player = data.child("player")

        result = data.child("result")

        newprofile.replace_int("event_flag", player.child_value("event_flag"))

        last = newprofile.get_dict("last")
        if sysinfo is not None:
            last.replace_int("play_time", sysinfo.child_value("time_gameend"))
            last.replace_str("shopname", sysinfo.child_value("shopname"))
            last.replace_str("areaname", sysinfo.child_value("areaname"))

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
            newprofile.replace_int(
                "mynews_cnt", info.child_value("mynews_cnt"))
            newprofile.replace_int("bonus_tune_points",
                                   info.child_value("bonus_tune_points"))
            newprofile.replace_bool(
                "is_bonus_tune_played", info.child_value("is_bonus_tune_played"))

        lastnode = player.child("last")
        if lastnode is not None:
            last.replace_int(
                "expert_option", lastnode.child_value("expert_option"))
            last.replace_int("sort", lastnode.child_value("sort"))
            last.replace_int("category", lastnode.child_value("category"))

            settings = lastnode.child("settings")
            if settings is not None:
                last.replace_int("marker", settings.child_value("marker"))
                last.replace_int("theme", settings.child_value("theme"))
                last.replace_int("title", settings.child_value("title"))
                last.replace_int("parts", settings.child_value("parts"))
                last.replace_int(
                    "rank_sort", settings.child_value("rank_sort"))
                last.replace_int(
                    "combo_disp", settings.child_value("combo_disp"))
                last.replace_int(
                    "target_type", settings.child_value("target_type"))
                last.replace_int_array(
                    "emblem", 5, settings.child_value("emblem"))
                last.replace_int("matching", settings.child_value("matching"))
                last.replace_int("hard", settings.child_value("hard"))
                last.replace_int("hazard", settings.child_value("hazard"))

        item = player.child("item")
        if item is not None:
            newprofile.replace_int_array(
                "music_list", 64, item.child_value("music_list"))
            newprofile.replace_int_array(
                "theme_list", 16, item.child_value("theme_list"))
            newprofile.replace_int_array(
                "marker_list", 16, item.child_value("marker_list"))
            newprofile.replace_int_array(
                "title_list", 160, item.child_value("title_list"))
            newprofile.replace_int_array(
                "parts_list", 160, item.child_value("parts_list"))
            newprofile.replace_int_array(
                "commu_list", 16, item.child_value("commu_list"))

            if not force_unlock:
                owned_songs = self.calculate_owned_items(
                    item.child_value("secret_list"))
                for index in owned_songs:
                    self.data.local.user.put_achievement(
                        self.game, self.version, userid, index, "song", {})

            owned_emblems = self.calculate_owned_items(
                item.child_value("emblem_list"))
            for index in owned_emblems:
                self.data.local.user.put_achievement(
                    self.game, self.version, userid, index, "emblem", {})

            newitem = item.child("new")
            if newitem is not None:
                newprofile.replace_int_array(
                    "theme_list_new", 16, newitem.child_value("theme_list"))
                newprofile.replace_int_array(
                    "marker_list_new", 16, newitem.child_value("marker_list"))

                if not force_unlock:
                    owned_secrets = self.calculate_owned_items(
                        item.child_value("secret_list"))
                    for index in owned_secrets:
                        self.data.local.user.put_achievement(
                            self.game, self.version, userid, index, "secret", {})

        # TODO: Save Fullcombo challenge result

        free_first_play = player.child("free_first_play")
        if free_first_play is not None:
            newprofile.replace_bool(
                "free_first_play_applied", free_first_play.child_value("is_applied"))

        event_info = player.child("event_info")
        if event_info is not None:
            for child in event_info.children:
                try:
                    eventid = int(child.attribute("type"))
                except TypeError:
                    continue
                is_completed = child.child_value("is_completed")

                oldevent = self.data.local.user.get_achievement(
                    self.game, self.version, userid, eventid, "event")

                if oldevent is None:
                    oldevent = ValidatedDict()

                oldevent.replace_bool("is_completed", is_completed)

                self.data.local.user.put_achievement(
                    self.game, self.version, userid, eventid, "event", oldevent)

        jbox = player.child("jbox")
        if jbox is not None:
            jboxdict = newprofile.get_dict("jbox")
            jboxdict.replace_int("point", jbox.child_value("point"))
            emblemtype = jbox.child_value("emblem/type")
            index = jbox.child_value("emblem/index")
            if emblemtype == self.JBOX_EMBLEM_NORMAL:
                jboxdict.replace_int("normal_index", index)
            elif emblemtype == self.JBOX_EMBLEM_PREMIUM:
                jboxdict.replace_int("premium_index", index)
            newprofile.replace_dict("jbox", jboxdict)

        newprofile.replace_int("navi_flag", player.child_value("navi/flag"))

        jubility = player.child("jubility")
        if jubility is not None:
            target_music = jubility.child("target_music")

            hot_music_list = target_music.child("hot_music_list")
            pick_up_chart = ValidatedDict()
            for music in hot_music_list.children:
                music_id = music.child_value("music_id")
                chart = self.game_to_db_chart(int(music.child_value(
                    "seq")), bool(music.child_value("is_hard_mode")))
                music_rate = float(music.child_value("rate")) / 10
                value = float(music.child_value("value")) / 10
                entry = {
                    "music_id": music_id,
                    "seq": chart,
                    "music_rate": music_rate,
                    "value": value
                }
                pick_up_chart.replace_dict(f"{music_id}_{chart}", entry)

            newprofile.replace_dict("pick_up_chart", pick_up_chart)
            newprofile.replace_float("pick_up_jubility", float(
                hot_music_list.attribute("param")) / 10)

            other_music_list = target_music.child("other_music_list")
            common_chart = ValidatedDict()
            for music in other_music_list.children:
                music_id = music.child_value("music_id")
                chart = self.game_to_db_chart(int(music.child_value(
                    "seq")), bool(music.child_value("is_hard_mode")))
                music_rate = float(music.child_value("rate")) / 10
                value = float(music.child_value("value")) / 10
                entry = {
                    "music_id": music_id,
                    "seq": chart,
                    "music_rate": music_rate,
                    "value": value
                }
                common_chart.replace_dict(f"{music_id}_{chart}", entry)

            newprofile.replace_dict("common_chart", common_chart)
            newprofile.replace_float("common_jubility", float(
                other_music_list.attribute("param")) / 10)

        fill_in_category = player.child("fill_in_category")
        if fill_in_category is not None:
            fill_in_category_normal = fill_in_category.child("normal")
            if fill_in_category_normal is not None:
                newprofile.replace_int_array(
                    "normal_no_gray_flag_list", 16, fill_in_category_normal.child_value("no_gray_flag_list"))
                newprofile.replace_int_array(
                    "normal_all_yellow_flag_list", 16, fill_in_category_normal.child_value("all_yellow_flag_list"))
                newprofile.replace_int_array(
                    "normal_full_combo_flag_list", 16, fill_in_category_normal.child_value("full_combo_flag_list"))
                newprofile.replace_int_array(
                    "normal_excellent_flag_list", 16, fill_in_category_normal.child_value("excellent_flag_list"))

            fill_in_category_hard = fill_in_category.child("hard")
            if fill_in_category_hard is not None:
                newprofile.replace_int_array(
                    "hard_no_gray_flag_list", 16, fill_in_category_hard.child_value("no_gray_flag_list"))
                newprofile.replace_int_array(
                    "hard_all_yellow_flag_list", 16, fill_in_category_hard.child_value("all_yellow_flag_list"))
                newprofile.replace_int_array(
                    "hard_full_combo_flag_list", 16, fill_in_category_hard.child_value("full_combo_flag_list"))
                newprofile.replace_int_array(
                    "hard_excellent_flag_list", 16, fill_in_category_hard.child_value("excellent_flag_list"))

        lightchat = player.child("lightchat")
        if lightchat is not None:
            newprofile.replace_int(
                "lightchat_current_map_id", lightchat.child_value("next_map_id"))
            newprofile.replace_int(
                "lightchat_current_event_id", lightchat.child_value("next_event_id"))

            map_list = lightchat.child("map_list")
            if map_list is not None:
                for map in map_list.children:
                    map_id = map.attribute("id")

                    lightchat_map = self.data.local.user.get_achievement(
                        self.game, self.version, userid, map_id, "lightchat"
                    )

                    if lightchat_map is None:
                        lightchat_map = ValidatedDict()

                    lightchat_map.replace_int(
                        "tune_count", map.child_value("tune_count"))
                    lightchat_map.replace_int(
                        "last_daily_bonus_time", map.child_value("last_daily_bonus_time"))

                    event_list = map.child("event_list")
                    if event_list is not None:
                        for event in event_list.children:
                            event_id = event.attribute("id")
                            eventdict = lightchat_map.get_dict(
                                f"event_{event_id}")

                            if eventdict is None:
                                eventdict = ValidatedDict()

                            eventdict.replace_int(
                                "display_state", event.child_value("display_state"))

                            condition_list = event.child("condition_list")
                            if condition_list is not None:
                                for condition_data in condition_list.children:
                                    condition_data_id = condition_data.attribute(
                                        "id")

                                    conditiondatadict = eventdict.get_dict(
                                        f"condition_data_{condition_data_id}")
                                    if conditiondatadict is None:
                                        conditiondatadict = ValidatedDict()

                                    for condition in condition_data.children:
                                        condition_id = condition.attribute(
                                            "id")

                                        conditiondict = eventdict.get_dict(
                                            f"condition_{condition_id}")
                                        if conditiondict is None:
                                            conditiondict = ValidatedDict()

                                        conditiondict.replace_bool(
                                            "is_cleared", condition.child_value("is_cleared"))
                                        conditiondict.replace_int(
                                            "progress", condition.child_value("progress"))

                                        conditiondatadict.replace_dict(
                                            f"condition_{condition_id}", conditiondict)

                                    eventdict.replace_dict(
                                        f"condition_data_{condition_data_id}", conditiondatadict)

                            section_list = event.child("section_list")
                            if section_list is not None:
                                for section in section_list.children:
                                    section_id = section.attribute("id")

                                    sectiondict = eventdict.get_dict(
                                        f"section_{section_id}")

                                    if sectiondict is None:
                                        sectiondict = ValidatedDict()

                                    sectiondict.replace_int(
                                        "acquired_jwatt", section.child_value("acquired_jwatt"))

                                    mission_list = section.child(
                                        "mission_list")
                                    if mission_list is not None:
                                        for mission in mission_list.children:
                                            mission_id = mission.attribute(
                                                "id")

                                            missiondict = sectiondict.get_dict(
                                                f"mission_{mission_id}")

                                            if missiondict is None:
                                                missiondict = ValidatedDict()

                                            missiondict.replace_bool(
                                                "is_cleared", mission.child_value("is_cleared"))
                                            missiondict.replace_int(
                                                "progress", mission.child_value("progress"))

                                            sectiondict.replace_dict(
                                                f"mission_{mission_id}", missiondict)

                                    eventdict.replace_dict(
                                        f"section_{section_id}", sectiondict)

                            lightchat_map.replace_dict(
                                f"event_{event_id}", eventdict)

                    self.data.local.user.put_achievement(
                        self.game, self.version, userid, map_id, "lightchat", lightchat_map)

        if result is not None:
            for tune in result.children:
                if tune.name != "tune":
                    continue
                result = tune.child("player")
                songid = tune.child_value("music")
                timestamp = tune.child_value("timestamp") / 1000
                chart = self.game_to_db_chart(
                    int(result.child("score").attribute("seq")),
                    bool(result.child_value("is_hard_mode"))
                )
                points = result.child_value("score")
                flags = int(result.child("score").attribute("clear"))
                combo = int(result.child("score").attribute("combo"))
                ghost = result.child_value("mbar")
                music_rate = result.child_value("music_rate")

                stats = {
                    "perfect": result.child_value("nr_perfect"),
                    "great": result.child_value("nr_great"),
                    "good": result.child_value("nr_good"),
                    "poor": result.child_value("nr_poor"),
                    "miss": result.child_value("nr_miss")
                }

                last.replace_int("music_id", songid)
                last.replace_int("seq_id", int(
                    result.child("score").attribute("seq")))

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

                self.update_score(
                    userid,
                    timestamp,
                    songid,
                    chart,
                    points,
                    medal,
                    combo,
                    ghost,
                    stats,
                    music_rate,
                )

        return newprofile
