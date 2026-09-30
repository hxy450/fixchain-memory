# 新增错误日志沿用工程的 hilog 约定，不写 console.*

ID：`lesson-11e9d15d947b30d2ce7e` · 版本：2

[本主题](index.md)

## 何时使用

功能实现阶段，在服务层、ViewModel 或页面的 catch 分支里为新增的错误处理选择日志写法时

## 适用情境

源端对失败静默处理或没有日志（如 Kotlin runCatching 吞掉异常），目标 ArkTS 在 catch 中新增错误日志；工程里已有 hilog 写法（TAG、DOMAIN 常量），而生成期规则只约束 build() 内的 console.log 或占位写法。

## 原因

源端没有可映射的日志，生成规则与迁移期静态检查也没有 console.* → hilog 的要求，写码者就按通用 TypeScript 习惯写 console.error，直到 ECAT 静态检查才被检出。来源两个应用都如此：一处写码 agent 批量读 skill 时输出被截断，含 hilog 导入映射的 skill 没进上下文；另一处生成期规则只禁止 console.info('TODO') 这类假实现，返修时才统一改成 hilog。

## 做法

1. 写日志前 rg 工程现有写法（如 import { hilog } from '@kit.PerformanceAnalysisKit' 与 TAG、DOMAIN 常量），照它写 hilog.error(DOMAIN, TAG, '<说明>: %{public}s', String(error))，TAG 取当前类名。
2. 每个切片写完，rg -n 'console\.' 本次改动的 .ets 文件，已登记占位之外的命中都改成 hilog。

