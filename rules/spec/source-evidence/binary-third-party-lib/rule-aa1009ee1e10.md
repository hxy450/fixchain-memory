# 规格把 prettytime 这类第三方格式化库映射成自实现时，写清库的行为契约和移植来源

审的是：规格
触发（任一种）：
- 读到：依赖清单里有 org.ocpsoft.prettytime:prettytime 这类格式化库，源函数体只是调用 PrettyTime(Locale.getDefault()).formatDuration(...)；写错的样子：跨栈映射写成「prettytime | 自实现（已有算法可直译）」，没写 locale 来源、单位与舍入、语言回退、只在 en 生效的缩写分支，也没指明移植来源
适用范围：规格提取阶段给目标平台没有同名库的第三方格式化依赖写映射时
做法：
- 先读调用点的函数体，确认算法在库里还是在应用里
- 映射行写行为契约：locale 来源（Locale.getDefault 或应用内语言）、单位表与舍入、语言回退、只在 en 生效的缩写分支；并写移植来源：依赖坐标和版本对应的库源码或资源包
针对本应用要查的：
- 库的版本和可移植的源码：源工程构建脚本或版本目录里的依赖坐标；本机 Gradle 缓存 modules-2/files-2.1 下该 group/artifact/版本目录里的 sources jar 或 jar；按坐标版本取库源码和各语言资源包，写进映射行作为移植来源
来源：1 张卡，1 个应用
- case-8d1f62d75e39070e7c62（jerboa）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1
