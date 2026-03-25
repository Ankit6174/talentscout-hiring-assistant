import os
from langchain.tools import tool
from pydantic import BaseModel, Field, ValidationError
from typing import List
from config.connect_db import get_collection

from langsmith import traceable

# Validation schema for every candidate.
class Valid_candidate(BaseModel):
    name: str = Field(description="Candidate's full name.")
    email: str = Field(description="Candidate's email address.")
    phone: int | str = Field(description="Candidate's phone number.")
    years_of_experience: int = Field(description="Years of experience.")
    desired_position: str = Field(description="Desired job role.")
    location: str = Field(description="Current location.")
    tech_stack: List[str] = Field(description="Technical skills list.")

# A tools to insert candidate data in mongoDB.
@tool(args_schema=Valid_candidate)
@traceable(name="insert_candidate_info_tool")
def insert_condidate_info(
    name: str,
    email: str,
    phone: int | str,
    years_of_experience: int | str,
    desired_position: str,
    location: str,
    tech_stack = List[str]
) -> str:
    """Tool used to store the information of candidate."""

    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "years_of_experience": years_of_experience,
        "desired_position": desired_position,
        "location": location,
        "tech_stack": tech_stack
    }

    collection = get_collection(
        database_name=os.environ["MONGO_DB_NAME"], 
        collection_name=os.environ["MONGO_COLLECTION_NAME"]
    )

    try:
        valid_candidate_data = Valid_candidate(**data)
        collection.insert_one(valid_candidate_data.model_dump())
        return "Cadidate's data inserted successfully!"
    except ValidationError as e:
        print(e.errors())
        return ("Validation failed!")
