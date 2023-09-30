# vim: set fileencoding=utf-8
import random
from typing import Any, Dict, List, Optional, Set, Tuple
from typing_extensions import Final

from bemani.backend.jubeat.base import JubeatBase
from bemani.backend.jubeat.common import (
    JubeatGametopGetMeetingHandler
)
from bemani.backend.jubeat.avenue import JubeatAvenue

from bemani.backend.base import Status
from bemani.common import Profile, Time, ValidatedDict, VersionConstants
from bemani.data import Data, UserID, Score, Song
from bemani.protocol import Node


class JubeatBeyondTheAvenue(
    JubeatGametopGetMeetingHandler,
    JubeatBase
):
    name: str = "Jubeat beyond the Avenue"
    version: int = VersionConstants.JUBEAT_BEYOND_THE_AVENUE

    def previous_version(self) -> Optional[JubeatBase]:
        return JubeatAvenue(self.data, self.config, self.model)

    def __get_lightchat_list(self) -> List[Dict[str, Any]]:
        class RewardType:
            Music: Final[int] = 1
            Title: Final[int] = 2
            Parts: Final[int] = 10
            BonusTuneGauge: Final[int] = 11

        class ConditionType:
            ClearEvent: Final[int] = 1
            DifficultyScore: Final[int] = 2
            Jubility: Final[int] = 6
            TunePlays: Final[int] = 7

        class MissionType:
            CategorySongPlay: Final[int] = 1
            PlaySongWithCondition: Final[int] = 2
            PlaySong: Final[int] = 3
            PlaySongWithFullCombo: Final[int] = 4
            LevelScore: Final[int] = 6
            LevelCombo: Final[int] = 7
            MatchingSelect: Final[int] = 8
            RandomSelect: Final[int] = 9
            PlayHardMode: Final[int] = 10
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
                        "hint": "ジグザグをつなげると良いことがあるみたい",
                        "unlock_text": "jubility3,000かつZIGZAG COWBOYをフルコンボか100TUNESプレー",
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
                                "dialogue": "ねぇねぇ",
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
                                "dialogue": "えいニャ！",
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

                    # PETA
                    {
                        "id": 10,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "CAPELIの帽子はSSS級オシャレ!",
                        "unlock_text": "jubility3,000かつReincarnation Of Dead PetalをSSSか100TUNESプレー",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [5, 0, 0],
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
                                        "condition_type": 2,
                                        "params": [11000005, 5, 980000],
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
                                        "params": [5, 0, 0],
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
                                "reward_param": 13580,
                                "dialogue": "こんにちは",
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
                                        "mission_params": [15, 0, 0],
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
                                "reward_type": RewardType.Music,
                                "reward_param": 70000075,
                                "dialogue": "ゆっくりしていってね~",
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
                                        "mission_params": [2, 0, 0],
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
                                "reward_param": 8002,
                                "dialogue": "ここはどこ？って？",
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
                                        "mission_params": [70000075, 5, 950000],
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
                                "dialogue": "僕にも分からない",
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
                                        "mission_params": [24, 0, 0],
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
                                "dialogue": "え？もう帰っちゃうの？",
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
                                        "mission_params": [15, 0, 0],
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

                    # TULI
                    {
                        "id": 11,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "スゴイビルだなぁ。飛行機も飛んでる！",
                        "unlock_text": "jubility3,000かつMetricクリアか300TUNESプレー",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [8, 0, 0],
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
                                        "condition_type": 3,
                                        "params": [50000338, 5, 0],
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
                                        "params": [8, 0, 0],
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
                                        "params": [300, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                ]
                            },
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "0edf40",
                                "required_jwatt": 2000,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13581,
                                "dialogue": "何食べようかな",
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
                                        "mission_type": MissionType.PlayHardMode,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [18, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "37d970",
                                "required_jwatt": 17600,
                                "reward_type": RewardType.Music,
                                "reward_param": 60000072,
                                "dialogue": "あ、さっきご飯食べたんだった",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 2000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [20, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [6, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "7aabb4",
                                "required_jwatt": 3000,
                                "reward_type": RewardType.Title,
                                "reward_param": 8003,
                                "dialogue": "写真撮って欲しいの？",
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
                                        "mission_params": [60000072, 5, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 400
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "3fe6c0",
                                "required_jwatt": 15000,
                                "reward_type": RewardType.Music,
                                "reward_param": 80000022,
                                "dialogue": "こっちに来て!",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 2000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [19, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 5,
                                "tube_text": "ee6dbc",
                                "required_jwatt": 3500,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000009,
                                "dialogue": "はい、チーズ!",
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
                                        "mission_params": [80000022, 5, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                        ]
                    },

                    # TOPEE
                    {
                        "id": 12,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "おや？キツネがこちらを見ているようです",
                        "unlock_text": "jubility3,000かつconconクリアか300TUNESプレー",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [8, 0, 0],
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
                                        "condition_type": 3,
                                        "params": [30000127, 5, 0],
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
                                        "params": [8, 0, 0],
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
                                        "params": [300, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                ]
                            },
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "0edf40",
                                "required_jwatt": 2000,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13582,
                                "dialogue": "こっちこっち！",
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
                                        "mission_type": MissionType.PlayHardMode,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [23, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "37d970",
                                "required_jwatt": 17600,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "探検って楽しいね",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 3000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [30000127, 5, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [3, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "7aabb4",
                                "required_jwatt": 3200,
                                "reward_type": RewardType.Title,
                                "reward_param": 8004,
                                "dialogue": "あれ？あとちょっとなんだけどな",
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
                                        "mission_params": [21, 0, 0],
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
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "3fe6c0",
                                "required_jwatt": 15000,
                                "reward_type": RewardType.Music,
                                "reward_param": 50000102,
                                "dialogue": "ほら、見えてきたよ",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 2000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [22, 0, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.CategorySongPlay,
                                        "bonus_type": BonusType.L,
                                        "bonus_param": 5
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 5,
                                "tube_text": "ee6dbc",
                                "required_jwatt": 3500,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000022,
                                "dialogue": "また探検しようね!",
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
                                        "mission_params": [50000102, 5, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                        ]
                    },

                    # NIGNIG
                    {
                        "id": 13,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "お礼の楽曲でスゴイ点数を取ると…",
                        "unlock_text": "お題の4曲全てのEXTのスコア95万点を取るか600TUNESプレー",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [9, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 1,
                                        "params": [10, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 3,
                                        "condition_type": 1,
                                        "params": [11, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 4,
                                        "condition_type": 1,
                                        "params": [12, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 5,
                                        "condition_type": 2,
                                        "params": [11000004, 2, 950000],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 6,
                                        "condition_type": 2,
                                        "params": [11000004, 2, 950000],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 7,
                                        "condition_type": 2,
                                        "params": [11000009, 2, 950000],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 8,
                                        "condition_type": 2,
                                        "params": [11000022, 2, 950000],
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
                                        "params": [9, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 1,
                                        "params": [10, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 3,
                                        "condition_type": 1,
                                        "params": [11, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 4,
                                        "condition_type": 1,
                                        "params": [12, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 5,
                                        "condition_type": 7,
                                        "params": [600, 0, 0],
                                        "precondition_ids": [0]
                                    }
                                ]
                            },
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "b967a4",
                                "required_jwatt": 3000,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13583,
                                "dialogue": "モグモグ",
                                # 부스트 미션
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
                                        "mission_params": [60000065, 2, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 2,
                                "tube_text": "dedbdc",
                                "required_jwatt": 3000,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "もっと夢を見せて",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 3000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [80000082, 2, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 3,
                                "tube_text": "e7e67c",
                                "required_jwatt": 3500,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "こんなに大きい夢は初めて",
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
                                        "mission_params": [80000090, 2, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 4,
                                "tube_text": "3fe6c0",
                                "required_jwatt": 4400,
                                "reward_type": RewardType.Title,
                                "reward_param": 8005,
                                "dialogue": "まだ夢の中なんだ",
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
                                        "mission_params": [90000013, 2, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.RandomSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 5,
                                "tube_text": "db6dbc",
                                "required_jwatt": 5800,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "誰か呼んでるよ",
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
                                        "mission_params": [90000123, 2, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 300
                                    },
                                ]
                            },
                            {
                                "id": 6,
                                "tube_text": "e7b7bc",
                                "required_jwatt": 6500,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000016,
                                "dialogue": "ほら、起きて",
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
                                        "mission_params": [90000124, 2, 950000],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithCondition,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
                                    },
                                    {
                                        "id": 3,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.MatchingSelect,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 450
                                    },
                                ]
                            },
                        ]
                    },

                    # HALO
                    {
                        "id": 14,
                        "event_type": 1,
                        "start_time": 1659488400000,
                        "end_time": 4102412399000,
                        "is_open": True,
                        "hint": "？？？？？",
                        "unlock_text": "jubility7,500達成か2,000TUNESプレー",
                        "conditions": [
                            {
                                "id": 1,
                                "conditions": [
                                    {
                                        "id": 1,
                                        "condition_type": 1,
                                        "params": [13, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 6,
                                        "params": [7500, 0, 0],
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
                                        "params": [13, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                    {
                                        "id": 2,
                                        "condition_type": 7,
                                        "params": [2000, 0, 0],
                                        "precondition_ids": [0]
                                    },
                                ]
                            },
                        ],
                        # 해금 순서
                        "sections": [
                            {
                                "id": 1,
                                "tube_text": "df76bc",
                                "required_jwatt": 3500,
                                "reward_type": RewardType.Parts,
                                "reward_param": 13584,
                                "dialogue": "ここは終わりの地",
                                # 부스트 미션
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
                                        "mission_params": [50000102, 2, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithFullCombo,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
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
                                "id": 2,
                                "tube_text": "de7b9c",
                                "required_jwatt": 4500,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "何も無い世界",
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
                                        "mission_params": [20000120, 2, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithFullCombo,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 500
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
                                "id": 3,
                                "tube_text": "7b6e6c",
                                "required_jwatt": 5500,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "まだ光を持ってるね",
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
                                        "mission_params": [70000011, 2, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithFullCombo,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 650
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
                                "tube_text": "3fe6c0",
                                "required_jwatt": 6500,
                                "reward_type": RewardType.Title,
                                "reward_param": 8006,
                                "dialogue": "キミはまだここに居るべきじゃない",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1200
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [80000088, 2, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithFullCombo,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 750
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
                                "id": 5,
                                "tube_text": "7b7eec",
                                "required_jwatt": 7500,
                                "reward_type": RewardType.BonusTuneGauge,
                                "reward_param": 100,
                                "dialogue": "みんな待ってるよ",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1200
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [90000166, 2, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithFullCombo,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 750
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
                                "id": 6,
                                "tube_text": "fffffc",
                                "required_jwatt": 12000,
                                "reward_type": RewardType.Music,
                                "reward_param": 11000014,
                                "dialogue": "また来てね",
                                "missions": [
                                    {
                                        "id": 1,
                                        "mission_params": [1, 0, 0],
                                        "repeatable": True,
                                        "mission_type": MissionType.DailyFirstPlay,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 2000
                                    },
                                    {
                                        "id": 2,
                                        "mission_params": [50000208, 2, 0],
                                        "repeatable": False,
                                        "mission_type": MissionType.PlaySongWithFullCombo,
                                        "bonus_type": BonusType.JWATT,
                                        "bonus_param": 1000
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

        event_info = Node.void("event_info")
        info.add_child(event_info)

        share_music = Node.void("share_music")
        info.add_child(share_music)

        genre_def_music = Node.void("genre_def_music")
        info.add_child(genre_def_music)

        info.add_child(
            Node.s32_array(
                "black_jacket_list",
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            )
        )

        weekly_music = Node.void("weekly_music")
        info.add_child(weekly_music)

        info.add_child(
            Node.s32_array(
                "white_music_list",
                [
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                ],
            )
        )

        info.add_child(
            Node.s32_array(
                "white_marker_list",
                [
                    255,
                    255,
                    255,
                    255,
                    255,
                    240,
                    1,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ],
            )
        )

        info.add_child(
            Node.s32_array(
                "white_theme_list",
                [
                    255,
                    29,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            )
        )

        info.add_child(
            Node.s32_array(
                "add_default_music_list",
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            )
        )

        info.add_child(
            Node.s32_array(
                "open_music_list",
                [
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                    -1,
                ],
            )
        )

        info.add_child(
            Node.s32_array(
                "shareable_music_list",
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            )
        )

        info.add_child(
            Node.s32_array(
                "inf_ojisan_music_list",
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            )
        )

        info.add_child(
            Node.s32_array(
                "hot_music_list",
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    -294928,
                    -1,
                    -1,
                    1069543551,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0
                ]
            )
        )

        jbox = Node.void("jbox")
        info.add_child(jbox)
        jbox.add_child(Node.s32("point", 0))
        emblem = Node.void("emblem")
        jbox.add_child(emblem)
        normal = Node.void("normal")
        emblem.add_child(normal)
        premium = Node.void("premium")
        emblem.add_child(premium)
        normal.add_child(Node.s16("index", 1))
        premium.add_child(Node.s16("index", 1))

        born = Node.void("born")
        info.add_child(born)
        born.add_child(Node.s8("status", 0))
        born.add_child(Node.s16("year", 0))

        expert_option = Node.void("expert_option")
        info.add_child(expert_option)
        expert_option.add_child(Node.bool("is_available", True))

        konami_logo_50th = Node.void("konami_logo_50th")
        info.add_child(konami_logo_50th)
        konami_logo_50th.add_child(Node.bool("is_available", True))

        all_music_matching = Node.void("all_music_matching")
        info.add_child(all_music_matching)
        all_music_matching.add_child(Node.bool("is_available", True))

        random_option = Node.void("random_option")
        info.add_child(random_option)
        random_option.add_child(Node.bool("is_available", True))

        judge_disp = Node.void("judge_disp")
        info.add_child(judge_disp)
        judge_disp.add_child(Node.bool("is_available", True))

        question_list = Node.void("question_list")
        info.add_child(question_list)

        department = Node.void("department")
        info.add_child(department)
        shop_list = Node.void("shop_list")
        department.add_child(shop_list)

        # team_battle

        # qr

        # course_list

        # emo_list

        # hike_event

        # tip_list

        # festo_dungeon

        # travel

        lightchat = Node.void("lightchat")
        info.add_child(lightchat)
        map_list = Node.void("map_list")
        lightchat.add_child(map_list)

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

        # lightchat_bonus_event

        # stamp

        # sync_wait_setting

        return info

    def handle_shopinfo_ave2_regist_request(self, request: Node) -> Node:
        self.update_machine_name(request.child_value("shop/name"))

        shopinfo = Node.void("shopinfo_ave2")

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

    def handle_demodata_ave2_get_info_request(self, request: Node) -> Node:
        root = Node.void("demodata_ave2")
        data = Node.void("data")
        root.add_child(data)

        info = Node.void("info")
        data.add_child(info)

        info.add_child(
            Node.s32_array(
                "black_jacket_list",
                [
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            )
        )

        return root

    def handle_demodata_ave2_get_jbox_list_request(self, request: Node) -> Node:
        root = Node.void("demodata_ave2")
        return root

    def handle_gametop_ave2_get_info_request(self, request: Node) -> Node:
        root = Node.void("gametop_ave2")
        data = Node.void("data")
        root.add_child(data)
        data.add_child(self.__get_global_info())

        return root

    def handle_gametop_ave2_regist_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")
        refid = player.child_value("refid")
        name = player.child_value("name")
        root = self.new_profile_by_refid(refid, name)

        return root

    def handle_gametop_ave2_get_pdata_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")
        refid = player.child_value("refid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("gametop_ave2")
            root.set_attribute("status", str(Status.NO_PROFILE))

        return root

    def handle_gametop_ave2_get_mdata_request(self, request: Node) -> Node:
        data = request.child("data")
        player = data.child("player")
        extid = player.child_value("jid")
        mdata_ver = player.child_value("mdata_ver")
        root = self.get_scores_by_extid(extid, mdata_ver, 3)
        if root is None:
            root = Node.void("gametop_ave2")
            root.set_attribute("status", str(Status.NO_PROFILE))

        return root

    def format_scores(
            self, userid: UserID, profile: Profile, scores: List[Score]
    ) -> Node:
        root = Node.void("gametop_ave2")
        datanode = Node.void("data")
        root.add_child(datanode)
        player = Node.void("player")
        datanode.add_child(player)
        player.add_child(Node.s32("jid", profile.extid))
        playdata = Node.void("mdata_list")
        player.add_child(playdata)

        return root

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("gametop_ave2")
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
        for achievement in achievements:
            if achievement.type == "event":
                event_completion[achievement.id] = achievement.data.get_bool(
                    "is_completed"
                )
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

        player.add_child(Node.s32("jid", profile.extid))
        player.add_child(Node.s32("session_id", 1))
        player.add_child(Node.string("name", profile.get_str("name", "PLAYER")))
        player.add_child(Node.u64("event_flag", profile.get_int("event_flag")))

        info = Node.void("info")
        player.add_child(info)
        info.add_child(
            Node.bool(
                "inherit",
                profile.get_bool("has_old_version") and not profile.get_bool("saved"),
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
        info.add_child(Node.s32("mtg_entry_cnt", profile.get_int("mtg_entry_cnt")))
        info.add_child(Node.s32("mtg_hold_cnt", profile.get_int("mtg_hold_cnt")))
        info.add_child(Node.u8("mtg_result", profile.get_int("mtg_result")))
        info.add_child(
            Node.s32("bonus_tune_points", profile.get_int("bonus_tune_points"))
        )
        info.add_child(
            Node.bool("is_bonus_tune_played", profile.get_bool("is_bonus_tune_played"))
        )

        lastdict = profile.get_dict("last")
        last = Node.void("last")
        player.add_child(last)
        last.add_child(Node.s64("play_time", lastdict.get_int("play_time")))
        last.add_child(Node.string("shopname", lastdict.get_str("shopname")))
        last.add_child(Node.string("areaname", lastdict.get_str("areaname")))
        last.add_child(Node.s32("music_id", lastdict.get_int("music_id")))
        last.add_child(Node.s8("seq_id", lastdict.get_int("seq_id")))
        if lastdict.get_int("seq_id") == 3:
            last.add_child(Node.string("seq_edit_id", lastdict.get_str("seq_edit_id")))
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
        settings.add_child(Node.s32("target_type", lastdict.get_int("target_type")))
        settings.add_child(Node.s8("judge_disp", lastdict.get_int("judge_disp")))
        settings.add_child(Node.s8("random_option", lastdict.get_int("random_option")))
        settings.add_child(Node.s8("matching", lastdict.get_int("matching")))
        settings.add_child(Node.s8("hard", lastdict.get_int("hard")))
        settings.add_child(Node.s8("hazard", lastdict.get_int("hazard")))

        partslist = lastdict.get_int_array("emblem", 5, [0, default_main, 0, 0, 0])
        if partslist[1] == 0:
            partslist[1] = default_main
        settings.add_child(Node.s16_array("emblem", partslist))

        item = Node.void("item")
        player.add_child(item)
        item.add_child(
            Node.s32_array(
                "music_list", profile.get_int_array("music_list", 64, [-1] * 64)
            )
        )
        item.add_child(
            Node.s32_array(
                "secret_list",
                ([-1] * 64)
                if force_unlock
                else self.create_owned_items(owned_songs, 64),
            )
        )
        item.add_child(
            Node.s32_array(
                "theme_list", profile.get_int_array("theme_list", 16, [-1] * 16)
            )
        )
        item.add_child(
            Node.s32_array(
                "marker_list", profile.get_int_array("marker_list", 16, [-1] * 16)
            )
        )
        item.add_child(
            Node.s32_array(
                "title_list", profile.get_int_array("title_list", 160, [-1] * 160)
            )
        )
        item.add_child(
            Node.s32_array(
                "parts_list", profile.get_int_array("parts_list", 160, [-1] * 160)
            )
        )
        item.add_child(
            Node.s32_array("emblem_list", self.create_owned_items(owned_emblems, 96))
        )
        item.add_child(
            Node.s32_array(
                "commu_list", profile.get_int_array("commu_list", 16, [-1] * 16)
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
                "theme_list", profile.get_int_array("theme_list_new", 16, [-1] * 16)
            )
        )
        new.add_child(
            Node.s32_array(
                "marker_list", profile.get_int_array("marker_list_new", 16, [-1] * 16)
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

        start_time, end_time = self.data.local.network.get_schedule_duration("daily")
        today_attempts = self.data.local.music.get_all_attempts(
            self.game,
            self.music_version,
            userid,
            entry.get_int("today", -1),
            timelimit=start_time
        )
        whim_attempts = self.data.local.music.get_all_attempts(
            self.game,
            self.music_version,
            userid,
            entry.get_int("whim", -1),
            timelimit=start_time
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

        official_news = Node.void("official_news")
        player.add_child(official_news)
        news_list = Node.void("news_list")
        official_news.add_child(news_list)

        history = Node.void("history")
        player.add_child(history)
        history.set_attribute("count", "0")

        free_first_play = Node.void("free_first_play")
        player.add_child(free_first_play)
        free_first_play.add_child(Node.bool("is_available", False))

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
        born.add_child(Node.s8("status", profile.get_int("born_status")))
        born.add_child(Node.s16("year", profile.get_int("born_year")))

        question_list = Node.void("question_list")
        player.add_child(question_list)

        server = Node.void("server")
        player.add_child(server)

        course_list = Node.void("course_list")
        player.add_child(course_list)

        fill_in_category = Node.void("fill_in_category")
        player.add_child(fill_in_category)

        normal = Node.void("normal")
        fill_in_category.add_child(normal)
        normal.add_child(
            Node.s32_array(
                "no_gray_flag_list",
                profile.get_int_array("normal_no_gray_flag_list", 16, [0] * 16),
            )
        )
        normal.add_child(
            Node.s32_array(
                "all_yellow_flag_list",
                profile.get_int_array("normal_all_yellow_flag_list", 16, [0] * 16),
            )
        )
        normal.add_child(
            Node.s32_array(
                "full_combo_flag_list",
                profile.get_int_array("normal_full_combo_flag_list", 16, [0] * 16),
            )
        )
        normal.add_child(
            Node.s32_array(
                "excellent_flag_list",
                profile.get_int_array("normal_excellent_flag_list", 16, [0] * 16),
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
                profile.get_int_array("hard_all_yellow_flag_list", 16, [0] * 16),
            )
        )
        hard.add_child(
            Node.s32_array(
                "full_combo_flag_list",
                profile.get_int_array("hard_full_combo_flag_list", 16, [0] * 16),
            )
        )
        hard.add_child(
            Node.s32_array(
                "excellent_flag_list",
                profile.get_int_array("hard_excellent_flag_list", 16, [0] * 16),
            )
        )

        eamuse_gift_list = Node.void("eamuse_gift_list")
        player.add_child(eamuse_gift_list)

        lightchat = Node.void("lightchat")
        player.add_child(lightchat)
        lightchat.add_child(
            Node.s32("current_map_id", profile.get_int("lightchat_current_map_id", 1)))
        lightchat.add_child(Node.s32("current_event_id",
                            profile.get_int("lightchat_current_event_id", 1)))

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
                            sectionnode.add_child(
                                Node.bool("is_cleared", sectiondict.get_bool("is_cleared"))
                            )

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
        sheet_list = Node.void("sheet_list")
        stamp.add_child(sheet_list)

        return root
