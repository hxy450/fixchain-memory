# 自定义组件的状态成员不与组件通用属性方法同名（position、width、height、id、visibility、enabled、zIndex、opacity 等）

ID：`lesson-c1968bdf112ed3e6b259` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段为组件状态接口表命名 @Local/@Param 变量，或界面实现阶段在自定义组件 struct 中声明成员时

## 适用情境

把源端事件或模型的字段名（如播放进度事件的 position）直接转写成组件成员；规格的状态接口表就是实现的成员表，实现者按表照写。

## 原因

自定义组件继承的 CustomComponent 上已有同名的通用属性方法，成员与之同名时赋初值会被当成给该方法赋值，编译报 Type 'number' is not assignable to type '(value: Position | Edges | LocalizedEdges) => CommonAttribute' 一类错误。来源中规格作者与实现者都预载了列出这些保留名的规则，仍沿用源字段名 position；偏差先在规格表形成，实现者照写时又没有对照。

## 做法

1. 把源字段名转成成员名前对照组件通用属性清单（position、width、height、id、visibility、enabled、zIndex、opacity 等），同名就改为带语义前缀的名字（如 playbackPosition），并在规格表里写出成员名与源字段的对应。
2. 实现时即使规格已给出成员名也再对照一次；该限制适用于所有自定义组件 struct，不只页面。发现规格名冲突时改名并回写规格。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-d33b282e5bf383e03328](../../../store/cases/case-d33b282e5bf383e03328/1dda694184b7fe969b4168eab455475da924bf8c39cf9e3dcdcb55cc6c09b7d4.json) · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`1dda694184b7fe969b4168eab455475da924bf8c39cf9e3dcdcb55cc6c09b7d4`
