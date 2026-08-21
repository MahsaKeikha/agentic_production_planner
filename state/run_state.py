from dataclasses import dataclass,field
@dataclass
class RunState:
 status:str="created"
 artifacts:list=field(default_factory=list)