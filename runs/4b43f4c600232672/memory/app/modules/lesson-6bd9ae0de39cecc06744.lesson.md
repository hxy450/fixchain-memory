# HAR 模块不引用宿主 BuildProfile：构建模式由壳层入口注入，跨模块只从包名入口导入

ID：`lesson-6bd9ae0de39cecc06744` · 版本：1

[本主题](index.md)

## 何时使用

多模块拆分、插桩或结构修复阶段，把代码迁入或写入 HAR 模块、需要 DEBUG 等构建模式常量，或调整跨模块导入时

## 适用情境

工程拆为 products 壳 HAP 与 features/components 等 HAR 模块；迁移或新增的 HAR 代码需要构建模式常量（裸模块名 'BuildProfile' 只在宿主 HAP 可解析，每个 HAR 另有自己生成的 BuildProfile），或宿主页要使用其他模块的类；整包 assembleHap 能通过，IDE 按模块做 ArkTS 检查。

## 原因

HAR 里写 import { DEBUG } from 'BuildProfile' 时整包构建能由宿主解析，按模块检查却报 Cannot find module；跨模块相对路径导入则报 Cannot import files outside of the current module。来源有三条分支：模块化下沉日志服务时原样带走宿主 BuildProfile 导入，也没有让宿主入口传入开关；UI 测试修复把壳层的 DEBUG && testMode 门控照抄进 HAR 页面，编译报错后又补宿主导入；结构检测因不解析模块名把合法的包名导入报为未使用，处理者改成跨模块相对路径让检测收敛。

## 做法

1. 把代码迁入 HAR 或在 HAR 新增代码时，逐文件检查只在宿主可解析的依赖（如 'BuildProfile'）；需要构建模式就改为初始化参数由壳层入口或组合层注入，测试门控读取共享测试态，不在 HAR 里 import 宿主 BuildProfile。
2. 开关改成初始化参数后，同步修改所有宿主入口的调用（主 Ability、卡片扩展、后台任务、备份扩展等）传入宿主 DEBUG。
3. 跨模块使用类只从模块包名入口（Index.ets 导出）导入；静态检测因不解析模块名而误报时，记录误报或修检测配置，不改成跨模块相对路径。

## 可选检查

- 模块化或插桩批次除 assembleHap 外，确认 features/components 中没有 from 'BuildProfile'、没有指向其他模块目录的相对路径导入，并按模块跑 ArkTS 检查。

## 来源（按需复核）

- case-282d676ed02777809cac · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`3ccee452becb0b8d6692069a021264d71465c9d94d907359d731e30f191bde9b`
