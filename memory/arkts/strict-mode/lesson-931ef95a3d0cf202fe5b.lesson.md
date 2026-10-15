# 只含方法签名的自定义接口用 implements 它的具名类实现：不传箭头函数对象字面量；已有类实例交给新声明的接口参数时写适配类，ArkTS 不做结构化匹配

ID：`lesson-931ef95a3d0cf202fe5b` · 版本：1

[本主题](index.md)

## 何时使用

实现或收口接线阶段，把依赖对象交给只含方法签名的端口或依赖接口，或把已有类实例传给新声明的接口参数时

## 适用情境

项目自定义的依赖接口只声明方法；写者准备用箭头函数属性的对象字面量直接传参或先赋给该接口类型的变量，或把结构上恰好具备这些方法、却未声明 implements 的已有类实例直接传入。

## 例外与边界

- 接口类型由 SDK 声明为 class 时，按 SDK 观察者类型的写法传入以该类型标注的对象字面量

## 原因

ArkTS 不支持结构化类型（arkts-no-structural-typing），已有类没有声明 implements 时不能当作该接口传入；只含方法签名的接口用对象字面量实现，先赋给接口类型变量也仍报 arkts-no-untyped-obj-literals。来源中 skill 只给了“赋给类型变量”的修法，修复者照此改后同一规则仍报错，改成实现接口的具名类才通过。

## 做法

1. 写 class XxxImpl implements Port { ... } 并传入实例；把已有类实例交给新接口时，写一个 implements 该接口、内部委托给原实例的适配类，或让原类声明 implements，参照工程中已有的“仓库类 implements 端口接口”写法。

来源支持：2 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5f5a856b7e04d91c8df6](../../../store/cases/case-5f5a856b7e04d91c8df6/1022293315e5d10096ff8b590e372e0de193a15e336419212c60205dc11720fe.json) · 结论：diagnosis, recommendation:3
  卡片版本：`1022293315e5d10096ff8b590e372e0de193a15e336419212c60205dc11720fe`
- [case-ca8dec09be8655edbb02](../../../store/cases/case-ca8dec09be8655edbb02/dfbbf6d269dc5f5443ab807c7dcd9499347ae85860a1e024533fbcff818efb49.json) · 结论：diagnosis, recommendation:5
  卡片版本：`dfbbf6d269dc5f5443ab807c7dcd9499347ae85860a1e024533fbcff818efb49`
