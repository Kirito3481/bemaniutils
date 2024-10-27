# vim: set fileencoding=utf-8
import random
import re
from typing import Dict, Final, List, Optional

from bemani.backend.iidx.base import IIDXBase
from bemani.backend.iidx.rootage import IIDXRootage

from bemani.common import VersionConstants, ID, Profile, ValidatedDict, Time
from bemani.protocol import Node
from bemani.data import UserID, Score


class IIDXHeroicVerse(IIDXBase):
    name: str = "Beatmania IIDX HEROIC VERSE"
    version: int = VersionConstants.IIDX_HEROIC_VERSE

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

    GAME_GHOST_TYPE_RIVAL: Final[int] = 1
    GAME_GHOST_TYPE_GLOBAL_TOP: Final[int] = 2
    GAME_GHOST_TYPE_GLOBAL_AVERAGE: Final[int] = 3
    GAME_GHOST_TYPE_LOCAL_TOP: Final[int] = 4
    GAME_GHOST_TYPE_LOCAL_AVERAGE: Final[int] = 5
    GAME_GHOST_TYPE_DAN_TOP: Final[int] = 6
    GAME_GHOST_TYPE_DAN_AVERAGE: Final[int] = 7
    GAME_GHOST_TYPE_RIVAL_TOP: Final[int] = 8
    GAME_GHOST_TYPE_RIVAL_AVERAGE: Final[int] = 9

    GAME_GHOST_LENGTH: Final[int] = 64

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

    FAVORITE_LIST_LENGTH: Final[int] = 20

    GAME_CHART_TYPE_N7: Final[int] = 0
    GAME_CHART_TYPE_H7: Final[int] = 1
    GAME_CHART_TYPE_A7: Final[int] = 2
    GAME_CHART_TYPE_N14: Final[int] = 3
    GAME_CHART_TYPE_H14: Final[int] = 4
    GAME_CHART_TYPE_A14: Final[int] = 5
    GAME_CHART_TYPE_B7: Final[int] = 6
    GAME_CHART_TYPE_L7: Final[int] = 7
    GAME_CHART_TYPE_B14: Final[int] = 8
    GAME_CHART_TYPE_L14: Final[int] = 9

    GAME_ARENA_CLASS_D5: Final[int] = 0
    GAME_ARENA_CLASS_D4: Final[int] = 1
    GAME_ARENA_CLASS_D3: Final[int] = 2
    GAME_ARENA_CLASS_D2: Final[int] = 3
    GAME_ARENA_CLASS_D1: Final[int] = 4
    GAME_ARENA_CLASS_C5: Final[int] = 5
    GAME_ARENA_CLASS_C4: Final[int] = 6
    GAME_ARENA_CLASS_C3: Final[int] = 7
    GAME_ARENA_CLASS_C2: Final[int] = 8
    GAME_ARENA_CLASS_C1: Final[int] = 9
    GAME_ARENA_CLASS_B5: Final[int] = 10
    GAME_ARENA_CLASS_B4: Final[int] = 11
    GAME_ARENA_CLASS_B3: Final[int] = 12
    GAME_ARENA_CLASS_B2: Final[int] = 13
    GAME_ARENA_CLASS_B1: Final[int] = 14
    GAME_ARENA_CLASS_A5: Final[int] = 15
    GAME_ARENA_CLASS_A4: Final[int] = 16
    GAME_ARENA_CLASS_A3: Final[int] = 17
    GAME_ARENA_CLASS_A2: Final[int] = 18
    GAME_ARENA_CLASS_A1: Final[int] = 19

    requires_extended_regions: bool = True

    def previous_version(self) -> Optional[IIDXBase]:
        return IIDXRootage(self.data, self.config, self.model)

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
            self.GAME_CHART_TYPE_L7: self.CHART_TYPE_L7,
            self.GAME_CHART_TYPE_B14: self.CHART_TYPE_B14,
            self.GAME_CHART_TYPE_N14: self.CHART_TYPE_N14,
            self.GAME_CHART_TYPE_H14: self.CHART_TYPE_H14,
            self.GAME_CHART_TYPE_A14: self.CHART_TYPE_A14,
            self.GAME_CHART_TYPE_L14: self.CHART_TYPE_L14,
        }[db_chart]

    # Overwrite to handle the ghost gauge
    def update_score(
        self,
        userid: Optional[UserID],
        songid: int,
        chart: int,
        clear_status: int,
        pgreats: int,
        greats: int,
        miss_count: int,
        ghost: Optional[bytes],
        ghost_gauge: Optional[bytes],
        shop: Optional[int],
    ) -> None:
        """
        Given various pieces of a score, update the user's high score and score
        history in a controlled manner, so all games in IIDX series can expect
        the same attributes in a score. Note that the medals passed here are
        expected to be converted from game identifier to our internal identifier,
        so that any game in the series may convert them back. In this way, a song
        played on Pendual that exists in Tricoro will still have scores/medals
        going back all versions.
        """
        # Range check medals
        if clear_status not in [
            self.CLEAR_STATUS_NO_PLAY,
            self.CLEAR_STATUS_FAILED,
            self.CLEAR_STATUS_ASSIST_CLEAR,
            self.CLEAR_STATUS_EASY_CLEAR,
            self.CLEAR_STATUS_CLEAR,
            self.CLEAR_STATUS_HARD_CLEAR,
            self.CLEAR_STATUS_EX_HARD_CLEAR,
            self.CLEAR_STATUS_FULL_COMBO,
        ]:
            raise Exception(f"Invalid clear status value {clear_status}")

        # Calculate ex score
        ex_score = (2 * pgreats) + greats

        if userid is not None:
            if (ghost or ghost_gauge) is None:
                raise Exception("Expected a ghost/ghost gauge for user score save!")
            oldscore = self.data.local.music.get_score(
                self.game,
                self.music_version,
                userid,
                songid,
                chart,
            )
        else:
            # Storing an anonymous attempt
            if (ghost or ghost_gauge) is not None:
                raise Exception("Expected no ghost for anonymous score save!")
            oldscore = None

        # Score history is verbatum, instead of highest score
        history = ValidatedDict(
            {
                "clear_status": clear_status,
                "miss_count": miss_count,
            }
        )
        old_ex_score = ex_score

        if ghost is not None:
            history["ghost"] = ghost
        if ghost_gauge is not None:
            history["ghost_gauge"] = ghost_gauge

        if oldscore is None:
            # If it is a new score, create a new dictionary to add to
            scoredata = ValidatedDict(
                {
                    "clear_status": clear_status,
                    "pgreats": pgreats,
                    "greats": greats,
                }
            )
            if miss_count != -1:
                scoredata.replace_int("miss_count", miss_count)
            if ghost is not None:
                scoredata["ghost"] = ghost
            if ghost_gauge is not None:
                scoredata["ghost_gauge"] = ghost_gauge
            raised = True
            highscore = True
        else:
            # Set the score to any new record achieved
            raised = ex_score > oldscore.points
            highscore = ex_score >= oldscore.points
            ex_score = max(ex_score, oldscore.points)
            scoredata = oldscore.data
            scoredata.replace_int("clear_status", max(scoredata.get_int("clear_status"), clear_status))
            if miss_count != -1:
                if scoredata.get_int("miss_count", -1) == -1:
                    scoredata.replace_int("miss_count", miss_count)
                else:
                    scoredata.replace_int("miss_count", min(scoredata.get_int("miss_count"), miss_count))
            if raised:
                scoredata.replace_int("pgreats", pgreats)
                scoredata.replace_int("greats", greats)
                if ghost is not None:
                    scoredata.replace_bytes("ghost", ghost)
                if ghost_gauge is not None:
                    scoredata.replace_bytes("ghost_gauge", ghost_gauge)

        if shop is not None:
            history.replace_int("shop", shop)
            scoredata.replace_int("shop", shop)

        # Look up where this score was earned
        lid = self.get_machine_id()

        if userid is not None:
            # Write the new score back
            self.data.local.music.put_score(
                self.game,
                self.music_version,
                userid,
                songid,
                chart,
                lid,
                ex_score,
                scoredata,
                highscore,
            )

        # Save the history of this score too
        self.data.local.music.put_attempt(
            self.game,
            self.music_version,
            userid,
            songid,
            chart,
            lid,
            old_ex_score,
            history,
            raised,
        )

    # Overwrite make_score_struct to handle the new chart types
    def make_score_struct(self, scores: List[Score], cltype: int, index: int) -> List[List[int]]:
        scorestruct: Dict[int, List[int]] = {}

        for score in scores:
            musicid = score.id
            chart = score.chart

            # Filter to only singles/doubles charts
            if cltype == self.CLEAR_TYPE_SINGLE:
                if chart not in [
                    self.CHART_TYPE_B7,
                    self.CHART_TYPE_N7,
                    self.CHART_TYPE_H7,
                    self.CHART_TYPE_A7,
                    self.CHART_TYPE_L7,
                ]:
                    continue
                chartindex = {
                    self.CHART_TYPE_B7: 0,
                    self.CHART_TYPE_N7: 1,
                    self.CHART_TYPE_H7: 2,
                    self.CHART_TYPE_A7: 3,
                    self.CHART_TYPE_L7: 4,
                }[chart]
            if cltype == self.CLEAR_TYPE_DOUBLE:
                if chart not in [
                    self.CHART_TYPE_B14,
                    self.CHART_TYPE_N14,
                    self.CHART_TYPE_H14,
                    self.CHART_TYPE_A14,
                    self.CHART_TYPE_L14,
                ]:
                    continue
                chartindex = {
                    self.CHART_TYPE_B14: 0,
                    self.CHART_TYPE_N14: 1,
                    self.CHART_TYPE_H14: 2,
                    self.CHART_TYPE_A14: 3,
                    self.CHART_TYPE_L14: 4,
                }[chart]

            if musicid not in scorestruct:
                scorestruct[musicid] = [
                    index,  # -1 is our scores, positive is rival index
                    musicid,  # Music ID!
                    0,  # Beginner status,
                    0,  # Normal status,
                    0,  # Hyper status,
                    0,  # Another status,
                    0,  # Leggendaria status,
                    0,  # EX score beginner,
                    0,  # EX score normal,
                    0,  # EX score hyper,
                    0,  # EX score another,
                    0,  # EX score leggendaria,
                    -1,  # Miss count beginner,
                    -1,  # Miss count normal,
                    -1,  # Miss count hyper,
                    -1,  # Miss count another,
                    -1,  # Miss count leggendaria,
                ]

            scorestruct[musicid][chartindex + 1] = self.db_to_game_status(score.data.get_int("clear_status"))
            scorestruct[musicid][chartindex + 6] = score.points
            scorestruct[musicid][chartindex + 11] = score.data.get_int("miss_count", -1)

        return [scorestruct[s] for s in scorestruct]

    def handle_IIDX27shop_sentinfo_request(self, request: Node) -> Node:
        return Node.void("IIDX27shop")

    def handle_IIDX27gameSystem_systemInfo_request(self, request: Node) -> Node:
        root = Node.void("IIDX27gameSystem")

        arena_schedule = Node.void("arena_schedule")
        root.add_child(arena_schedule)
        arena_schedule.add_child(Node.u8("phase", 3))  # 1 - 개최하지 않습니다, 2 - 개최 예고, 3 - 개최 중
        arena_schedule.add_child(Node.u32("start", Time.beginning_of_this_month()))
        arena_schedule.add_child(Node.u32("end", Time.end_of_this_month()))

        # rewards = [
        #     {
        #         "cube_num": 1,
        #         "kind": 1,
        #         "value": ""
        #     }
        # ]
        # for index, reward in enumerate(rewards):
        #     arena_reward = Node.void("arena_reward")
        #     root.add_child(arena_reward)
        #     arena_reward.add_child(Node.s32("index", index))
        #     arena_reward.add_child(Node.s32("cube_num", reward["cube_num"]))
        #     arena_reward.add_child(Node.s32("kind", reward["kind"]))
        #     arena_reward.add_child(Node.string("value", reward["value"]))

        for play_style in (self.GAME_CLTYPE_SINGLE, self.GAME_CLTYPE_DOUBLE):
            for arena_class in range(20):
                arena_music_difficult = Node.void("arena_music_difficult")
                root.add_child(arena_music_difficult)
                arena_music_difficult.add_child(Node.s32("play_style", play_style))
                arena_music_difficult.add_child(Node.s32("arena_class", arena_class))
                arena_music_difficult.add_child(Node.s32("low_difficult", 1))
                arena_music_difficult.add_child(Node.s32("high_difficult", 12))
                arena_music_difficult.add_child(Node.bool("is_leggendaria", True))
                arena_music_difficult.add_child(Node.s32("force_music_list_id", 0))

                # maching_class_range = Node.void("maching_class_range")
                # root.add_child(maching_class_range)
                # maching_class_range.add_child(Node.s32("play_style", play_style))
                # maching_class_range.add_child(Node.s32("matching_class", arena_class))
                # maching_class_range.add_child(Node.s32("low_arena_class", arena_class))
                # maching_class_range.add_child(Node.s32("high_arena_class", arena_class + 4))

        return root

    def handle_IIDX27lobby_entry_request(self, request: Node) -> Node:
        extid = request.child_value("iidx_id")
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        root = Node.void("IIDX27lobby")
        if userid is None:
            root.set_attribute("fault", "1")
            return root

        lobbies = self.data.local.lobby.get_all_lobbies(self.game, self.version)
        previous_hosted_lobbies = [True for uid, _ in lobbies if uid == userid]
        previous_joined_lobbies = [(uid, lobby) for uid, lobby in lobbies if userid in lobby["participants"]]
        nonfull_lobbies = [(uid, lobby) for uid, lobby in lobbies if len(lobby["participants"]) < 4]

        self.data.local.lobby.put_play_session_info(
            self.game,
            self.version,
            userid,
            {
                "ver": request.child_value("ver"),
                "play_style": request.child_value("play_style"),
                "arena_class": request.child_value("arena_class"),
                "lose_value": request.child_value("lose_value"),
                "ga": request.child_value("address/ga"),
                "gp": request.child_value("address/gp"),
                "la": request.child_value("address/la"),
                "pcbid": self.config.machine.pcbid,
            }
        )

        play_session_info = self.data.local.lobby.get_play_session_info(
            self.game,
            self.version,
            userid,
        )

        if (nonfull_lobbies or previous_joined_lobbies) and not previous_hosted_lobbies:
            if previous_joined_lobbies:
                # If we're already "in" a lobby, we should go back to that one.
                uid, lobby = previous_joined_lobbies[0]
            else:
                # Pick a random one, assign ourselves to it.
                uid, lobby = random.choice(nonfull_lobbies)

            # Look up the host's information.
            host_play_session_info = self.data.local.lobby.get_play_session_info(
                self.game,
                self.version,
                uid,
            )

            # Join this lobby.
            participants = set(lobby["participants"])
            participants.add(userid)
            lobby["participants"] = list(participants)
            self.data.local.lobby.put_lobby(self.game, self.version, uid, lobby)

            root.add_child(Node.bool("host", False))
            root.add_child(Node.s32("matching_class", host_play_session_info.get_int("matching_class")))
            address = Node.void("address")
            root.add_child(address)
            address.add_child(Node.u8_array("ga", host_play_session_info.get_int_array("ga", 4)))
            address.add_child(Node.u16("gp", host_play_session_info.get_int("gp")))
            address.add_child(Node.u8_array("la", host_play_session_info.get_int_array("la", 4)))
            return root

        self.data.local.lobby.put_lobby(
            self.game,
            self.version,
            userid,
            {
                "ga": play_session_info.get_int_array("ga", 4),
                "gp": play_session_info.get_int("gp"),
                "la": play_session_info.get_int_array("la", 4),
                "matching_class": request.child_value("arena_class"),
                "lobbysize": 4,
                "createtime": Time.now(),
                "participants": [userid],
            },
        )
        lobby = self.data.local.lobby.get_lobby(self.game, self.version, userid)

        root.add_child(Node.bool("host", True))
        root.add_child(Node.s32("matching_class", play_session_info.get_int("matching_class")))
        address = Node.void("address")
        root.add_child(address)
        address.add_child(Node.u8_array("ga", play_session_info.get_int_array("ga", 4)))
        address.add_child(Node.u16("gp", play_session_info.get_int("gp")))
        address.add_child(Node.u8_array("la", play_session_info.get_int_array("la", 4)))

        return root

    def handle_IIDX27lobby_delete_request(self, request: Node) -> Node:
        lobbies = self.data.local.lobby.get_all_lobbies(self.game, self.version)
        for uid, lobby in lobbies:
            if lobby.get_int_array("ga", 4) == request.child_value("address/ga") and lobby.get_int("gp") == request.child_value("address/gp") and lobby.get_int_array("la", 4) == request.child_value("address/la"):
                lobby = self.data.local.lobby.get_lobby(self.game, self.version, uid)
                if lobby is not None:
                    self.data.local.lobby.destroy_lobby(lobby.get_int("id"))

        return Node.void("IIDX27lobby")

    def handle_IIDX27music_getrank_request(self, request: Node) -> Node:
        cltype = int(request.attribute("cltype"))

        root = Node.void("IIDX27music")
        style = Node.void("style")
        root.add_child(style)
        style.set_attribute("type", str(cltype))

        for rivalid in [-1, 0, 1, 2, 3, 4]:
            if rivalid == -1:
                attr = "iidxid"
            else:
                attr = f"iidxid{rivalid}"

            try:
                extid = int(request.attribute(attr))
            except Exception:
                # Invalid extid
                continue
            userid = self.data.remote.user.from_extid(self.game, self.version, extid)
            if userid is not None:
                scores = self.data.remote.music.get_scores(self.game, self.music_version, userid)

                # Grab score data for user/rival
                scoredata = self.make_score_struct(
                    scores,
                    self.CLEAR_TYPE_SINGLE if cltype == self.GAME_CLTYPE_SINGLE else self.CLEAR_TYPE_DOUBLE,
                    rivalid,
                )
                for s in scoredata:
                    root.add_child(Node.s16_array("m", s))

                # if rivalid == -1:
                #     top = Node.void("top")

                # Grab most played for user/rival
                most_played = [
                    play[0] for play in self.data.local.music.get_most_played(self.game, self.music_version, userid, 20)
                ]
                if len(most_played) < 20:
                    most_played.extend([0] * (20 - len(most_played)))
                best = Node.u16_array("best", most_played)
                best.set_attribute("rno", str(rivalid))
                root.add_child(best)

        return root

    def handle_IIDX27music_appoint_request(self, request: Node) -> Node:
        musicid = int(request.attribute("mid"))
        game_chart = int(request.attribute("clid"))
        chart = self.game_to_db_chart(game_chart)
        ghost_type = int(request.attribute("ctype"))
        extid = int(request.attribute("iidxid"))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)

        root = Node.void("IIDX27music")
        if userid is not None:
            ghost_score = self.get_ghost(
                {}.get(ghost_type, self.GHOST_TYPE_NONE),
                request.attribute("subtype"),
                self.GAME_GHOST_LENGTH,
                musicid,
                chart,
                userid,
            )

            if ghost_score is not None:
                sdata = Node.binary("sdata", ghost_score["ghost"])
                root.add_child(sdata)

            my_socre = self.data.remote.music.get_score(self.game, self.music_version, userid, musicid, chart)
            if my_socre is not None:
                root.add_child(Node.binary("mydata", my_socre.data.get_bytes("ghost")))
                root.add_child(Node.binary("my_gauge_data", my_socre.data.get_bytes("ghost_gauge")))

        return root

    def handle_IIDX27music_reg_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        musicid = int(request.attribute("mid"))
        game_chart = int(request.attribute("clid"))
        rankside = int(request.attribute("rankside"))
        userid = self.data.remote.user.from_extid(self.game, self.version, extid)
        chart = self.game_to_db_chart(game_chart)

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
            ghost_gauge = request.child_value("ghost_gauge")
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
                ghost_gauge,
                shopid,
            )

        root = Node.void("IIDX27music")
        root.set_attribute("mid", str(musicid))
        root.set_attribute("clid", str(game_chart))
        root.set_attribute("rankside", str(rankside))

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

        if userid is not None:
            ranklist = Node.void("ranklist")
            root.add_child(ranklist)

            all_scores = sorted(
                self.data.remote.music.get_all_scores(game=self.game, version=self.version, songid=musicid, songchart=chart),
                key=lambda s: (s[1].points, s[1].timestamp),
                reverse=True,
            )
            missing_players = [
                uid for (uid, _) in all_scores
                if uid not in all_players
            ]
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
            relevant_scores = all_scores[start:(end + 1)]

            record_num = start + 1
            ranklist.set_attribute("total_user_num", str(len(relevant_scores)))
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
                data.set_attribute("clflg", str(self.db_to_game_status(score[1].data.get_int("clear_status"))))
                data.set_attribute("pid", str(profile.get_int("pid")))
                data.set_attribute("sgrade", str(
                    self.db_to_game_rank(profile.get_int(self.DAN_RANKING_SINGLE, -1), self.GAME_CLTYPE_SINGLE),
                ))
                data.set_attribute("dgrade", str(
                    self.db_to_game_rank(profile.get_int(self.DAN_RANKING_DOUBLE, -1), self.GAME_CLTYPE_DOUBLE),
                ))
                qpro_dict = profile.get_dict("qpro")
                data.set_attribute("head", str(qpro_dict.get_int("head")))
                data.set_attribute("hair", str(qpro_dict.get_int("hair")))
                data.set_attribute("face", str(qpro_dict.get_int("face")))
                data.set_attribute("body", str(qpro_dict.get_int("body")))
                data.set_attribute("hand", str(qpro_dict.get_int("hand")))

                record_num = record_num + 1

            shopdata = Node.void("shopdata")
            root.add_child(shopdata)
            shopdata.set_attribute("rank", "-1" if oldindex is None else str(oldindex + 1))

        return root

    def handle_IIDX27pc_common_request(self, request: Node) -> Node:
        root = Node.void("IIDX27pc")
        root.set_attribute("expire", "1")

        # Monthly Music Ranking
        root.add_child(Node.u16_array("monthly_mranking", [0] * 20))

        # Total Music Ranking
        root.add_child(Node.u16_array("total_mranking", [0] * 20))

        root.add_child(Node.s32_array("kac_mid", [0] * 30))
        root.add_child(Node.s32_array("kac_clid", [0] * 30))

        ir = Node.void("ir")
        root.add_child(ir)
        ir.set_attribute("beat", "2")

        # Advertisements displayed on the demo screen
        # List: cm_2020kuji, cm_paseli, cm_ultimate
        cm = Node.void("cm")
        root.add_child(cm)
        cm.set_attribute("id", "1")
        cm.set_attribute("folder", "cm_ultimate")
        cm.set_attribute("compo", "cm_ultimate")

        tdj_cm = Node.void("tdj_cm")
        root.add_child(tdj_cm)
        tdj_cms = ["2020kuji.ifs", "paseli.ifs", "ultimate.ifs"]
        for id, filename in enumerate(tdj_cms):
            cm = Node.void("cm")
            tdj_cm.add_child(cm)
            cm.set_attribute("id", str(id + 1))
            cm.set_attribute("filename", filename)

        playvideo_disable_music = Node.void("playvideo_disable_music")
        root.add_child(playvideo_disable_music)

        # Probably a list of music videos to be censored
        music_movie_suspend = Node.void("music_movie_suspend")
        root.add_child(music_movie_suspend)
        censored_music_movie_list = []
        for index, music in enumerate(censored_music_movie_list):
            music = Node.void("music")
            music_movie_suspend.add_child(music)
            music.set_attribute("index", str(index))
            music.set_attribute("music_id", str(music["id"]))
            music.set_attribute("name", str(music["name"]))

        movie_agreement = Node.void("movie_agreement")
        root.add_child(movie_agreement)
        movie_agreement.set_attribute("version", "1")

        escape_package_info = Node.void("escape_package_info")
        root.add_child(escape_package_info)

        boss = Node.void("boss")
        root.add_child(boss)
        boss.set_attribute("phase", "1")

        root.add_child(Node.void("vip_pass_black"))

        deller_bonus = Node.void("deller_bonus")
        root.add_child(deller_bonus)
        deller_bonus.set_attribute("open", "1")

        newsong_another = Node.void("newsong_another")
        root.add_child(newsong_another)
        newsong_another.set_attribute("open", "1")

        pcb_check = Node.void("pcb_check")
        root.add_child(pcb_check)
        pcb_check.set_attribute("flg", "1")

        eaorder_phase = Node.void("eaorder_phase")
        root.add_child(eaorder_phase)
        eaorder_phase.set_attribute("phase", "1")

        common_evnet = Node.void("common_evnet")
        root.add_child(common_evnet)
        common_evnet.set_attribute("flg", "0")

        system_voice_phase = Node.void("system_voice_phase")
        root.add_child(system_voice_phase)
        system_voice_phase.set_attribute("phase", "0")

        # SHADOW REVELLION event
        extra_boss_event = Node.void("extra_boss_event")
        root.add_child(extra_boss_event)
        extra_boss_event.set_attribute("phase", "0")

        event1_phase = Node.void("event1_phase")
        root.add_child(event1_phase)
        event1_phase.set_attribute("phase", "1")

        premium_area_news = Node.void("premium_area_news")
        root.add_child(premium_area_news)
        premium_area_news.set_attribute("open", "1")

        premium_area_qpro = Node.void("premium_area_qpro")
        root.add_child(premium_area_qpro)
        premium_area_qpro.set_attribute("open", "1")

        root.add_child(Node.void("display_asio_logo"))

        return root

    def handle_IIDX27pc_delete_request(self, request: Node) -> Node:
        return Node.void("IIDX27pc")

    def handle_IIDX27pc_oldget_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        userid = self.data.remote.user.from_refid(self.game, self.version, refid)
        if userid is not None:
            oldversion = self.previous_version()
            profile = oldversion.get_profile(userid)
        else:
            profile = None

        root = Node.void("IIDX27pc")
        root.set_attribute("status", "1" if profile is None else "0")
        return root

    def handle_IIDX27pc_get_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        root = self.get_profile_by_refid(refid)
        if root is None:
            root = Node.void("IIDX27pc")
        return root

    def handle_IIDX27pc_reg_request(self, request: Node) -> Node:
        refid = request.attribute("rid")
        name = request.attribute("name")
        pid = int(request.attribute("pid"))
        profile = self.new_profile_by_refid(refid, name, pid)

        root = Node.void("IIDX27pc")
        if profile is not None:
            root.set_attribute("id", str(profile.extid))
            root.set_attribute("id_str", ID.format_extid(profile.extid))
        return root

    def handle_IIDX27pc_visit_request(self, request: Node) -> Node:
        root = Node.void("IIDX27pc")
        root.set_attribute("anum", "0")
        root.set_attribute("snum", "0")
        root.set_attribute("pnum", "0")
        root.set_attribute("aflg", "0")
        root.set_attribute("sflg", "0")
        root.set_attribute("pflg", "0")
        return root

    def handle_IIDX27pc_save_request(self, request: Node) -> Node:
        extid = int(request.attribute("iidxid"))
        self.put_profile_by_extid(extid, request)

        return Node.void("IIDX27pc")

    def format_profile(self, userid: UserID, profile: Profile) -> Node:
        root = Node.void("IIDX27pc")

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
        pcdata.set_attribute("pmode", str(profile.get_int("pmode")))
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
        lightning_setting.add_child(Node.s32_array("slider", lightning_setting_dict.get_int_array("slider", 7, [7, 7, 7, 7, 7, 15, 15])))
        lightning_setting.add_child(Node.bool_array("light", lightning_setting_dict.get_bool_array("light", 6, [True] * 6)))
        lightning_setting.add_child(Node.bool("concentration", lightning_setting_dict.get_bool("concentration", False)))

        # Weekly Ranking 획득 스타 수
        weekly_achieve = Node.void("weekly_achieve")
        root.add_child(weekly_achieve)
        weekly_achieve.set_attribute("weekly_achieve_0", "0")
        weekly_achieve.set_attribute("weekly_achieve_1", "0")
        weekly_achieve.set_attribute("weekly_achieve_2", "0")
        weekly_achieve.set_attribute("weekly_achieve_3", "0")
        weekly_achieve.set_attribute("weekly_achieve_4", "0")

        # What is this?
        # spdp_rival = Node.void("spdp_rival")
        # root.add_child(spdp_rival)
        # spdp_rival.set_attribute("flg", "-1")

        root.add_child(Node.void("bind_eaappli"))

        root.add_child(Node.void("ea_premium_course"))

        root.add_child(Node.void("enable_qr_reward"))

        kac_entry_info = Node.void("kac_entry_info")
        root.add_child(kac_entry_info)
        # kac_entry_info.add_child(Node.void("enable_kac_deller"))
        # kac_entry_info.add_child(Node.void("disp_kac_mark"))
        # kac_entry_info.add_child(Node.void("is_kac_entry"))
        # kac_entry_info.add_child(Node.void("is_kac_evnet_entry"))
        kac_secret_musics = [27080, 27052]  # ランカーキラーガール, SCREW // owo // SCREW
        kac_secret_music = Node.void("kac_secret_music")
        kac_entry_info.add_child(kac_secret_music)
        for index, musicid in enumerate(kac_secret_musics):
            music_info = Node.void("music_info")
            kac_secret_music.add_child(music_info)
            music_info.set_attribute("index", str(index))
            music_info.set_attribute("music_id", str(musicid))

        leggendaria_open = Node.void("leggendaria_open")
        root.add_child(leggendaria_open)

        secret = Node.void("secret")
        root.add_child(secret)
        secret.add_child(Node.s64_array("flg1", [0] * 3))
        secret.add_child(Node.s64_array("flg2", [0] * 3))
        secret.add_child(Node.s64_array("flg3", [0] * 3))
        secret.add_child(Node.s64_array("flg4", [0] * 3))

        favorite = Node.void("favorite")
        root.add_child(favorite)
        favorite.add_child(Node.binary("sp_mlist", b"\x00"))
        favorite.add_child(Node.binary("sp_clist", b"\x00"))
        favorite.add_child(Node.binary("dp_mlist", b"\x00"))
        favorite.add_child(Node.binary("dp_clist", b"\x00"))

        # extra_favorite

        qpro_secret_dict = profile.get_dict("qpro_secret")
        qpro_secret = Node.void("qpro_secret")
        root.add_child(qpro_secret)
        qpro_secret.add_child(Node.s64_array("head", qpro_secret_dict.get_int_array("head", 5)))
        qpro_secret.add_child(Node.s64_array("hair", qpro_secret_dict.get_int_array("hair", 5)))
        qpro_secret.add_child(Node.s64_array("face", qpro_secret_dict.get_int_array("face", 5)))
        qpro_secret.add_child(Node.s64_array("body", qpro_secret_dict.get_int_array("body", 5)))
        qpro_secret.add_child(Node.s64_array("hand", qpro_secret_dict.get_int_array("hand", 5)))

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

        # Eternal Rank (Lightming model only)
        eisei_grade = Node.void("eisei_grade")
        root.add_child(eisei_grade)

        # User settings
        settings_dict = profile.get_dict("settings")
        root.add_child(
            Node.s16_array(
                "skin",
                [
                    settings_dict.get_int("frame"),
                    settings_dict.get_int("turntable"),
                    settings_dict.get_int("burst"),
                    settings_dict.get_int("bgm"),
                    settings_dict.get_int("flags"),
                    settings_dict.get_int("towel"),
                    settings_dict.get_int("judge_pos"),
                    settings_dict.get_int("voice"),
                    settings_dict.get_int("noteskin"),
                    settings_dict.get_int("full_combo"),
                    settings_dict.get_int("beam"),
                    settings_dict.get_int("judge"),
                    0,
                    settings_dict.get_int("disable_song_preview"),
                    settings_dict.get_int("pacemaker"),
                    settings_dict.get_int("effector_lock"),
                    settings_dict.get_int("effector_preset"),
                    settings_dict.get_int("explosion_size"),
                    settings_dict.get_int("disable_hcn_color"),
                    settings_dict.get_int("note_preview"),
                ]
            )
        )

        # Qpro data
        qpro_dict = profile.get_dict("qpro")
        root.add_child(
            Node.u32_array(
                "qprodata",
                [
                    qpro_dict.get_int("head"),
                    qpro_dict.get_int("hair"),
                    qpro_dict.get_int("face"),
                    qpro_dict.get_int("hand"),
                    qpro_dict.get_int("body"),
                ],
            )
        )

        rlist = Node.void("rlist")
        root.add_child(rlist)

        # DJ RANK
        for dj_rank in achievements:
            if dj_rank.type != "dj_rank":
                continue

            dj_rank_node = Node.void("dj_rank")
            root.add_child(dj_rank_node)
            dj_rank_node.set_attribute("style", str(dj_rank.id))
            dj_rank_node.add_child(Node.s32_array("rank", dj_rank.data.get_int_array("rank", 15)))
            dj_rank_node.add_child(Node.s32_array("point", dj_rank.data.get_int_array("point", 15)))

        for style in (0, 1):
            dj_rank_ranking_node = Node.void("dj_rank_ranking")
            root.add_child(dj_rank_ranking_node)
            dj_rank_ranking_node.set_attribute("style", str(style))
            for j in range(15):
                detail = Node.void("detail")
                dj_rank_ranking_node.add_child(detail)
                detail.set_attribute("category", str(j))
                detail.set_attribute("total_user", "0")
                detail.set_attribute("rank", "0")
                detail.set_attribute("platinum_point", "0")
                detail.set_attribute("platinum_rank", "0")
                detail.set_attribute("gold_point", "0")
                detail.set_attribute("gold_rank", "0")
                detail.set_attribute("silver_point", "0")
                detail.set_attribute("silver_rank", "0")
                detail.set_attribute("bronze_point", "0")
                detail.set_attribute("bronze_rank", "0")
                detail.set_attribute("white_point", "0")
                detail.set_attribute("white_rank", "0")

        for notes_radar in achievements:
            if notes_radar.type != 'notes_radar':
                continue
            notes_radar_node = Node.void("notes_radar")
            root.add_child(notes_radar_node)
            notes_radar_node.set_attribute("style", str(notes_radar.id))
            notes_radar_node.add_child(Node.s32_array("radar_score", notes_radar.data.get_int_array('radar_score', 6)))

        tonjyutsu_dict = profile.get_dict("tonjyutsu")
        tonjyutsu = Node.void("tonjyutsu")
        root.add_child(tonjyutsu)
        tonjyutsu.set_attribute("platinum_pass", str(tonjyutsu_dict.get_int("platinum_pass")))
        tonjyutsu.set_attribute("black_pass", str(tonjyutsu_dict.get_int("black_pass")))

        # shitei

        # weekly

        # weekly_score

        # join_shop

        # visitor

        step_dict = profile.get_dict("step")
        step = Node.void("step")
        root.add_child(step)
        step.set_attribute("enemy_damage", str(step_dict.get_int("enemy_damage")))
        step.set_attribute("progress", str(step_dict.get_int("progress")))
        step.set_attribute("sp_level", str(step_dict.get_int("sp_level")))
        step.set_attribute("dp_level", str(step_dict.get_int("dp_level")))
        step.set_attribute("sp_mission_point", str(step_dict.get_int("sp_mission_point")))
        step.set_attribute("dp_mission_point", str(step_dict.get_int("dp_mission_point")))
        step.set_attribute("sp_dj_mission_level", str(step_dict.get_int("sp_dj_mission_level")))
        step.set_attribute("dp_dj_mission_level", str(step_dict.get_int("dp_dj_mission_level")))
        step.set_attribute("sp_clear_mission_level", str(step_dict.get_int("sp_clear_mission_level")))
        step.set_attribute("dp_clear_mission_level", str(step_dict.get_int("dp_clear_mission_level")))
        step.set_attribute("sp_dj_mission_clear", str(step_dict.get_int("sp_dj_mission_clear")))
        step.set_attribute("dp_dj_mission_clear", str(step_dict.get_int("dp_dj_mission_clear")))
        step.set_attribute("sp_clear_mission_clear", str(step_dict.get_int("sp_clear_mission_clear")))
        step.set_attribute("dp_clear_mission_clear", str(step_dict.get_int("dp_clear_mission_clear")))
        step.set_attribute("sp_mplay", str(step_dict.get_int("sp_mplay")))
        step.set_attribute("dp_mplay", str(step_dict.get_int("dp_mplay")))
        step.set_attribute("tips_read_list", str(step_dict.get_int("tips_read_list")))
        step.add_child(Node.bool("is_track_ticket", step_dict.get_bool("is_track_ticket")))

        # Daily recommendations
        entry = self.data.local.game.get_time_sensitive_settings(self.game, self.version, "dailies")
        if entry is not None:
            packinfo = Node.void("packinfo")
            root.add_child(packinfo)

            pack_id = int(entry["start_time"] / 86400)
            packinfo.set_attribute("pack_id", str(pack_id))
            packinfo.set_attribute("music_0", str(entry["music"][0]))
            packinfo.set_attribute("music_1", str(entry["music"][1]))
            packinfo.set_attribute("music_2", str(entry["music"][2]))
        else:
            # No dailies :(
            pack_id = None

        # Tran medals and shit
        achievement_node = Node.void("achievements")
        root.add_child(achievement_node)

        # Dailies
        if pack_id is None:
            achievement_node.set_attribute("pack", "0")
            achievement_node.set_attribute("pack_comp", "0")
        else:
            daily_played = self.data.local.user.get_achievement(self.game, self.version, userid, pack_id, "daily")
            if daily_played is None:
                daily_played = ValidatedDict()
            achievement_node.set_attribute("pack", str(daily_played.get_int("pack_flg")))
            achievement_node.set_attribute("pack_comp", str(daily_played.get_int("pack_comp")))

        # Weeklies
        achievement_node.set_attribute("last_weekly", str(profile.get_int("last_weekly")))
        achievement_node.set_attribute("weekly_num", str(profile.get_int("weekly_num")))

        # Prefecture visit flag
        achievement_node.set_attribute("visit_flg", str(profile.get_int("visit_flg")))

        # Number of rivals beaten
        achievement_node.set_attribute("rival_crush", str(profile.get_int("rival_crush")))

        # Tran medals
        achievement_node.add_child(Node.s64_array("trophy", profile.get_int_array("trophy", 20)))

        # Track deller
        deller = Node.void("deller")
        root.add_child(deller)
        deller.set_attribute("deller", str(profile.get_int("deller")))
        deller.set_attribute("rate", "0")

        # Orb data
        orb_data = Node.void("orb_data")
        root.add_child(orb_data)
        orb_data.set_attribute("rest_orb", str(profile.get_int("orbs")))
        orb_data.set_attribute("present_orb", str(profile.get_int("present_orb")))

        # expert_point

        # This seems to be a dummy function
        pay_per_use_item = Node.void("pay_per_use_item")
        root.add_child(pay_per_use_item)
        pay_per_use_item.set_attribute("item_num", "0")
        present_pay_per_use_item = Node.void("present_pay_per_use_item")
        root.add_child(present_pay_per_use_item)
        present_pay_per_use_item.set_attribute("item_num", "0")

        old_linkage_secret_flg = Node.void("old_linkage_secret_flg")
        root.add_child(old_linkage_secret_flg)
        old_linkage_secret_flg.set_attribute("floor_infection2", "-1")
        old_linkage_secret_flg.set_attribute("floor_infection3", "-1")
        old_linkage_secret_flg.set_attribute("bemani_vote", "-1")

        leggendaria_semi_open = Node.void("leggendaria_semi_open")
        root.add_child(leggendaria_semi_open)
        leggendaria_semi_open.set_attribute("flg", "1")

        arena_data = Node.void("arena_data")
        root.add_child(arena_data)
        arena_data.set_attribute("play_num", "0")
        arena_data.set_attribute("play_num_sp", "0")
        arena_data.set_attribute("play_num_dp", "0")
        # achieve_data = Node.void("achieve_data")
        # arena_data.add_child(achieve_data)
        # achieve_data.set_attribute("play_style", "0")
        # achieve_data.set_attribute("arena_class", "0")
        # achieve_data.set_attribute("rating_value", "0")
        # achieve_data.set_attribute("now_top_class_continuing", "0")
        # achieve_data.set_attribute("best_top_class_continuing", "0")

        tsujigiri_dict = profile.get_dict("tsujigiri")
        tsujigiri = Node.void("tsujigiri")
        root.add_child(tsujigiri)
        tsujigiri.set_attribute("total_num_sp", str(tsujigiri_dict.get_int("total_num_sp")))
        tsujigiri.set_attribute("total_num_dp", str(tsujigiri_dict.get_int("total_num_dp")))

        skin_customize_flg = Node.void("skin_customize_flg")
        root.add_child(skin_customize_flg)
        skin_customize_flg.set_attribute("skin_frame_flg", "0")
        skin_customize_flg.set_attribute("skin_bgm_flg", "0")

        event1_dict = profile.get_dict("event1")
        event1 = Node.void("event1")
        root.add_child(event1)
        event1.set_attribute("event_play_num", str(event1_dict.get_int("event_play_num")))
        event1.set_attribute("last_select_gym_id", str(event1_dict.get_int("last_select_gym")))
        for gym_data in achievements:
            if gym_data.type != "gym_data":
                continue

            gym_data_node = Node.void("gym_data")
            event1.add_child(gym_data_node)
            gym_data_node.set_attribute("gym_id", str(gym_data.id))
            gym_data_node.set_attribute("play_num", str(gym_data.data.get_int("play_num")))
            gym_data_node.set_attribute("gauge_spirit", str(gym_data.data.get_int("gauge_spirit")))
            gym_data_node.set_attribute("gauge_technique", str(gym_data.data.get_int("gauge_technique")))
            gym_data_node.set_attribute("gauge_body", str(gym_data.data.get_int("gauge_body")))
            gym_data_node.set_attribute("boss_attack_num", str(gym_data.data.get_int("boss_attack_num")))
            gym_data_node.set_attribute("boss_damage", str(gym_data.data.get_int("boss_damage")))
            gym_data_node.set_attribute("disp_lounge_list", str(gym_data.data.get_int("disp_lounge_list")))
            gym_data_node.set_attribute("stb_type", str(gym_data.data.get_int("stb_type")))
            gym_data_node.add_child(Node.bool("is_complete", gym_data.data.get_bool("is_complete")))
            gym_data_node.add_child(Node.bool("is_gauge_max", gym_data.data.get_bool("is_gauge_max")))

        floor_infection4 = Node.void("floor_infection4")
        root.add_child(floor_infection4)
        floor_infection4.set_attribute("music_list", "-1")

        bemani_vote = Node.void("bemani_vote")
        root.add_child(bemani_vote)
        bemani_vote.set_attribute("music_list", "-1")

        bemani_janken_meeting = Node.void("bemani_janken_meeting")
        root.add_child(bemani_janken_meeting)
        bemani_janken_meeting.set_attribute("music_list", "-1")

        bemani_rush = Node.void("bemani_rush")
        root.add_child(bemani_rush)
        bemani_rush.set_attribute("music_list_ichika", "-1")
        bemani_rush.set_attribute("music_list_nono", "-1")

        ultimate_mobile_link = Node.void("ultimate_mobile_link")
        root.add_child(ultimate_mobile_link)
        ultimate_mobile_link.set_attribute("music_list", "-1")

        player_compe = Node.void("player_compe")
        root.add_child(player_compe)

        news = Node.void("news")
        root.add_child(news)

        news_data_all = Node.void("news_data_all")
        news.add_child(news_data_all)
        news_data_all.set_attribute("last_read_time", str(Time.now()))
        news_data_shop = Node.void("news_data_shop")
        news.add_child(news_data_shop)
        news_data_shop.set_attribute("last_read_time", str(Time.now()))
        news_data_grade = Node.void("news_data_grade")
        news.add_child(news_data_grade)
        news_data_grade.set_attribute("last_read_time", str(Time.now()))
        news_data_rival = Node.void("news_data_rival")
        news.add_child(news_data_rival)
        news_data_rival.set_attribute("last_read_time", str(Time.now()))
        news_data_all_top = Node.void("news_data_all_top")
        news.add_child(news_data_all_top)
        news_data_all_top.set_attribute("last_read_time", str(Time.now()))
        news_data_area_top = Node.void("news_data_area_top")
        news.add_child(news_data_area_top)
        news_data_area_top.set_attribute("last_read_time", str(Time.now()))
        news_data_shop_top = Node.void("news_data_shop_top")
        news.add_child(news_data_shop_top)
        news_data_shop_top.set_attribute("last_read_time", str(Time.now()))

        # detail = Node.void("detail")
        # news_data_all.add_child(detail)
        # detail.set_attribute("music_id", "1000")
        # detail.set_attribute("class_id", "0")
        # detail.set_attribute("news_type", "0")
        # detail.set_attribute("news_data", "4")  # 1 - Failed, 2 - Assist Clear, 3 - Clear, 4
        # detail.set_attribute("news_time", str(Time.now()))
        # detail.set_attribute("dj_name", "TEST")

        language_setting = Node.void("language_setting")
        root.add_child(language_setting)
        language_setting.set_attribute("language", str(profile.get_int("language")))

        movie_agreement = Node.void("movie_agreement")
        root.add_child(movie_agreement)
        movie_agreement.set_attribute("agreement_version", "1")

        # SHADOW REVELLION event
        extra_boss_event_dict = profile.get_dict("extra_boss_event")
        extra_boss_event = Node.void("extra_boss_event")
        root.add_child(extra_boss_event)
        extra_boss_event.set_attribute("key_orb", str(extra_boss_event_dict.get_int("key_orb")))
        extra_boss_event.set_attribute("boss_orb_0", str(extra_boss_event_dict.get_int("boss_orb_0")))
        extra_boss_event.set_attribute("boss_orb_1", str(extra_boss_event_dict.get_int("boss_orb_1")))
        extra_boss_event.set_attribute("boss_orb_2", str(extra_boss_event_dict.get_int("boss_orb_2")))
        extra_boss_event.set_attribute("boss_orb_3", str(extra_boss_event_dict.get_int("boss_orb_3")))
        extra_boss_event.set_attribute("boss_orb_4", str(extra_boss_event_dict.get_int("boss_orb_4")))
        extra_boss_event.set_attribute("boss_orb_5", str(extra_boss_event_dict.get_int("boss_orb_5")))
        extra_boss_event.set_attribute("boss_orb_6", str(extra_boss_event_dict.get_int("boss_orb_6")))
        extra_boss_event.set_attribute("boss_orb_7", str(extra_boss_event_dict.get_int("boss_orb_7")))

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
        if "s_lift" in request.attributes:
            newprofile.replace_int("s_lift", int(request.attribute("s_lift")))
        if "d_lift" in request.attributes:
            newprofile.replace_int("d_lift", int(request.attribute("d_lift")))
        newprofile.replace_int("mode", int(request.attribute("mode")))
        newprofile.replace_int("pmode", int(request.attribute("pmode")))
        newprofile.replace_int("rtype", int(request.attribute("rtype")))

        # Update judge window adjustments per-machine
        judge_dict = newprofile.get_dict("machine_judge_adjust")
        machine_judge = judge_dict.get_dict(self.config.machine.pcbid)
        machine_judge.replace_int("single", int(request.attribute("s_judgeAdj")))
        machine_judge.replace_int("double", int(request.attribute("d_judgeAdj")))
        judge_dict.replace_dict(self.config.machine.pcbid, machine_judge)
        newprofile.replace_dict("machine_judge_adjust", judge_dict)

        lightning_play_data = request.child("lightning_play_data")
        if lightning_play_data is not None:
            if cltype == self.GAME_CLTYPE_SINGLE:
                play_stats.increment_int("lightning_single_plays")
            if cltype == self.GAME_CLTYPE_DOUBLE:
                play_stats.increment_int("lightning_double_plays")

        lightning_setting = request.child("lightning_setting")
        if lightning_setting is not None:
            lightning_setting_dict = newprofile.get_dict("lightning_setting")
            lightning_setting_dict.replace_int("headphone_vol", int(lightning_setting.attribute("headphone_vol")))
            lightning_setting_dict.replace_int("resistance_sp_left", int(lightning_setting.attribute("resistance_sp_left")))
            lightning_setting_dict.replace_int("resistance_sp_right", int(lightning_setting.attribute("resistance_sp_right")))
            lightning_setting_dict.replace_int("resistance_dp_left", int(lightning_setting.attribute("resistance_dp_left")))
            lightning_setting_dict.replace_int("resistance_dp_right", int(lightning_setting.attribute("resistance_dp_right")))
            lightning_setting_dict.replace_int_array("slider", 7, lightning_setting.child_value("slider"))
            lightning_setting_dict.replace_bool_array("light", 6, lightning_setting.child_value("light"))
            lightning_setting_dict.replace_bool("concentration", lightning_setting.child_value("concentration"))
            newprofile.replace_dict("lightning_setting", lightning_setting_dict)

        secret = request.child("secret")
        if secret is not None:
            secret_dict = newprofile.get_dict("secret")
            secret_dict.replace_int_array("flg1", 3, secret.child_value("flg1"))
            secret_dict.replace_int_array("flg2", 3, secret.child_value("flg2"))
            secret_dict.replace_int_array("flg3", 3, secret.child_value("flg3"))
            secret_dict.replace_int_array("flg4", 3, secret.child_value("flg4"))
            newprofile.replace_dict("secret", secret_dict)

        # favorite

        # extra_favorite

        # playlist

        qpro_secret = request.child("qpro_secret")
        if qpro_secret is not None:
            qpro_secret_dict = newprofile.get_dict("qpro_secret")
            qpro_secret_dict.replace_int_array("head", 5, qpro_secret.child_value("head"))
            qpro_secret_dict.replace_int_array("hair", 5, qpro_secret.child_value("hair"))
            qpro_secret_dict.replace_int_array("face", 5, qpro_secret.child_value("face"))
            qpro_secret_dict.replace_int_array("body", 5, qpro_secret.child_value("body"))
            qpro_secret_dict.replace_int_array("hand", 5, qpro_secret.child_value("hand"))
            newprofile.replace_dict("qpro_secret", qpro_secret_dict)

        step = request.child("step")
        if step is not None:
            step_dict = newprofile.get_dict("step")
            step_dict.replace_int("enemy_damage", int(step.attribute("enemy_damage")))
            step_dict.replace_int("progress", int(step.attribute("progress")))
            step_dict.replace_bool("is_track_ticket", step.child_value("is_track_ticket"))
            step_dict.replace_int("sp_level", int(step.attribute("sp_level")))
            step_dict.replace_int("dp_level", int(step.attribute("dp_level")))
            step_dict.replace_int("sp_mission_point", int(step.attribute("sp_mission_point")))
            step_dict.replace_int("dp_mission_point", int(step.attribute("dp_mission_point")))
            step_dict.replace_int("sp_dj_mission_level", int(step.attribute("sp_dj_mission_level")))
            step_dict.replace_int("dp_dj_mission_level", int(step.attribute("dp_dj_mission_level")))
            step_dict.replace_int("sp_clear_mission_level", int(step.attribute("sp_clear_mission_level")))
            step_dict.replace_int("dp_clear_mission_level", int(step.attribute("dp_clear_mission_level")))
            step_dict.replace_int("sp_dj_mission_clear", int(step.attribute("sp_dj_mission_clear")))
            step_dict.replace_int("dp_dj_mission_clear", int(step.attribute("dp_dj_mission_clear")))
            step_dict.replace_int("sp_clear_mission_clear", int(step.attribute("sp_clear_mission_clear")))
            step_dict.replace_int("dp_clear_mission_clear", int(step.attribute("dp_clear_mission_clear")))
            step_dict.replace_int("sp_mplay", int(step.attribute("sp_mplay")))
            step_dict.replace_int("dp_mplay", int(step.attribute("dp_mplay")))
            step_dict.replace_int("tips_read_list", int(step.attribute("tips_read_list")))

        achievements = request.child("achievements")
        if achievements is not None:
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

            trophies = achievements.child("trophy")
            if trophies is not None:
                newprofile.replace_int_array("trophy", 20, trophies.value[:20])

        # expert_point

        for dj_rank in request.children:
            if dj_rank.name != "dj_rank":
                continue

            rankid = int(dj_rank.attribute("style"))
            rank = dj_rank.child_value("rank")
            point = dj_rank.child_value("point")

            self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                rankid,
                "dj_rank",
                {
                    "rank": rank,
                    "point": point,
                },
            )

        for notes_radar in request.children:
            if notes_radar.name != 'notes_radar':
                continue

            rankid = int(notes_radar.attribute("style"))
            score = notes_radar.child_value("radar_score")

            self.data.local.user.put_achievement(
                self.game,
                self.version,
                userid,
                rankid,
                "notes_radar",
                {
                    "radar_score": score,
                },
            )

        tonjyutsu = request.child("tonjyutsu")
        if tonjyutsu is not None:
            tonjyutsu_dict = newprofile.get_dict("tonjyutsu")
            tonjyutsu_dict.replace_int("platinum_pass", int(tonjyutsu.attribute("platinum_pass")))
            tonjyutsu_dict.replace_int("black_pass", int(tonjyutsu.attribute("black_pass")))
            newprofile.replace_dict("tonjyutsu", tonjyutsu_dict)

        # shitei

        deller = request.child("deller")
        if deller is not None:
            newprofile.replace_int("deller", newprofile.get_int("deller") + int(deller.attribute("deller")))

        orb_data = request.child("orb_data")
        if orb_data is not None:
            orbs = newprofile.get_int("orbs")
            orbs = orbs + int(orb_data.attribute("add_orb"))
            if orb_data.child_value("use_vip_pass"):
                orbs = 0
            newprofile.replace_int("orbs", orbs)

        # pay_per_use_item

        # present_pay_per_use_item

        # qpro_ticket

        # pay_money_data

        # leggendaria_semi_open

        # konami_style

        # arena_data

        # arena_log

        # music_history

        # qr_window

        tsujigiri = request.child("tsujigiri")
        if tsujigiri is not None:
            tsujigiri_dict = newprofile.get_dict("tsujigiri")
            tsujigiri_dict.replace_int("total_num_sp", int(tsujigiri.attribute("total_num_sp")))
            tsujigiri_dict.replace_int("total_num_dp", int(tsujigiri.attribute("total_num_dp")))
            newprofile.replace_dict("tsujigiri", tsujigiri_dict)

        # tsujigiri_hidden_chara

        # play_log

        # coin_option

        # weekly_result

        # skin_customize_flg

        # news

        language_setting = request.child("language_setting")
        if language_setting is not None:
            newprofile.replace_int("language", int(language_setting.attribute("language")))

        movie_agreement = request.child("movie_agreement")
        if movie_agreement is not None:
            newprofile.replace_int("movie_agreement", int(movie_agreement.attribute("agreement_version")))

        # hero_ranking_data

        extra_boss_event = request.child("extra_boss_event")
        if extra_boss_event is not None:
            extra_boss_event_dict = newprofile.get_dict("extra_boss_event")
            extra_boss_event_dict.replace_int("key_orb", int(extra_boss_event.attribute("key_orb")))
            extra_boss_event_dict.replace_int("boss_orb_0", int(extra_boss_event.attribute("boss_orb_0")))
            extra_boss_event_dict.replace_int("boss_orb_1", int(extra_boss_event.attribute("boss_orb_1")))
            extra_boss_event_dict.replace_int("boss_orb_2", int(extra_boss_event.attribute("boss_orb_2")))
            extra_boss_event_dict.replace_int("boss_orb_3", int(extra_boss_event.attribute("boss_orb_3")))
            extra_boss_event_dict.replace_int("boss_orb_4", int(extra_boss_event.attribute("boss_orb_4")))
            extra_boss_event_dict.replace_int("boss_orb_5", int(extra_boss_event.attribute("boss_orb_5")))
            extra_boss_event_dict.replace_int("boss_orb_6", int(extra_boss_event.attribute("boss_orb_6")))
            extra_boss_event_dict.replace_int("boss_orb_7", int(extra_boss_event.attribute("boss_orb_7")))
            newprofile.replace_dict("extra_boss_event", extra_boss_event_dict)

        event1 = request.child("event1")
        if event1 is not None:
            last_select_gym = int(event1.attribute("last_select_gym_id"))
            event1_dict = newprofile.get_dict("event1")
            event1_dict.increment_int("event_play_num")
            event1_dict.replace_int("last_select_gym", last_select_gym)

            for gym_data in event1.children:
                if gym_data.name != "gym_data":
                    continue

                gymid = int(gym_data.attribute("gym_id"))
                play_num = int(gym_data.attribute("play_num"))
                is_complete = gym_data.child_value("is_complete") or False
                is_gauge_max = gym_data.child_value("is_gauge_max") or False
                gauge_spirit = int(gym_data.attribute("gauge_spirit"))
                gauge_technique = int(gym_data.attribute("gauge_technique"))
                gauge_body = int(gym_data.attribute("gauge_body"))
                boss_attack_num = int(gym_data.attribute("boss_attack_num"))
                boss_damage = int(gym_data.attribute("boss_damage"))
                disp_lounge_list = int(gym_data.attribute("disp_lounge_list"))
                stb_type = int(gym_data.attribute("stb_type"))

                self.data.local.user.put_achievement(
                    self.game,
                    self.version,
                    userid,
                    gymid,
                    "gym_data",
                    {
                        "play_num": play_num,
                        "gauge_spirit": gauge_spirit,
                        "gauge_technique": gauge_technique,
                        "gauge_body": gauge_body,
                        "boss_attack_num": boss_attack_num,
                        "boss_damage": boss_damage,
                        "disp_lounge_list": disp_lounge_list,
                        "stb_type": stb_type,
                        "is_complete": is_complete,
                        "is_gauge_max": is_gauge_max,
                    }
                )

                if is_complete:
                    last_select_gym = max(last_select_gym, gymid + 1)

            event1_dict.replace_int("last_select_gym", last_select_gym)
            newprofile.replace_dict("event1", event1_dict)

        self.update_play_statistics(userid, play_stats)

        return newprofile
