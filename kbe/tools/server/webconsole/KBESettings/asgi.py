"""
ASGI config for KBESettings project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from KBESettings.path import initExtraRootPath

initExtraRootPath()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from KBESettings.ws import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KBESettings.settings')

# application = get_asgi_application()



application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 继续支持 HTTP
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns # 👈 引入 websocket 路由
        )
    ),
})

#
# import faulthandler
# import sys
#
# faulthandler.enable(sys.stderr, all_threads=True)
#
#
# import threading
# import traceback
#
# def dump_threads():
#     for t in threading.enumerate():
#         print(f"Thread {t.name} (daemon={t.daemon}):")
#         for filename, lineno, name, line in traceback.extract_stack(sys._current_frames()[t.ident]):
#             print(f'  File "{filename}", line {lineno}, in {name}')
#             if line:
#                 print(f'    {line}')
#
# import signal
#
# signal.signal(signal.SIGINT, lambda sig, frame: dump_threads())




# manage.py 或其他启动脚本中
# import signal
# import sys
#
# from webconsole.machines_mgr import machinesmgr
#
# def handle_exit(sig, frame):
#     print("检测到退出信号，执行清理操作...")
#     # 这里放你想执行的逻辑，比如保存状态、关闭资源等
#     machinesmgr.cleanup()
#     sys.exit(0)
#
# # 捕捉 Ctrl+C (SIGINT)
# signal.signal(signal.SIGINT, handle_exit)
#
# # 捕捉终止信号 (SIGTERM)
# signal.signal(signal.SIGTERM, handle_exit)


