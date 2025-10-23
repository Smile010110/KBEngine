// Copyright 2008-2018 Yolo Technologies, Inc. All Rights Reserved. https://www.comblockengine.com

#include "db_exception.h"
#include "db_interface_redis.h"
#include "db_interface/db_interface.h"

namespace KBEngine { 
	namespace redis {

		//-------------------------------------------------------------------------------------
		DBException::DBException(DBInterface* pdbi) :
			errStr_(static_cast<DBInterfaceRedis*>(pdbi)->getstrerror()),
			errNum_(static_cast<DBInterfaceRedis*>(pdbi)->getlasterror())
		{
		}

		//-------------------------------------------------------------------------------------
		DBException::~DBException() throw()
		{
		}

		//-------------------------------------------------------------------------------------
		bool DBException::shouldRetry() const
		{
			ERROR_MSG(fmt::format("Redis DBException::shouldRetry() errNum_={} errStr_={} \n", errNum_, errStr_));

			// 使用正确的错误码值
			return (errNum_ == REDIS_ERR_OOM) ||        // 5
				(errNum_ == REDIS_ERR_OTHER) ||      // 2  
				(errNum_ == REDIS_ERR_TIMEOUT);      // 6
		}

		//-------------------------------------------------------------------------------------
		bool DBException::isLostConnection() const
		{
			ERROR_MSG(fmt::format("Redis DBException::isLostConnection() errNum_={} errStr_={} \n", errNum_, errStr_));

			// 使用正确的错误码值
			return (errNum_ == REDIS_ERR_IO) ||         // 1
				(errNum_ == REDIS_ERR_EOF) ||        // 3
				(errNum_ == REDIS_ERR_TIMEOUT);      // 6
		}

		//-------------------------------------------------------------------------------------
	}
}

// db_exception.cpp
