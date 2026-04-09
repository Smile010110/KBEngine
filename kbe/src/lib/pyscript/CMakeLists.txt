# ---------------- 源文件 ----------------
set(SRCS
	copy.cpp
	map.cpp
	math.cpp
	pickler.cpp
	py_compression.cpp
	py_gc.cpp
	pyurl.cpp
	py_platform.cpp
	pystruct.cpp
	pyprofile.cpp
	pyprofile_handler.cpp
	py_memorystream.cpp
	pywatcher.cpp
	script.cpp
	scriptobject.cpp
	scriptstdout.cpp
	scriptstderr.cpp
	scriptstdouterr.cpp
	scriptstdouterrhook.cpp
	sequence.cpp
	vector2.cpp
	vector3.cpp
	vector4.cpp
)
# ---------------- 创建静态库 ----------------
add_library(pyscript STATIC ${SRCS})

target_link_libraries(pyscript PRIVATE 
	fmt::fmt
	python_interface
)


