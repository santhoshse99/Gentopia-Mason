import requests
from gentopia.tools.basetool import *
from typing import Optional, Type

class JobOpportunityArgs(BaseModel):
    role: str = Field(..., description="The job role for which to provide current openings")
    location: Optional[str] = Field(None, description="The location for the job role (optional).")

class JobOpportunity(BaseTool):
    """Tool that provides job listings for a specific role using the Adzuna API."""
    
    name = "job_opportunity"
    description = "Provides job openings for a specified role using the Adzuna API."

    args_schema: Optional[Type[BaseModel]] = JobOpportunityArgs

    def _run(self, role: str, location: Optional[str] = None) -> str:
        try:
            application_id = "" #Put your adzuna app_id here. Removed before submission. Sign up on Adzuna api website and get it 
            adzuna_api_key = "" #Put your adzuna api key here. Removed before submission. Sign up on Adzuna api website and get it
            country = "us"

            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            params = {
                'app_id': application_id,
                'app_key': adzuna_api_key,
                'what': role,
                'where': location,
                'results_per_page': 1
            }

            url_response = requests.get(url, params=params)
            returned_data = url_response.json()

            if url_response.status_code != 200 or 'error' in returned_data:
                return "Failed to fetch job openings"

            num_of_job_listings = returned_data.get('count', 0)  

            if num_of_job_listings > 0:
                return (f"There are currently {num_of_job_listings} job openings for {role} "
                        f"in {location if location else 'the US'} according to the latest market trends.")
            else:
                 return f"No job openings found for {role} in {location if location else 'the US'}."


        except Exception as error:
            return " Error fetching job openings"
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
