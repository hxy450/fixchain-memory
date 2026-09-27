# 共享单例 ViewModel 按规格的键丢弃过期响应，页面各加载入口先做单飞，不写成“新请求取消上一请求”

ID：`lesson-c883a0ff96c32dfbd9ba` · 版本：1

[本主题](index.md)

## 何时使用

页面接线阶段，把 aboutToAppear、Refresh 的 onRefreshing、@Monitor 等多个加载入口接到共享单例 ViewModel 或 Service 时

## 适用情境

目标 ViewModel 为单例，run() 对任何新请求先取消上一请求；页面同时存在 aboutToAppear、Refresh（refreshing 初值可能为 true）与切城监听等入口；规格要求按 areaId 一类键丢弃旧城市的迟到响应、一次刷新只产生一次请求。

## 原因

把取消语义写成“任何新请求取消上一请求”，同一城市的两个入口几乎同时触发时，第二次调用会取消第一次的并发请求，双方互相取消或销毁响应，页面进入失败态。来源中同一实例初始化时触发了两次加载，真机日志先出现一组 cancelled、随后一组失败；加上单飞保护后只剩一组请求。

## 做法

1. 共享单例的取消语义按规格键实现：以 areaId 等作为 generation key，只丢弃旧键的迟到响应；同键的重复调用合并或复用在途请求。
2. 页面接线时列出所有加载入口（生命周期、Refresh 初值与 onRefreshing、@Monitor），调用单例加载方法前加单飞或在途复用，并核对冷启动时实际触发了几次。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-fa7bbda457517260efc4 · 结论：diagnosis, recommendation:3, recommendation:4
  卡片版本：`13060717bdfc19afb975d9cd93d6c841d9e637fde59c3eb5f8e6b8ab8e892577`
