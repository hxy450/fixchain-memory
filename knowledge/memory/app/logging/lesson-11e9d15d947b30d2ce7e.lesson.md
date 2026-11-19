# 新增错误日志沿用工程的 hilog 约定，不写 console.*

ID：`lesson-11e9d15d947b30d2ce7e` · 版本：2

> 带知识的试验版（未并入 store）：正文按 `knowledge/lessons/lesson-11e9d15d947b30d2ce7e.json` 改了 0 句，后面接了 4 条已核实的平台事实。原文、来源和证据卡见 [memory/app/logging/lesson-11e9d15d947b30d2ce7e.lesson.md](../../../../memory/app/logging/lesson-11e9d15d947b30d2ce7e.lesson.md)。

## 何时使用

功能实现阶段，在服务层、ViewModel 或页面的 catch 分支里为新增的错误处理选择日志写法时

## 适用情境

源端对失败静默处理或没有日志（如 Kotlin runCatching 吞掉异常），目标 ArkTS 在 catch 中新增错误日志；工程里已有 hilog 写法（TAG、DOMAIN 常量），而生成期规则只约束 build() 内的 console.log 或占位写法。

## 原因

源端没有可映射的日志，生成规则与迁移期静态检查也没有 console.* → hilog 的要求，写码者就按通用 TypeScript 习惯写 console.error，直到 ECAT 静态检查才被检出。来源两个应用都如此：一处写码 agent 批量读 skill 时输出被截断，含 hilog 导入映射的 skill 没进上下文；另一处生成期规则只禁止 console.info('TODO') 这类假实现，返修时才统一改成 hilog。

## 做法

1. 写日志前 rg 工程现有写法（如 import { hilog } from '@kit.PerformanceAnalysisKit' 与 TAG、DOMAIN 常量），照它写 hilog.error(DOMAIN, TAG, '<说明>: %{public}s', String(error))，TAG 取当前类名。
2. 每个切片写完，rg -n 'console\.' 本次改动的 .ets 文件，已登记占位之外的命中都改成 hilog。

## 已核实的平台事实

核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看。

- 〔做法第 1 步〕hilog 从 '@kit.PerformanceAnalysisKit' 导入：import { hilog } from '@kit.PerformanceAnalysisKit'（该 kit 再导出 @ohos.hilog）（出处：鸿蒙 SDK 的 ets/kits/@kit.PerformanceAnalysisKit.d.ts）
- 〔做法第 1 步〕hilog.error(domain: number, tag: string, format: string, ...args: any[]): void；debug/info/warn/fatal 参数相同。domain 为 0x0–0xFFFF 的十六进制整数，超出范围不打印；tag 超长截断（d.ts 写不超过 32 字节，开发指南写最多 31 字节）（出处：鸿蒙 SDK 的 ets/api/@ohos.hilog.d.ts，hilog.error；文档 hilog-guidelines-arkts.md，参数解析）
- 〔做法第 1 步〕format 里每个参数写成 %{private flag}specifier：不写标识符默认 private，输出 <private>；%{public}s 才明文显示（出处：文档 hilog-guidelines-arkts.md，参数解析（隐私标识符））
- 〔做法第 1 步〕格式说明符：d/i 打印 number、bigint；s 打印 string、undefined、boolean、null；o/O 打印 object（API 20 起）；Error 对象不在 s 支持的类型里（出处：文档 hilog-guidelines-arkts.md，参数解析（格式说明符））
