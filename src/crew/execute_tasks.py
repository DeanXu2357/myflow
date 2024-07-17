from pydantic import BaseModel


class ExecuteTasks(BaseModel):
    def kickoff(self, state):
        # Execute the tasks
        return state
