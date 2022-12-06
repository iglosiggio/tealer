from typing import List, Set

from tealer.detectors.abstract_detector import AbstractDetector, DetectorType
from tealer.teal.basic_blocks import BasicBlock
from tealer.teal.teal import Teal

class DeadCode(AbstractDetector):  # pylint: disable=too-few-public-methods

    NAME = "deadCode"
    DESCRIPTION = "Detect dead code"
    TYPE = DetectorType.STATELESS

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

    def detect(self) -> List[str]:

        visited = set()
        self._check_dead_code(self.teal.bbs[0], visited)
        dead = [bb for bb in self.teal.bbs if bb not in visited]

        if not dead:
            return []

        filename = f"{self.program_sanitized}.dead_code.dot"
        description = "Dead code found\n"
        description += f"\tConsider removing the code highlighted on {filename}\n"

        self.teal.bbs_to_dot(filename, dead)

        return [description]
