# 源端从 assets 播放的音频文件，目标要逐个复制到 resources/rawfile，保持文件名

审的是：资源
触发（任一种）：
- 读到：源工程 src/main/assets（含依赖模块的 assets）下放着按键 mp3，点击处理按文件名播放；写错的样子：目标 resources/rawfile 下没有这些音频，或代码里 getRawFd('…') 的文件名在 rawfile 下找不到
适用范围：迁移按键音、提示音这类由源端 assets 提供的音频时
做法：
- 按源端播放调用里用到的文件名，从源工程各模块的 assets 找到实际音频文件，逐个复制到目标模块的 src/main/resources/rawfile/，文件名不变，代码按同一个文件名 getRawFd
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- rawfile 目录里的文件直接打包进应用，不编译、不分配资源 ID，按文件路径和文件名访问：源端 assets 的对应目录（出处：resource-categories-and-access.md，资源目录）
- getContext().resourceManager.getRawFd('rawfilepath') 取得 {fd, offset, length}：代码访问 rawfile 文件的方式，路径相对 rawfile 目录（出处：resource-categories-and-access.md，访问本模块资源或模块依赖的HAR资源）
针对本应用要查的：
- 要复制哪些音频文件：源工程里播放工具类和点击处理器传入的文件名，以及各模块（含依赖模块）的 src/main/assets 目录；列出处理器各分支用到的文件名，在 assets 里逐个找到同名文件；漏一个就有一个按键无声
来源：1 张卡，1 个应用
- case-a224386ed55020afec18（android-train-ticket-vest7）：做法第 1 步 ← 建议 4、诊断
