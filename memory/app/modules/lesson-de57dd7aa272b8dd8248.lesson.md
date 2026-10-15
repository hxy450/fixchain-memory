# 多模块工程跨模块使用类只从模块包名入口导入：静态检测误报时不改成跨模块相对路径

ID：`lesson-de57dd7aa272b8dd8248` · 版本：2

[本主题](index.md)

## 何时使用

多模块工程的实现、插桩或结构修复阶段，宿主页或其他模块要使用某个 HAR 的类，或为通过静态检测调整导入路径时

## 适用情境

工程拆为壳 HAP 与多个 HAR，HAR 在 Index.ets 导出对外的类，并在使用方的 oh-package.json5 中声明依赖；结构检测或孤儿文件扫描不解析模块名，把合法的包名导入报为未使用或孤儿。

## 原因

跨模块相对路径导入越过模块边界：hvigor 的导入检查对它报“Cannot import files outside of the current module using relative paths”（build-profile 的 strictMode.noExternalImportByPath 为 true 时是错误，否则为警告；hvigor-ohos-plugin 6.23.6）；静态检测不解析模块名时会把包名导入误报为未使用，按检测结果改成相对路径能让检测收敛，却破坏了模块边界。

## 做法

1. 跨模块使用类只从模块包名入口导入（目标模块 Index.ets 导出、使用方 oh-package.json5 声明依赖）；要用的类还没导出时，在该模块 Index.ets 补导出。
2. 静态检测因不解析模块名而误报时，记录误报或修检测配置，不改成跨模块相对路径。

## 可选检查

- 结构修复后检索指向其他模块目录的相对路径导入（如 from '../../features/...'），结果应为空，并按模块跑 ArkTS 检查。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-282d676ed02777809cac](../../../store/cases/case-282d676ed02777809cac/eab8108abf2710c6c0db3d794e2a5f56cc8185903938c300442069d2d2fc6ccc.json) · 结论：diagnosis, recommendation:4, recommendation:5
  卡片版本：`eab8108abf2710c6c0db3d794e2a5f56cc8185903938c300442069d2d2fc6ccc`
