# 共享单例 ViewModel 按规格的键丢弃过期响应，页面各加载入口先做单飞，不写成“新请求取消上一请求”

ID：`lesson-c883a0ff96c32dfbd9ba` · 版本：4 · 阶段：execute · 主题：[ui/state/lifecycle](index.md)

概要：共享单例按键丢弃过期响应，加载入口先单飞不取消上一请求

信号：`onRefreshing`, `Refresh`, `@Monitor`, `aboutToAppear`, `areaId`

## 何时使用

页面接线阶段，把 aboutToAppear、Refresh 的 onRefreshing、@Monitor 等多个加载入口接到共享单例 ViewModel 或 Service 时

## 适用情境

目标 ViewModel 为单例，run() 对任何新请求先取消上一请求；页面同时存在 aboutToAppear、Refresh（refreshing 初值可能为 true）与切城监听等入口；规格要求按 areaId 一类键丢弃旧城市的迟到响应、一次刷新只产生一次请求。

## 原因

把取消语义写成“任何新请求取消上一请求”，同一城市的两个入口几乎同时触发时，第二次调用会取消第一次的并发请求，双方互相取消或销毁响应，页面进入失败态。来源中同一实例初始化时触发了两次加载，真机日志先出现一组 cancelled、随后一组失败；加上单飞保护后只剩一组请求。

## 做法

1. 共享单例的取消语义按规格键实现：以 areaId 等作为 generation key，只丢弃旧键的迟到响应；同键的重复调用合并或复用在途请求。
2. 页面接线时列出所有加载入口（生命周期、Refresh 初值与 onRefreshing、@Monitor），调用单例加载方法前加单飞或在途复用，并核对冷启动时实际触发了几次。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [PowerShell 读文件带 UTF8 编码，乱码视为未读](../../../process/unloaded-input/lesson-6a3a7f46c8fec282affa.lesson.md)（共享 1 张卡）
- [规格与源码冲突时按源端语义实现并标注差异](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）
- [多路聚合缓存至少一路成功才写，命中校验时效和载荷](../../../data/sync/lesson-c6379cfcbee86500f91f.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-fa7bbda457517260efc4](../../../../../store/cases/case-fa7bbda457517260efc4/58d73cfa31553fee929796eb72c6f37fc2faba952a2e2f334aa420b8f0325b08.json) · 结论：diagnosis, rec-c545d04c00, rec-e2d94b7336
  卡片版本：`58d73cfa31553fee929796eb72c6f37fc2faba952a2e2f334aa420b8f0325b08`
