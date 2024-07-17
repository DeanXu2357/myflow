from pydantic import BaseModel


class ExplainChanges(BaseModel):
    def kickoff(self, state):
        # Explain the changes
        return state
