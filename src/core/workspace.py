from src.domain.campaign.models.campaign import Campaign


class Workspace:
    def __init__(self):
        self._current_campaign: Campaign | None = None
        
    @property
    def current_campaign(self) -> Campaign | None:
        return self._current_campaign
    
    def select_campaign(self, campaign: Campaign) -> None:
        self._current_campaign = campaign
        
    def close_campaign(self) -> None:
        self._current_campaign = None
        
