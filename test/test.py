import asyncio

from app.search_engines import SearchEngineManager
from app.search_engines import XSearch

# async def main():
#     engines = [
#         XSearch()
#     ]
#     manager = SearchEngineManager(
#         # headers={
#         #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
#         # },
#         engines=engines
#     )
#     results = manager.search("hello world", limit=10)
#     for result in results:
#         print(result)

# asyncio.run(main())

def main():
    engines = [
        XSearch()
    ]
    manager = SearchEngineManager(
        engines=engines
    )
    results = manager.search("tesla", limit=10,timeout=2)
    for result in results:
        print(result)

main()