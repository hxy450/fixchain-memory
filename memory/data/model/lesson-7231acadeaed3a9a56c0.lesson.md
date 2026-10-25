# 响应 DTO 按 SDK data class 逐字段建模：平铺还是嵌套、可空性与名称相近的字段分别写明，页面按源端访问路径取值

ID：`lesson-7231acadeaed3a9a56c0` · 版本：1

[本主题](index.md)

## 何时使用

API 清单与规格提取阶段整理共享响应 Bean 字段表时；数据模型与页面实现阶段把源端字段访问映射到目标 DTO 时

## 适用情境

源端经第三方 SDK 的 kotlinx.serialization data class 直接反序列化 JSON（字段名即 wire key），SDK 源码不在工程内但可下载；目标手写 DTO 并用 JSON.parse 直转；视图类型里可能有平铺字段而非嵌套 *View 的类型，或名称相近、语义不同的字段（作者被本社区封禁与当前用户被封禁）。

## 原因

JSON.parse 直转时，声明错的字段在运行期恒为 undefined 而不报错：平铺结构被概括成嵌套包装，列表读不到数据；漏掉某个字段后，页面改读名称相近的另一字段，显示的是另一种语义。规格里的概括会被 DTO 照抄，页面再按 DTO 误映射。

## 做法

1. 规格按 SDK data class 逐字段写共享响应 Bean：平铺或嵌套、可空性与默认值，只列源码中真实存在的字段，名称相近的字段分别写语义；SDK 源码是临时下载的时，把下载坐标或完整字段表交给 DTO 实现者，引用的子类型先读到定义。
2. 实现 DTO 时，规格只有文字概括的嵌套结构先检索源端消费点（如 reportView.post、commentView.creator_xxx）核对访问路径，与规格冲突时以 SDK 为准并回报。
3. 页面映射字段时，DTO 缺字段就按源端字段名窄化读取并登记 DTO 缺口，不改用名称相近、语义不同的字段。
4. 与主接口协议不同的响应（如 nodeinfo）按其协议命名，不套用主接口的 snake_case 约定；规格只写 Object 时先查 SDK 定义再写子字段。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bb262f5910f2bb20c35d](../../../store/cases/case-bb262f5910f2bb20c35d/0aa0263a00188f45426cf254ea881a05a6ba0e642f711feb90390c3cfde58c3f.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4, recommendation:5
  卡片版本：`0aa0263a00188f45426cf254ea881a05a6ba0e642f711feb90390c3cfde58c3f`
