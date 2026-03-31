<div align="center">
<img alt="KBEngineNex" src="https://github.com/KBEngineLab/KBEngineNexMaterials/blob/main/images/logo_200.png?raw=true" width="120"  style="margin-top:20px;">


<h1>KBEngine Nex</h1>

一款开源的游戏服务端引擎，客户端通过简单的约定协议就能与服务端通讯

使用KBEngine插件能够快速与(Unity3D, UE, Cocos等等)技术结合形成一个完整的客户端

<a href="https://www.kbelab.com/">🎨 官网</a> · <a href="https://api.kbelab.com/">🍀
文档</a> · <a href="https://github.com/KBEngineLab/KBEngine-Nex/issues">
报告问题</a> · <a href="https://github.com/KBEngineLab/KBEngine-Nex/discussions/categories/ideas">
建议反馈</a> · <a href="UPDATE.md">更新日志</a> · <a href="https://github.com/kbengine/kbengine">KBEngine</a>

[![][qq1-shield]][qq1-link]

[![][build-status-shield]][build-status-link] [![][release-shield]][release-link] [![][dockerhub-shield]][dockerhub-link] [![][last-commit-shield]][last-commit-shield-link] [![][github-issues-shield]][github-issues-shield-link] [![][github-stars-shield]][github-stars-link] [![JetBrains Plugins](https://img.shields.io/jetbrains/plugin/v/27963-kbenginex.svg)](https://plugins.jetbrains.com/plugin/27963-kbenginex)

</div>

## Pycharm 插件

**Pycharm插件已发布，支持 2024.2 - 2025.\***

[![JetBrains Plugins](https://img.shields.io/jetbrains/plugin/v/27963-kbenginex.svg)](https://plugins.jetbrains.com/plugin/27963-kbenginex)

[点击查看插件使用文档](https://www.kbelab.com/kbex/)

- [x] [**新建项目**](https://www.kbelab.com/kbex/create_project.html) 通过 Pycharm IDE 新建项目

- [x] [**插件设置**](https://www.kbelab.com/kbex/settings.html) 配置项目相关信息

- [x] [**服务端管理**](https://www.kbelab.com/kbex/server.html) 在Pycharm中启动、停止、调试服务端

- [x] [**SDK生成**](https://www.kbelab.com/kbex/gensdk.html) 一键生成SDK

- [x] [**远程服务**](https://www.kbelab.com/kbex/settings.html#二、ssh-配置功能) 支持远程服务端，自动上传项目

- [x] [**项目支持**](https://www.kbelab.com/kbex/create_project.html#_3-创建成功后-插件会创建venv虚拟环境-并设置隔离app工作区) 支持KBE项目结构，隔离BASE/CELL/BOTS 工作区

- [x] [**内置 KBEngine 模块**](https://www.kbelab.com/kbex/builtin_modules.html) 插件内置 KBEngine
  模块，支持tips自动区分BASE、CELL等模块，自动提示、补全

- [x] [**内置 Math 模块**](https://www.kbelab.com/kbex/builtin_modules.html) 件内置 Math 模块，支持内置方法自动提示、补全

- [x] [**自动补全**](https://www.kbelab.com/kbex/completion_contributor.html) 支持base/cell class 映射、代码自动补全
  ，支持client方法自动补全，支持def文件自动补全及代码生成

- [x] [**代码跳转**](https://www.kbelab.com/kbex/completion_contributor.html#符号跳转) 支持base/cell/client 跳转符号定义处

- [x] [**文件映射**](https://www.kbelab.com/kbex/completion_contributor.html#文件映射) 支持PY文件与DEF文件间的项目跳转

- [x] [**类型映射**](https://www.kbelab.com/kbex/completion_contributor.html#类型映射) 为KBE基础类型提供类型映射

---

## 什么是 KBEngine

https://github.com/kbengine/kbengine

一款开源的游戏服务端引擎，客户端通过简单的约定协议就能与服务端通讯， 使用KBEngine插件能够快速与(Unity3D, UE, Cocos等等)
技术结合形成一个完整的客户端。

服务端底层框架使用C++编写，游戏逻辑层使用Python(支持热更新)，开发者无需重复的实现一些游戏服务端通用的底层技术，
将精力真正集中到游戏开发层面上来，快速的打造各种网络游戏。

## 什么是 KBEngine Nex

KBEngine Nex 是在KBEngine 2.5.12 的基础上社区继续维护的版本

| 区别                  | KBEngine | KBEngine Nex    |
|---------------------|----------|-----------------| 
| Pycharm IDE 插件支持    | 不支持      | 支持              |
| UE5 SDK             | 不支持      | 支持              |
| TS SDK（Cocos、Laya）  | 不支持      | 支持              |
| C# SDK（godot、unity） | 不支持      | 支持              |
| Unity WebSocket     | 不支持      | 支持              |
| WebConsole          | 旧版本      | 已重构             |
| Python版本            | 3.7      | 3.13.3          |
| Python VENV         | 复杂配置     | 支持              |
| MySQL               | 5.x      | 5.x - 9.x       |
| ARM架构               | 不支持      | 支持              |
| 第三方依赖               | 过时       | 全面升级            |
| 一键安装                | 不支持      | 提供脚本            |
| Linux编译工具           | makefile | cmake           |
| Docker基础镜像          | 无        | 有，并提供dockerfile |
| 平台覆盖测试              | 无        | 每个版本都会做全平台编译测试  |

--- 

## 特性

- **多人同时在线**：支持持大量的玩家同时在线实时游戏的交互。 具体承载量需要根据游戏的类型和复杂度以及硬件的性能来决定。
- **自动备份**：支持定时自动备份数据到数据库，同时也提供了API让用户主动调用一次写库功能。
- **跨平台**：Linux支持(x86/x64): Ubuntu, Debain, Centos, Redhat。 支持所有版本的Windows系统，但目前仅用于调试和游戏开发环境。
- **完善的客户端SDK**：客户端开发者所要做的就是接收事件数据，然后渲染。 SDK支持UE、Unity、Cocos等等。
- **配置简单**：只需要修改kbengine.xml 与 kbengine_defaults.xml 配置文件。
- **动态负载平衡**：为了更有效地利用有限的硬件，动态负载均衡技术在高负载时引擎仍然能够很好的工作。
- **强大的配套工具**：在线调试、查看服务端状态、启动与关闭。 在线升级、策划数据导出、等等。
- **快速开发游戏**：只需要使用Python就可以快速的进行设计游戏。 底层安全可靠，保证效率。

---

## 测试平台

| 平台      | 系统版本                        | 环境                            | 引擎版本      |
|---------|-----------------------------|-------------------------------|-----------|
| Ubuntu  | 24.04.3 AMD64               | g++ 13 <br> openssl3.x        | Nex 2.6.3 |
| Ubuntu  | 24.04.4 LTS ARM64           | g++ 13 <br> openssl3.x        | Nex 2.6.3 |
| Ubuntu  | 22.04.5 AMD64               | g++ 9 <br> openssl1.1.x       | Nex 2.6.3 |
| Deepin  | 25.0.1 AMD64                | g++ 12.3.0 <br> OpenSSL 3.2.4 | Nex 2.6.3 |
| CentOS  | Stream-10-20250908.0-x86_64 | g++ 14.3.1 <br> OpenSSL 3.5.2 | Nex 2.6.3 |
| CentOS  | 8.5.2111-x86_64             | g++ 8.5.0 <br> OpenSSL 1.1.1k | Nex 2.6.3 |
| Debian  | 13.1.0-amd64                | g++ 14.2.0 <br> OpenSSL 3.5.1 | Nex 2.6.3 |
| Windows | 专业版 22621.4317              | msbuild <br> openssl1.0.x     | Nex 2.6.3 |

---

## 安装

**注意：VCPKG强依赖于Github，需要网络支持，请自行解决网络问题！**

**Gitee目录提供了国内镜像安装脚本**

### 执行编译脚本 `install_*.bat/sh`

**作用**：自动编译 KBEngine-Nex 服务端和工具。

**使用方法**：

``` CMD
install_windows.bat [CONFIG] [VCPKGPATH]
```

``` sh
install_linux.sh [CONFIG]
```

**参数说明**：

| 参数         | 说明                         | 默认值   |
|------------|----------------------------|-------|
| CONFIG     | 指定编译配置，`Debug` 或 `Release` | Debug |
| VCPKGPATH  | 指定 vcpkg 安装路径              | 可选    |
| GUICONSOLE | 安装 GUI 控制台工具               | 可选    |

**示例**：

##### Windows：

```CMD
# 使用默认 Debug 配置
install_windows.bat

# 指定 Release 配置并指定 vcpkg 路径
install_windows.bat Release D:\Tools\vcpkg

# 编译并安装 GUICONSOLE
install_windows.bat Debug D:\Tools\vcpkg GUICONSOLE

# 所有示例
install_windows.bat Debug
install_windows.bat Debug "VCPKGPATH"
install_windows.bat Debug "" GUICONSOLE
install_windows.bat Release
install_windows.bat Release "VCPKGPATH"
install_windows.bat Release  "" GUICONSOLE
```

##### Linux：

```sh
# 使用默认 Release 配置
install_linux.sh

# 指定Debug
# Linux下支持 Release、Debug、Hybrid、Evaluation
install_linux.sh Debug


# 所有示例
install_linux.sh Debug
install_linux.sh Release
install_linux.sh Hybrid
install_linux.sh Evaluation
```



##### Docker：

本镜像用于快速启动 KBEngine-Nex

###### 准备条件

1.	已安装 Docker （在 macOS/Windows/Linux 上均可）。
2.	本地有一个用于映射的目录，例如你提供的：/Users/KBE/worksapce/Kbengine/demo_kbengine_nex_assets，用于映射到容器内的资产路径。
3.	理解你希望使用的容器名、端口范围及卷映射：
•	容器名：kbenginex-nex-server
•	TCP 端口映射：主机 20013-20025 映射到容器 20013-20025（请注意，端口需要和你的服务端配置一致）
•	UDP 端口映射：主机 20005-20009 映射到容器 20005-20009（请注意，端口需要和你的服务端配置一致）
•	卷映射：主机 /Users/KBE/worksapce/Kbengine/demo_kbengine_nex_assets 映射到容器内 /KBE/server_assets

###### 拉取镜像

``` bash
docker pull kbenginelab/kbengine-nex
```

###### 创建容器（Create）

以下命令仅创建容器，不立即运行：

``` bash
docker create   --name kbenginex-nex-server   -p 20013-20025:20013-20025/tcp   -p 20005-20009:20005-20009/udp   -v /Users/KBE/worksapce/Kbengine/demo_kbengine_nex_assets:/KBE/server_assets   kbenginelab/kbengine-nex
```

说明：

-   `--name kbenginex-nex-server`：容器名称\
-   `-p`：开放并映射 TCP/UDP 端口\
-   `-v`：将本地资产目录挂载到容器内部 `/KBE/server_assets`\
-   创建完成后容器处于 *Created* 状态，不会立即运行

###### 启动容器（Start）

``` bash
docker start kbenginex-nex-server
```

查看启动日志：

``` bash
docker logs -f kbenginex-nex-server
```

###### 进入容器（可选）

``` bash
docker exec -it kbenginex-nex-server /bin/bash
```

###### 停止与再次启动

注意：docker stop 命令非安全退出，会导致持久化数据丢失，请在容器中执行safe_kill.sh 脚本

``` bash
docker stop kbenginex-nex-server
docker start kbenginex-nex-server
```

###### 删除容器

``` bash
docker rm kbenginex-nex-server
```

###### 挂载的资产目录说明

本地路径：

    /Users/KBE/worksapce/Kbengine/demo_kbengine_nex_assets

映射到容器内部：

    /KBE/server_assets


---

## 支持的引擎

<span height="20">&nbsp;</span>
<div align="center">
	<a href="https://unity.com/" target="_blank"><img src="https://raw.githubusercontent.com/KBEngineLab/KBEngineNexMaterials/938f6a964c299176995384985cde18fb88accb5c/images/third_party_logo/unity.svg" alt="Unity" height="30"></a>
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	<a href="https://www.unrealengine.com/zh-CN" target="_blank"><img src="https://raw.githubusercontent.com/KBEngineLab/KBEngineNexMaterials/938f6a964c299176995384985cde18fb88accb5c/images/third_party_logo/unreal-engine.svg" alt="UE5" height="30"></a>
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	<a href="https://www.cocos.com/" target="_blank"><img src="https://github.com/KBEngineLab/KBEngineNexMaterials/blob/main/images/third_party_logo/cocos_dark.png?raw=true" alt="Cocos" height="30"></a>
</div>

<span height="20">&nbsp;</span>

<div align="center">
	<a href="https://layaair.com" target="_blank"><img src="https://github.com/KBEngineLab/KBEngineNexMaterials/blob/main/images/third_party_logo/layaair-logo_dark.png?raw=true" alt="LayaAir" height="30"></a>
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
	<a href="https://godotengine.org/" target="_blank"><img src="https://raw.githubusercontent.com/KBEngineLab/KBEngineNexMaterials/938f6a964c299176995384985cde18fb88accb5c/images/third_party_logo/godot-logo.svg" alt="Godot" height="30"></a>
</div>

## Demo

| 平台           | 链接                                                                 |
|--------------|--------------------------------------------------------------------|
| Unity        | https://github.com/KBEngineLab/demo_kbengine_unity3d_default       |
| UE5          | https://github.com/KBEngineLab/demo_kbengine_ue5_default           |
| UE5 C++ SDK  | https://github.com/KBEngineLab/demo_kbengine_ue5_cxx           |
| C++  | https://github.com/KBEngineLab/demo_kbengine_cxx_console           |
| CocosCreator | https://github.com/KBEngineLab/demo_kbengine_cocos_creator_default |
| Godot        | https://github.com/KBEngineLab/demo_kbengine_godot_default         |

<!-- Cocos2d_js	: https://github.com/kbengine/kbengine_cocos2d_js_demo -->
<!-- Godot Engine	: https://github.com/krogank9/kbe_godot_demo -->


[build-status-shield]: https://ci.appveyor.com/api/projects/status/aij7ox4twu53v3v0/branch/master?svg=true

[build-status-link]: https://ci.appveyor.com/project/KBEngineLab/kbengine-nex/branch/master

[release-shield]: https://img.shields.io/github/v/release/KBEngineLab/KBEngine-Nex?color=3eaf7c&labelColor=black&logo=github&style=flat-square

[release-link]: https://github.com/KBEngineLab/KBEngine-Nex/releases


[last-commit-shield]: https://img.shields.io/github/last-commit/KBEngineLab/KBEngine-Nex?color=c4f042&labelColor=black&style=flat-square

[last-commit-shield-link]: https://github.com/KBEngineLab/KBEngine-Nex/commits/master/


[dockerhub-shield]: https://img.shields.io/docker/v/kbenginelab/kbengine-nex?color=369eff&label=docker&labelColor=black&logoColor=white&style=flat-square

[dockerhub-link]: https://hub.docker.com/r/kbenginelab/kbengine-nex/tags


[github-stars-shield]: https://img.shields.io/github/stars/KBEngineLab/KBEngine-Nex?labelColor&style=flat-square&color=ffcb47

[github-stars-link]: https://github.com/KBEngineLab/KBEngine-Nex


[github-issues-shield]: https://img.shields.io/github/issues/KBEngineLab/KBEngine-Nex?labelColor=black&style=flat-square&color=ff80eb

[github-issues-shield-link]: https://github.com/KBEngineLab/KBEngine-Nex/issues


[qq1-shield]: https://img.shields.io/badge/QQ交流①群-150506969-3eaf7c

[qq1-link]: https://qm.qq.com/q/IuzGOBQqK4


