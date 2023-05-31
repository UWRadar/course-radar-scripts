import httpx
from rich import print
import uuid
import asyncio
import json
import sqlite3
import time

dawgpath_cookie = '_hp2_id.3001039959={"userId":"4842590607244095","pageviewId":"4336556983834859","sessionId":"2076341506492832","identity":null,"trackerVersion":"4.0"}; _ga_TNNYEHDN9L=GS1.1.1684736916.16.0.1684736919.0.0.0; csrftoken=THhj0ogZQwm9h7PhBa3EYlhImKLcUSlmCy7RLVMIoDIiIa59JzGsY0VqfrXP345E; sessionid=gawnxzr93s6qmlz4f4e857v835hs1whx; _ga_ZC9EHK2ZQY=GS1.1.1684818033.1.1.1684818046.0.0.0; _ga_J814GNXH0D=GS1.1.1684818034.1.1.1684818046.0.0.0; _gid=GA1.2.1093942245.1685317323; _ga=GA1.1.449556412.1683221743; _ga_BFQJ094C4L=GS1.1.1685373739.12.1.1685373750.0.0.0'
myplan_cookie = '_ga_ZC9EHK2ZQY=GS1.1.1684818033.1.1.1684818046.0.0.0; _ga_J814GNXH0D=GS1.1.1684818034.1.1.1684818046.0.0.0; _ga=GA1.1.449556412.1683221743; _ga_BFQJ094C4L=GS1.1.1685373739.12.1.1685375125.0.0.0; _ga_B3VH61T4DT=GS1.1.1685472352.1.0.1685472359.0.0.0; _hp2_id.3001039959={"userId":"4842590607244095","pageviewId":"685340989013846","sessionId":"427915151407462","identity":null,"trackerVersion":"4.0"}; sessionId=ebcc3d0e68fa98b40b5ac20cdb257111a9ce51d2787f87b8852cbd7f91f52cea; _ga_TNNYEHDN9L=GS1.1.1685510324.19.1.1685510324.0.0.0'
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"

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

conn = sqlite3.connect("./db.db")
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS Courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                courseId TEXT UNIQUE,
                code TEXT,
                subject TEXT,
                value TEXT
               )
               ''')

def insert_course(c, campus) -> bool:
    cursor.execute('SELECT courseId FROM Courses WHERE courseId = ?', [c['courseId']])
    existing_course = cursor.fetchone()

    if existing_course:
        # print(f"\nAlready exists: ", {"courseId": c['courseId'], "code": c["code"]})
        return False
    
    try:
        cursor.execute('''
                       INSERT INTO Courses 
                       (courseId, code, subject, campus, value) 
                       VALUES (?, ?, ?, ?, ?)
                       ''', 
                       (c['courseId'], c['code'], c['subject'], campus, json.dumps(c))
                       )
        conn.commit()
        # print("\n[green]Inserted course: ")
        # print({"courseId": c['courseId'], "code": c["code"]})
        return True
    except Exception as e:
        print("\nError occurred while inserting the course:", c['code'])
        print(e)
        return False


def major_exists_in_db(major: str):
    cursor.execute('SELECT id, subject FROM Courses WHERE subject = ?', [major])
    existing_course = cursor.fetchone()
    return True if existing_course else False


async def main() -> None:
    # c_kv_list = get_major_kv_list(cookie)
    m_list = get_subject_areas(myplan_cookie)
    seattle_m_list = filter(lambda r: r['campus'] == 'seattle', m_list)
    # print(m_list[:23])

    for m in m_list:
        success_count = 0
        print("Starting major {}".format(m["code"]))
        if major_exists_in_db(m['code'].upper()):
            print("Major '{}' already scraped".format(m['code']))
            continue
        data = get_major_courses(myplan_cookie, m["code"], m['campus'])
        # print(f"\nStarting major '{m['code']}' - {len(data)} courses")
        for c in data:
            t = insert_course(c, m['campus'])
            if t:
                success_count += 1

        print("Finished major '{}', inserted {} / {} courses".format(
            m['code'], success_count, len(data)))
        time.sleep(0.5)
    conn.close()


if __name__ == "__main__":
    asyncio.run(main())

