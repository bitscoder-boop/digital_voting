from fastapi import FastAPI
from voter import voter_route
from candidate import candidate_route

app = FastAPI()

app.include_router(voter_route.router)
app.include_router(candidate_route.router)
