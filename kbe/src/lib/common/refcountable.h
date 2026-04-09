// Copyright 2008-2018 Yolo Technologies, Inc. All Rights Reserved. https://www.comblockengine.com


/*
	引用计数实现类

	使用方法:
		class AA:public RefCountable
		{
		public:
			AA(){}
			~AA(){ printf("析构"); }
		};
		
		--------------------------------------------
		AA* a = new AA();
		RefCountedPtr<AA>* s = new RefCountedPtr<AA>(a);
		RefCountedPtr<AA>* s1 = new RefCountedPtr<AA>(a);
		
		int i = (*s)->getRefCount();
		
		delete s;
		delete s1;
		
		执行结果:
			析构
*/
#ifndef KBE_REFCOUNTABLE_H
#define KBE_REFCOUNTABLE_H
	
#include "common.h"
	
namespace KBEngine{

class RefCountable 
{
public:
	inline void incRef(void) const
	{
		++refCount_;
	}

	inline void decRef(void) const
	{
		
		int currRef = --refCount_;
		assert(currRef >= 0 && "RefCountable:currRef maybe a error!");
		if (0 >= currRef)
			onRefOver();											// 引用结束了
	}

	virtual void onRefOver(void) const
	{
		delete const_cast<RefCountable*>(this);
	}

	void setRefCount(int n)
	{
		refCount_ = n;
	}

	int getRefCount(void) const 
	{ 
		return refCount_; 
	}

protected:
	RefCountable(void) : refCount_(0) 
	{
	}

	virtual ~RefCountable(void) 
	{ 
		assert(0 == refCount_ && "RefCountable:currRef maybe a error!"); 
	}

protected:
	volatile mutable long refCount_;
};

#if KBE_PLATFORM == PLATFORM_WIN32
class SafeRefCountable 
{
public:
	inline void incRef(void) const
	{
		::InterlockedIncrement(&refCount_);
	}

	inline void decRef(void) const
	{
		
		long currRef =::InterlockedDecrement(&refCount_);
		assert(currRef >= 0 && "RefCountable:currRef maybe a error!");
		if (0 >= currRef)
			onRefOver();											// 引用结束了
	}

	virtual void onRefOver(void) const
	{
		delete const_cast<SafeRefCountable*>(this);
	}

	void setRefCount(long n)
	{
		InterlockedExchange((long *)&refCount_, n);
	}

	int getRefCount(void) const 
	{ 
		return InterlockedExchange((long *)&refCount_, refCount_);
	}

protected:
	SafeRefCountable(void) : refCount_(0) 
	{
	}

	virtual ~SafeRefCountable(void) 
	{ 
		assert(0 == refCount_ && "SafeRefCountable:currRef maybe a error!"); 
	}

protected:
	volatile mutable long refCount_;
};
#else
class SafeRefCountable 
{
public:
	inline void incRef(void) const
	{
	#if defined(__x86_64__) || defined(__i386__)
		__asm__ volatile (
			"lock addl $1, %0"
			:
			: "m"(this->refCount_)
			: "memory"
		);
	#elif defined(__aarch64__)
		uint32_t tmp;
		uint32_t status;
		asm volatile(
			"1: ldaxr %w0, [%2]\n"   // 从内存加载到 tmp
			"   add %w0, %w0, #1\n"   // tmp = tmp + 1
			"   stlxr %w1, %w0, [%2]\n" // 尝试存储，status 表示成功与否
			"   cbnz %w1, 1b\n"        // 如果失败，重试
			: "=&r"(tmp), "=&r"(status)
			: "r"(&this->refCount_)
			: "memory"
		);
	#else
		refCount_++;  // fallback, 非线程安全
	#endif
	}

	inline void decRef(void) const
	{
		
		long currRef = intDecRef();
		assert(currRef >= 0 && "RefCountable:currRef maybe a error!");
		if (0 >= currRef)
			onRefOver();											// 引用结束了
	}

	virtual void onRefOver(void) const
	{
		delete const_cast<SafeRefCountable*>(this);
	}

	void setRefCount(long n)
	{
		//InterlockedExchange((long *)&refCount_, n);
	}

	int getRefCount(void) const 
	{ 
		//return InterlockedExchange((long *)&refCount_, refCount_);
		return refCount_;
	}

protected:
	SafeRefCountable(void) : refCount_(0) 
	{
	}

	virtual ~SafeRefCountable(void) 
	{ 
		assert(0 == refCount_ && "SafeRefCountable:currRef maybe a error!"); 
	}

protected:
	volatile mutable long refCount_;
private:
	/**
	 *	This private method decreases the reference count by 1.
	 */
	inline int intDecRef() const
	{
	#if defined(__x86_64__) || defined(__i386__)
		int ret;
		__asm__ volatile (
			"mov $-1, %0      \n\t"
			"lock xadd %0, %1"
			: "=&a"(ret)                  // output only and early clobber
			: "m"(this->refCount_)        // input (memory)
			: "memory"
		);
		return ret;

	#elif defined(__aarch64__)
		int old, tmp, res;
		asm volatile(
			"1: ldaxr %w0, [%3]\n"   // old = *refCount_
			"   sub %w1, %w0, #1\n"  // tmp = old - 1
			"   stlxr %w2, %w1, [%3]\n" // res = store success?
			"   cbnz %w2, 1b\n"      // retry if failed
			: "=&r"(old), "=&r"(tmp), "=&r"(res)
			: "r"(&this->refCount_)
			: "memory"
		);
		return old;

	#else
		// fallback，非线程安全
		int old = this->refCount_;
		this->refCount_--;
		return old;
	#endif
	}
};
#endif

template<class T>
class RefCountedPtr 
{
public:
	RefCountedPtr(T* ptr):ptr_(ptr) 
	{
		if (ptr_)
			ptr_->addRef();
	}

	RefCountedPtr(RefCountedPtr<T>* refptr):ptr_(refptr->getObject()) 
	{
		if (ptr_)
			ptr_->addRef();
	}
	
	~RefCountedPtr(void) 
	{
		if (0 != ptr_)
			ptr_->decRef();
	}

	T& operator*() const 
	{ 
		return *ptr_; 
	}

	T* operator->() const 
	{ 
		return (&**this); 
	}

	T* getObject(void) const 
	{ 
		return ptr_; 
	}

private:
	T* ptr_;
};

}
#endif // KBE_REFCOUNTABLE_H
