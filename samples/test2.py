import asyncio

async def slow_operation(future):
    await asyncio.sleep(2)
    future.set_result('result')


def on_complete(future):
    print(future.result())

loop = asyncio.get_event_loop()

future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(on_complete)


future2 = asyncio.Future()
asyncio.ensure_future(slow_operation(future2))
future2.add_done_callback(on_complete)

try:
    loop.run_forever()
finally:
    loop.close()
