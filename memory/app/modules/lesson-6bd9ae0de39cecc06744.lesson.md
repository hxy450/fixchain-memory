# HAR 里需要构建模式时不引用宿主的 BuildProfile：用本模块生成的 BuildProfile，须与宿主构建模式一致时由壳层入口注入

ID：`lesson-6bd9ae0de39cecc06744` · 版本：3

[本主题](index.md)

## 何时使用

多模块拆分、插桩或结构修复阶段，把含 DEBUG 等构建模式判断的代码迁入或写入 HAR 模块时

## 适用情境

工程拆为 products 壳 HAP 与 features/components 等 HAR 模块；迁移或新增的 HAR 代码需要构建模式常量，源端或壳层写法是 import { DEBUG } from 'BuildProfile'（裸模块名只在宿主 HAP 可解析）；每个 HAR 在模块根另有自己生成的 BuildProfile.ets；整包 assembleHap 能通过，IDE 按模块做 ArkTS 检查。

## 例外与边界

- 代码位于 HAP 模块时，直接从宿主的 'BuildProfile' 读 DEBUG（生成文件同时导出 DEBUG 常量和兼容用的默认类 BuildProfile，hvigor-ohos-plugin 6.23.6），见 BuildConfig.DEBUG 映射一条

## 原因

HAR 里写裸模块名 'BuildProfile' 时整包构建能由宿主解析，按模块做 ArkTS 检查时解析不到。HAR 自己生成的 BuildProfile.ets 中 DEBUG 取该 HAR 当前 target 的 buildOption.debuggable（未配置时为 true），与宿主 HAP 的构建模式不一定一致（DevEco 自带 hvigor-ohos-plugin 6.23.6 的 HAR BuildProfile 生成任务）。

## 做法

1. 把代码迁入 HAR 或在 HAR 新增代码时，逐文件检查只在宿主可解析的依赖（如裸模块名 'BuildProfile'），不在 HAR 里 import 宿主的 BuildProfile。
2. 只需该 HAR 自身的构建模式时，按相对路径导入本模块根目录生成的 BuildProfile.ets 并读 DEBUG；要求与宿主 HAP 构建模式严格一致时（如日志开关、测试门控），改为初始化参数由壳层入口或组合层注入，测试门控读取共享测试态。
3. 开关改成初始化参数后，同步修改所有宿主入口的调用（主 Ability、卡片扩展、后台任务、备份扩展等）传入宿主 DEBUG。

## 可选检查

- 模块化或插桩批次除 assembleHap 外，确认 HAR 目录中没有 from 'BuildProfile' 的裸模块名导入，并按模块跑 ArkTS 检查。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-282d676ed02777809cac](../../../store/cases/case-282d676ed02777809cac/eab8108abf2710c6c0db3d794e2a5f56cc8185903938c300442069d2d2fc6ccc.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`eab8108abf2710c6c0db3d794e2a5f56cc8185903938c300442069d2d2fc6ccc`
