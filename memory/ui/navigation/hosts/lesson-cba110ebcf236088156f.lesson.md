# Navigation 的 .navDestination 直接传 @Builder 方法，不包箭头函数

ID：`lesson-cba110ebcf236088156f` · 版本：2

[本主题](index.md)

## 何时使用

入口页实现与收尾接线阶段，编写 Navigation 的 navDestination 分发时；冷启动日志出现 Builder function is empty 时

## 适用情境

入口 Navigation 用 @Builder 方法按名称分发目的地（如 pageMap），写成 .navDestination((name, param) => { this.pageMap(name, param) }) 一类箭头包装。

## 例外与边界

- 向自定义组件的 @BuilderParam 槽传页面内容不适用本条：那里按箭头闭包只调用 @Builder 的规则写（见 lesson-7d643db6ab406ae64c77）

## 原因

在已观察的工具链（target SDK 6.1.1(24)）中，.navDestination 收到箭头函数包装时，冷启动日志出现 Builder function is empty，目的地构建为空。其他 SDK 版本上箭头包装是否同样失败未验证；直接传方法在已观察版本可用，统一这样写不受此未知项影响。

## 做法

1. .navDestination 直接传 @Builder 方法，如 .navDestination(this.pageMap)，不包箭头函数；冷启动后检查日志没有 Builder function is empty。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-5fcc464cf9b9cd1034f1](../../../../store/cases/case-5fcc464cf9b9cd1034f1/5731c96e6de78b4e563facc594dbf9753ef8665bb26d0dbae0ec029e58adc7d5.json) · 结论：diagnosis, recommendation:2
  卡片版本：`5731c96e6de78b4e563facc594dbf9753ef8665bb26d0dbae0ec029e58adc7d5`
