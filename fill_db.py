from rich import print
import asyncio
import time
from config import *
from db import *
from api import *

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

