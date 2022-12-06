from typing import List, Set

from tealer.detectors.abstract_detector import (
    AbstractDetector,
    DetectorClassification,
    DetectorType,
)
from tealer.teal.basic_blocks import BasicBlock
from tealer.teal.teal import Teal

class DeadCode(AbstractDetector):  # pylint: disable=too-few-public-methods

    NAME = "deadCode"
    DESCRIPTION = "Detect dead code"
    TYPE = DetectorType.STATELESS

    IMPACT = DetectorClassification.OPTIMIZATION
    CONFIDENCE = DetectorClassification.HIGH

    WIKI_TITLE = "Dead code"
    WIKI_DESCRIPTION = "Detect basic blocks that will never be executed"
    WIKI_EXPLOIT_SCENARIO = """
Dead code costs space for the blockchain and will increase the deployment cost
of the contract.
"""

    WIKI_RECOMMENDATION = """
Remove every piece of code flagged as dead.
"""

    def _check_dead_code(
        self,
        bb: BasicBlock,
        visited: Set[BasicBlock],
    ) -> None:
        if bb in visited:
            return
        visited.add(bb)

        for next_bb in bb.next:
            self._check_dead_code(next_bb, visited)

    def detect(self) -> "SupportedOutput":

        visited = set()
        self._check_dead_code(self.teal.bbs[0], visited)
        dead = [bb for bb in self.teal.bbs if bb not in visited]

        if dead:
            dead = [dead]

        filename = "dead-code"
        description = "Dead code found\n"
        description += f"\tConsider removing the code highlighted on {filename}\n"

        return self.generate_result(dead, description, filename)
