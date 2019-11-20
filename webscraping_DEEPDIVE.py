import asyncio, requests

urls = [
    'https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/data-static/documents/breakfast.jpg',
    'https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/data-static/documents/forbidden',
    'https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/data-static/documents/the-html5-breakfast-site.html'
]

async def main():
    loop = asyncio.get_event_loop()
    futures = [loop.run_in_executor(None, requests.get, url) for url in urls]
    for response in await asyncio.gather(*futures):
        print(response.status_code)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())