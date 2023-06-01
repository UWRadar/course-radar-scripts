import uuid
import httpx
from config import user_agent

def get_course_kv_list(cookie, campus: str = "seattle"):
    url = "https://dawgpath.uw.edu/api/v1/courses/" + campus
    headers = {
        "cookie": cookie,
        "user-agent": user_agent
    }
    res = httpx.get(url, headers=headers)
    data = res.json()
    return data

def get_major_kv_list(cookie, campus: str = "seattle"):
    url = "https://dawgpath.uw.edu/api/v1/majors/" + campus
    headers = {
        "cookie": cookie,
        "user-agent": user_agent
    }
    res = httpx.get(url, headers=headers)
    data = res.json()
    return data

def get_subject_areas(cookie: str):
    url = "https://course-app-api.planning.sis.uw.edu/api/subjectAreas"
    res = httpx.get(url, headers={ "cookie": cookie, "user-agent": user_agent })
    return res.json()

def get_major_courses(cookie: str, major: str, campus: str):
    url = "https://course-app-api.planning.sis.uw.edu/api/courses"
    res = httpx.post(
        url,
        headers={ "cookie": cookie, "user-agent": user_agent },
        json={
            "campus": campus,
            "consumerLevel": "UNDERGRADUATE",
            "days": [],
            "endTime": "2230",
            "instructorSearch": False,
            "queryString": major,
            "requestId": str(uuid.uuid4()),
            "sectionSearch": True,
            "startTime": "0630",
            "username": "blan2",
        }
    )
    return res.json()

