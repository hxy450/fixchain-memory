# app/logging

日志 API 选择与工程内的日志约定

[上一级](../index.md)

## 本级经验

- [新增错误日志沿用工程的 hilog 约定，不写 console.*](lesson-11e9d15d947b30d2ce7e.lesson.md)
  - 时机：功能实现阶段，在服务层或 ViewModel 的 catch 分支里为新增的错误处理选择日志写法时
  - 情境：源端对失败静默处理或没有日志（如 Kotlin runCatching 吞掉异常），目标 ArkTS 在 catch 中新增错误日志；工程里已有 hilog 写法（TAG、DOMAIN 常量），而生成期规则只约束 build() 内的 console.log 或占位写法。
