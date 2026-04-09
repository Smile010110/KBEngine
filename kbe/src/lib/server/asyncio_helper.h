// Copyright 2008-2018 Yolo Technologies, Inc. All Rights Reserved. https://www.comblockengine.com

#ifndef KBE_ASYNCIO_HELPER_HANDLER_H
#define KBE_ASYNCIO_HELPER_HANDLER_H

#include "common/common.h"
#include "Python.h"

namespace KBEngine {

	class AsyncioHelper
	{
	public:

		/**
		 * 提交一个协程到async_dispatcher模块中执行。
		 * 这个函数会检查传入的pyObject是否是一个可等待的对象（即实现了__await__方法），
		 * 如果是，则调用async_dispatcher模块中的submit_coroutine函数提交该协程。
		 *
		 * @param pyObject: 要提交的Python对象，必须是一个可等待的协程。
		 * @return 返回NULL，因为submitCoroutine函数是异步的，暂时不处理返回结果。
		 */
		static PyObject* submitCoroutine(PyObject* pyObject);
	};

}

#endif
