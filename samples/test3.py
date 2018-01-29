import asyncio

async def sleep_printer(name):
    for x in range(5):
        print(f"{name} iter #{x}")
        await asyncio.sleep(1)


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    sleep_printer("Jan"), 
    sleep_printer("Natasha"), 
    sleep_printer("Kris"), 
))
