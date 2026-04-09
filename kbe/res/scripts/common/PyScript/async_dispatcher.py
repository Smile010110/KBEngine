# async_dispatcher.py
import asyncio
import threading
from KBEDebug import *


loop = asyncio.new_event_loop()
# pending_tasks = []
loop_started = threading.Event()  # 事件同步器
shutdown_requested = threading.Event()
lock = threading.Lock()


def start_loop():
    asyncio.set_event_loop(loop)
    INFO_MSG("[asyncio] Event loop started")
    loop_started.set()  # 通知已准备好
    try:
        loop.run_forever()
    except Exception as e:
        ERROR_MSG(f"[asyncio] Event loop exception: {e}")
    finally:
        INFO_MSG("[asyncio] Event loop stopping...")
        loop.close()
        INFO_MSG("[asyncio] Event loop stopped")

# 启动线程
threading.Thread(target=start_loop, daemon=True).start()

def submit_coroutine(coro):
    if not loop_started.wait(timeout=2):  # 等待 loop 准备好
        ERROR_MSG("[asyncio] Coroutine submitted too early! Loop not started yet!")
        return

    future = asyncio.run_coroutine_threadsafe(coro, loop)

    # def on_done(fut):
    #     try:
    #         result = fut.result()
    #         ERROR_MSG("[asyncio] Coroutine done:", result)
    #     except Exception as e:
    #         ERROR_MSG("[asyncio] Coroutine error:", e)

    # future.add_done_callback(on_done)
    # pending_tasks.append(future)

def onAsyncTimer(timerID):
    """
    KBEngine method.
    定时器，Python保活
    """
    pass

def shutdown():
    """
    安全关闭 asyncio loop：
    1. 取消所有 coroutine
    2. 停止事件循环
    """
    if shutdown_requested.is_set():
        return  # 避免重复 shutdown

    shutdown_requested.set()
    INFO_MSG("[asyncio] Shutdown initiated...")


    # 停止 loop
    if loop.is_running():
        loop.call_soon_threadsafe(loop.stop)