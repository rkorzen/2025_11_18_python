import asyncio

async def f():
    await asyncio.sleep(0)
    return 1

async def g():
    task = asyncio.create_task(f())
    await asyncio.sleep(0)
    return task.result()

print(asyncio.run(g()))
