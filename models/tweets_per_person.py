#Native modules
from email.policy import default
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, List

#Pydantic modules
from pydantic import BaseModel
from pydantic import Field

class TweetsPerPerson(BaseModel):
    relation : Dict[UUID, Optional[List[UUID]]] = Field(
        ...,
        default = []
    )
