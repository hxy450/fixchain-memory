# 给接口或类类型的参数传实现对象时按声明来源选写法：SDK 声明的类型用带类型标注的对象字面量，项目自定义的方法接口用 implements 具名类

ID：`lesson-931ef95a3d0cf202fe5b` · 版本：2

[本主题](index.md)

## 何时使用

实现、修复或收口接线阶段，为 errorManager.on('error') 一类系统 API 准备观察者对象，或把依赖对象交给只含方法签名的端口接口、把已有类实例传给新声明的接口参数时

## 适用情境

要传入的类型或由 SDK d.ts 声明（如 application/ErrorObserver.d.ts 的 export default class ErrorObserver），或是项目自定义、只声明方法的依赖接口；写者按 TS 习惯准备 implements 一个 class，或用箭头函数属性的对象字面量实现项目接口，或把结构上恰好具备这些方法、却未声明 implements 的已有类实例直接传入；生成或修复 worker 可能被要求不自行编译。

## 例外与边界

- 只含数据属性的接口或 class，按对象字面量落到具名类型的经验（lesson-1696967d1320c7735732）处理

## 原因

ArkTS 的 implements 只接受 interface（arkts-implements-only-iface），TS 中“class 可当接口被 implements”的写法会编译失败；ArkTS 不做结构化匹配（arkts-no-structural-typing），未声明 implements 的类实例不能当作该接口传入。arkts-no-untyped-obj-literals 对 SDK 声明的类型放行带类型标注的对象字面量，对项目自定义、含方法成员的类型仍报错，先赋给接口类型变量也一样（ets-loader 内置 typescript.js 的字面量校验对库类型放行、对含方法的类型拒绝）。

## 做法

1. 写前在 d.ts 或项目源码确认该类型由谁声明、是 class 还是 interface、是否含方法成员。
2. SDK 声明的观察者或回调类型（class 或 interface）写成以该类型标注的对象字面量，例如 const observer: errorManager.ErrorObserver = { onUnhandledException: (errMsg: string): void => {...}, onException: (errObject: Error): void => {...} }，再传给 errorManager.on('error', observer)，持有它的字段也标注为 SDK 类型；SDK 类型是 class 时不写 implements。
3. 项目自定义、只含方法签名的接口写 class XxxImpl implements Port { ... } 并传入实例；把已有类实例交给新接口时，写一个 implements 该接口、内部委托给原实例的适配类，或让原类声明 implements，参照工程中已有的“仓库类 implements 端口接口”写法。

来源支持：3 张卡 · 2 次迁移 · 2 个应用

## 来源（按需复核）

- [case-28990049b25bf1086836](../../../store/cases/case-28990049b25bf1086836/4c3037100e303a3b9a9c78b8d172f92cb23342e0be0d2c8c467948a720e3723f.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`4c3037100e303a3b9a9c78b8d172f92cb23342e0be0d2c8c467948a720e3723f`
- [case-5f5a856b7e04d91c8df6](../../../store/cases/case-5f5a856b7e04d91c8df6/1022293315e5d10096ff8b590e372e0de193a15e336419212c60205dc11720fe.json) · 结论：diagnosis, recommendation:3
  卡片版本：`1022293315e5d10096ff8b590e372e0de193a15e336419212c60205dc11720fe`
- [case-ca8dec09be8655edbb02](../../../store/cases/case-ca8dec09be8655edbb02/dfbbf6d269dc5f5443ab807c7dcd9499347ae85860a1e024533fbcff818efb49.json) · 结论：diagnosis, recommendation:5
  卡片版本：`dfbbf6d269dc5f5443ab807c7dcd9499347ae85860a1e024533fbcff818efb49`
