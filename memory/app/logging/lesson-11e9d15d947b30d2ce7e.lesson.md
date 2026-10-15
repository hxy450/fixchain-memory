# 新增错误日志沿用工程的 hilog 约定，不写 console.*

ID：`lesson-11e9d15d947b30d2ce7e` · 版本：4

[本主题](index.md)

## 何时使用

功能实现阶段，在服务层或 ViewModel 的 catch 分支里为新增的错误处理选择日志写法时

## 适用情境

源端对失败静默处理或没有日志（如 Kotlin runCatching 吞掉异常），目标 ArkTS 在 catch 中新增错误日志；工程里已有 hilog 写法（TAG、DOMAIN 常量），而生成期规则只约束 build() 内的 console.log 或占位写法。

## 原因

源端没有可映射的日志，生成规则与迁移期静态检查也不要求把 console.* 换成 hilog，新增的 catch 里就会写成 console.error，日志出口与工程已有的 hilog 约定不一致，直到专门检查 console.* 的静态规则才被检出。

## 做法

1. 写日志前 rg 工程现有写法（如 import { hilog } from '@kit.PerformanceAnalysisKit' 与 TAG、DOMAIN 常量），照它写 hilog.error(DOMAIN, TAG, '<说明>: %{public}s', String(error))，TAG 取当前类名。
2. 每个切片写完，rg -n 'console\.' 本次改动的 .ets 文件，已登记占位之外的命中都改成 hilog。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-2b82a569104ca26f84ae](../../../store/cases/case-2b82a569104ca26f84ae/f1850eb1032b509abdc74d54d07eb436c4dd08567fb70c7ba3e9ab984d43cf5d.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`f1850eb1032b509abdc74d54d07eb436c4dd08567fb70c7ba3e9ab984d43cf5d`
- [case-98e7bd27bb334db83f51](../../../store/cases/case-98e7bd27bb334db83f51/2bd8a63105c2a86e012e477614f9ed3d54d26dbfc05250b99a797f194a3e1b79.json) · 结论：diagnosis
  卡片版本：`2bd8a63105c2a86e012e477614f9ed3d54d26dbfc05250b99a797f194a3e1b79`
