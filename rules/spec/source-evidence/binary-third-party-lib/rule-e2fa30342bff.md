# 外观或行为由仓库外三方库决定时，按坐标取库制品写真值，取不到登记缺口

审的是：规格
触发（任一种）：
- 读到：依赖里有三方库坐标（implementation、@aar），源码只 extends 或调用库类、布局里只有库的自定义 View，仓库里没有库源码；写错的样子：规格写「源码不在本仓库」「内部 UI 不可见 → 自研」「默认样式即可对齐」「待核自由度」，或跨栈映射只写「→ Toast / 自研」，没有库里的尺寸、缺省值、行为和出处，也没登记缺库真值
适用范围：规格里写由 AAR / jar 三方库决定的外观和行为时
做法：
- 从构建脚本 dependencies、libs.versions.toml 或 import 包名读出 group:artifact:version，到 Gradle 缓存 modules-2/files-2.1/<group>/<artifact>/<version>/ 下取 aar、jar 或 sources jar；没有就解析依赖或从库的官方仓库取同版本
- 解包读 res/layout*、res/values*、res/drawable，反编译 classes.jar 或用 javap -p -c -constants 读构造缺省和常量，把尺寸、缺省值、行为连同库版本写进规格
- 确实取不到制品时登记缺库真值的阻塞或待核，不写无证据的替代裁定或确定契约
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 只有编译后的 jar、没有 sources jar 也能读：javap -p -c -constants 反汇编出缺省值和常量：「库源不可查」不成立（出处：卡里修好并验证过）
针对本应用要查的：
- 三方库的坐标、版本和制品：源工程 Gradle 构建脚本的 dependencies、版本目录 libs.versions.toml、源文件的 import 包名；Gradle 用户缓存 caches/modules-2/files-2.1/<group>/<artifact>/<version>/ 下的 aar、jar、sources jar，或解包后的 transforms 目录；缓存里有就解包；没有就让 Gradle 解析依赖或按版本从库的官方仓库取，再读 res 和类
未核实：生成环境能否联网或运行 Gradle 解析依赖，卡里没有记录
来源：3 张卡，3 个应用
- case-087050b57a3e1a6ac4ce（jerboa）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-49a2270970314f62c95f（GameOfLife）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 1 ← 诊断
- case-74b07cb94daa311f36b1（omni-notes-hmos）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 1
