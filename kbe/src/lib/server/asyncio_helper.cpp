#include "asyncio_helper.h"

namespace KBEngine {

	
	PyObject* AsyncioHelper::submitCoroutine(PyObject* pyObject)
	{
		if (pyObject) {
			int isAwaitable = PyObject_HasAttrString(pyObject, "__await__");
			if (isAwaitable > 0) {
				PyObject* dispatcherMod = PyImport_ImportModule("async_dispatcher");
				PyObject* submitFunc = PyObject_GetAttrString(dispatcherMod, "submit_coroutine");
				PyObject* fut = PyObject_CallFunctionObjArgs(submitFunc, pyObject, NULL);
				if (!fut) {
					PyErr_PrintEx(0);
				}
				Py_XDECREF(fut);
				Py_XDECREF(dispatcherMod);
				Py_XDECREF(submitFunc);

			}
		}

		// 暂时返回NULL， 因为submitCoroutine函数是异步的，
		// 需要等待异步执行完成后才能返回结果。
		// 未来可能会处理返回结果，让app间可以通过协程方式进行通信。
		return NULL;
	}
}
