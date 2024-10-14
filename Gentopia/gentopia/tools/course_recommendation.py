import requests
from gentopia.tools.basetool import *
from typing import Optional, Type


class CourseRecommendationArgs(BaseModel):
    skill: str = Field(..., description="The skill for which to recommend courses.")

class CourseRecommendation(BaseTool):
    """Tool that recommends online courses for a specified skill using the Coursera API."""
    
    name = "course_recommendation"
    description = "Recommends online courses for a specified skill using the Coursera API."
    
    args_schema: Optional[Type[BaseModel]] = CourseRecommendationArgs

    def _run(self, skill: str) -> str:
        try:
            url = "https://api.coursera.org/api/courses.v1"
            params = {
                'q': 'search',
                'query': f"learn {skill}",
                'limit': 5
            }

            url_response = requests.get(url, params=params)
            returned_data = url_response.json()

            if url_response.status_code != 200 or 'error' in returned_data:
                return "Failed to fetch course details"

            returned_courses = returned_data.get('elements', [])
            if not returned_courses:
                return "No courses found for specified skill"

            course_list = [f"{course['name']} - https://www.coursera.org/learn/{course['slug']}" for course in returned_courses]
            return f"Here are some recommended courses for {skill}:\n" + "\n".join(course_list)

        except Exception as error:
            return "Error fetching courses"
    
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
