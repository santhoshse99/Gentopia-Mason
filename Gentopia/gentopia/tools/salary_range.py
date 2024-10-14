import requests
from gentopia.tools.basetool import *
from typing import Optional, Type


class SalaryRangeArgs(BaseModel):
    role: str = Field(..., description="The job role for which salary range is required.")
    location: Optional[str] = Field(None, description="The job role location which is an optional argument")

class SalaryRange(BaseTool):
    """Tool that provides the expected salary range using Adzuna API for a specified role(location is optional) """
    
    name = "salary_range"
    description = "Provides the salary range for a specified job role using the Adzuna API(location is optional)"
    
    args_schema: Optional[Type[BaseModel]] = SalaryRangeArgs

    def _run(self, role: str, location: Optional[str] = None) -> str:
        
        try:
            application_id = "" #put your adzuna app_id here. Removed as it had to be removed before submission
            adzuna_api_key = "" #put your adzuna api key here. Removed as it had to be removed before submission
            country = "us"  

            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            params = {
                'app_id': application_id,
                'app_key': adzuna_api_key,
                'what': role,
                'where': location,
                'results_per_page': 1  
            }

            if location:
                params['where'] = location

            url_response = requests.get(url, params=params)
            returned_data = url_response.json()

            if url_response.status_code != 200 or 'error' in returned_data:
                return  "Failed to fetch salary data."

            if 'results' in returned_data and returned_data['results']:
                job_listing = returned_data['results'][0]
                minimum_salary = job_listing.get('salary_min', 'Not specified')
                maximum_salary = job_listing.get('salary_max', 'Not specified')
                average_salary = job_listing.get('mean_salary', job_listing.get('average_salary', 'Not specified'))

                return (f"The expected salary range for a {role} in {location if location else 'the US'} "
                        f"is between {minimum_salary} and {maximum_salary}. The average salary is {average_salary}.")
            else:
                return f"No salary data available for {role} in {location if location else 'the US'}."
        
        except Exception as error:
            return "Error fetching salary trends"
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
