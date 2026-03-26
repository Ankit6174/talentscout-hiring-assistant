import os
from langchain.tools import tool
from pydantic import BaseModel, Field, ValidationError
from typing import List
from config.connect_db import get_collection

from langsmith import traceable

# Validation schema for every candidate.
class Valid_candidate(BaseModel):
    """
    Pydantic model to validate candidate information.
    Ensures all required fields are present and correctly typed.
    """
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
    # Note that this docstring is intentionally short. This tool's schema is provided to the LLM, 
    # so a longer description would make token generation slower. 
    # This concise description has been tested and is sufficient to generate the desired output.

    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "years_of_experience": years_of_experience,
        "desired_position": desired_position,
        "location": location,
        "tech_stack": tech_stack
    }

    # Connect to MongoDB Collection
    collection = get_collection(
        database_name=os.environ["MONGO_DB_NAME"], 
        collection_name=os.environ["MONGO_COLLECTION_NAME"]
    )

    try:
         # Validate input using Pydantic
        valid_candidate_data = Valid_candidate(**data)

        # Insert validated data into MongoDB
        collection.insert_one(valid_candidate_data.model_dump())
        return "Cadidate's data inserted successfully!"
    
        # The above data will be securely stored in MongoDB Atlas cloud.
        # We can also extend this to store additional information, 
        # such as the candidate's conversation history or overall performance metrics.
    except ValidationError as e:
        print(e.errors())
        return ("Validation failed!")
