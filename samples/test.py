import asyncio

async def printNTimes(s, limit=10, period=1):
    for x in range(limit):
        print(s)
        await asyncio.sleep(float(period))
        
loop = asyncio.get_event_loop()
loop.run_until_complete(printNTimes("coroutine_1"))
for x in range(10):
    print("hello")
loop.close()
