# V1 服务卡片页里由状态派生的值写成 build 内调用的普通方法，不写 struct 的 get 访问器

ID：`lesson-1baf94e39d4a01043d9e` · 版本：2

[本主题](index.md)

## 何时使用

服务卡片实现阶段，在 V1 @Entry 卡片页里由尺寸等状态派生布局值或样式时

## 适用情境

目标为 ArkTS 服务卡片的 V1 卡片页（@Entry struct + @LocalStorageProp），实现者准备在 struct 里写 get 访问器（如 get layoutSize()）派生档位或样式。

## 原因

已观察到的卡片工具链中，V1 卡片页 struct 的 get 访问器不在转译产物里，运行时取到 undefined，派生值恒走默认分支，编译不报错。该现象只在一个 SDK 版本的编译产物中确认，其他版本是否相同未知；改写成普通方法后该版本的派生值随尺寸生效，这种写法也不依赖 getter 是否被保留，所以不必先判断版本。

## 做法

1. 派生值写成普通方法并在 build 内调用（如 layoutSize()），不写 struct getter。

## 可选检查

- 派生值是否生效有疑问时，查编译产物（entry/build 下 CompileArkTS 的输出）中该方法仍在，或在卡片加日志确认。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-77c6596fcdf362f9e832](../../../store/cases/case-77c6596fcdf362f9e832/c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a.json) · 结论：diagnosis, recommendation:3
  卡片版本：`c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a`
