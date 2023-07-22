from pydantic import BaseModel

class PredictIn(BaseModel):
    medinc : float
    houseage : float
    averooms : float
    avebedrms : float
    population : float
    aveoccup : float
    latitude : float
    longitude : float
    
class PredictOut(BaseModel):
    medhouseval: float
    
