# HAR 模块不引用宿主 BuildProfile：构建模式由壳层入口注入，跨模块只从包名入口导入

## 何时使用

多模块拆分、插桩或结构修复阶段，把代码迁入或写入 HAR 模块、需要 DEBUG 等构建模式常量，或调整跨模块导入时

## 适用情境

工程拆为 products 壳 HAP 与 features/components 等 HAR 模块；迁移或新增的 HAR 代码需要构建模式常量（裸模块名 'BuildProfile' 只在宿主 HAP 可解析，每个 HAR 另有自己生成的 BuildProfile），或宿主页要使用其他模块的类；整包 assembleHap 能通过，IDE 按模块做 ArkTS 检查。

## 例外与边界

- 把跨模块相对路径改回包名入口导入时，被引用的类须已在对方模块的入口声明文件（oh-package.json5 的 main 指定，默认 Index.ets）导出，且引用方模块已配置对该 HAR 的依赖；缺哪一项就补哪一项，不退回相对路径。

## 原因

HAR 里写 import { DEBUG } from 'BuildProfile' 时整包构建能由宿主解析，按模块检查却报 Cannot find module；跨模块相对路径导入则报 Cannot import files outside of the current module。来源有三条分支：模块化下沉日志服务时原样带走宿主 BuildProfile 导入，也没有让宿主入口传入开关；UI 测试修复把壳层的 DEBUG && testMode 门控照抄进 HAR 页面，编译报错后又补宿主导入；结构检测因不解析模块名把合法的包名导入报为未使用，处理者改成跨模块相对路径让检测收敛。

## 做法

1. 把代码迁入 HAR 或在 HAR 新增代码时，逐文件检查只在宿主可解析的依赖（如 'BuildProfile'）；需要构建模式就改为初始化参数由壳层入口或组合层注入，测试门控读取共享测试态，不在 HAR 里 import 宿主 BuildProfile。
2. 开关改成初始化参数后，同步修改所有宿主入口的调用（主 Ability、卡片扩展、后台任务、备份扩展等）传入宿主 DEBUG。
3. 跨模块使用类只从模块包名入口（Index.ets 导出）导入；静态检测因不解析模块名而误报时，记录误报或修检测配置，不改成跨模块相对路径。

## 可选检查

- 模块化或插桩批次除 assembleHap 外，确认 features/components 中没有 from 'BuildProfile'、没有指向其他模块目录的相对路径导入，并按模块跑 ArkTS 检查。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 3 步〕HAR 对外提供的接口统一在入口声明文件（默认是 Index.ets）中导出，入口文件由该模块 oh-package.json5 的 main 字段指定
- 〔做法第 1 步〕AppStorage 是 UI 框架在应用启动时创建、与应用进程绑定的单例，存放的状态在应用级别可访问，不按模块分份
- 〔适用情境 / 原因〕每个 HAR 有自己生成的 BuildProfile.ets，裸模块名 'BuildProfile' 只在宿主 HAP 中可解析；HAR 里写这类导入时，hvigor 按 HAP 整体 assembleHap 能通过，IDE 的 ArkTS 检查按模块校验时才报错
