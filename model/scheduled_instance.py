from typing import List, Literal, Dict, Union
from .base_node import *
from .timing import Timing

class ScheduledInstance(NodeId):
  timelineId: Union[str, None] = None
  timelineExitId: Union[str, None] = None
  defaultConditionId: Union[str, None] = None
  epochId: Union[str, None] = None
  instanceType: Literal['ScheduledInstance']

class ScheduledActivityInstance(ScheduledInstance):
  activityIds: List[str] = []
  encounterId: Union[str, None] = None
  instanceType: Literal['ScheduledActivityInstance']

class ScheduledDecisionInstance(ScheduledInstance):
  conditionAssignments: Dict[str, str]
  instanceType: Literal['ScheduledDecisionInstance']
