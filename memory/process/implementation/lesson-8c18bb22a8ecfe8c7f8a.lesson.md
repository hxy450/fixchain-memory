# 翻译 == null / != null 前先核声明类型与来源：编译期保证非空时 == null 恒假（从不触发）、!= null 恒真

ID：`lesson-8c18bb22a8ecfe8c7f8a` · 版本：4

[本主题](index.md)

## 何时使用

规格提取阶段把源端显示条件、弹窗或权限请求的触发条件写成页面契约与偏好默认值时；实现阶段按规格新增依赖该条件的弹窗、权限请求或协调服务时

## 适用情境

Compose 页面用 collectAsState(initial = false) 收集 Flow<Boolean>（DataStore getter 映射为 preferences[KEY] == true 或带 ?: 默认值），显示条件里却把该状态与 null 比较；规格可能同时写着“该偏好 Boolean、默认 false”与“== null 表示从未写入/首次进入”。

## 例外与边界

- 值来自 Java 平台类型（未标注可空性的 Java API 返回值，Kotlin 视为 T!）、反射反序列化（Gson 等可绕过 Kotlin 非空检查写入 null）或其他不受控来源时，非空声明不保证运行时非 null，== null 分支可能可达，回源码看数据的实际来源再判断（依据：kotlinlang.org Java interop 的 null safety and platform types 一节，2026-10-15 访问）；collectAsState(initial) 加受控 getter 映射这类来源仍按非空处理

## 原因

Kotlin 非空类型在编译期保证非 null 时，与 null 的 == 比较恒为 false、!= 比较恒为 true；把 == null 读成“未初始化/首次进入”，会凭空造出可达的弹窗或权限请求，并反推出源端没有的三态偏好键，再经规格传给偏好层、协调服务与验收条目。

## 做法

1. 遇到对状态变量的 == null / != null 判断，先查声明类型和来源：collectAsState 的 initial 值、Flow getter 的映射（== true、?: 默认值）。来源在编译期保证非空时，在规格中记为“== null 恒假、从不触发”或“!= null 恒真、总是触发”。
2. 偏好默认值以 getter 的实际映射为准；同一规格里“默认 false”与“== null 表示未写入”矛盾时回源码裁决，不从一个条件表达式反推三态键或新增 hasKey 语义。
3. 按规格新增弹窗、权限请求或协调服务前，确认该分支在源端可达；规格的三态条件与源码非空类型冲突时，按源端可观察行为实现（不新增该触发），并把冲突回报规格。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3b4906429163bc7ea455](../../../store/cases/case-3b4906429163bc7ea455/85f96a8b2f7d0006cb872bae5e3e5fdc072ca256a8506124f7080b08fbd23330.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`85f96a8b2f7d0006cb872bae5e3e5fdc072ca256a8506124f7080b08fbd23330`
