from pydantic import BaseModel, validator
from datetime import datetime

class Task(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    description: str
    
    @validator('end_time')
    def validate_start_end_time(cls, v, values, **kwargs):
        if 'start_time' in values and v < values['start_time']:
            raise ValueError("end_time must be greater than start_time")
        return v


    def __str__(self):
        return f"Task ID: {self.id}, Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}, End Time: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}, Description: {self.description}"
