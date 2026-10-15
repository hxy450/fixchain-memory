# 目标用 A2DP、HFP 等分协议回调判断耳机连接时按设备聚合：所监听协议都断开才判定设备断开，成功提示以回调或回读确认

ID：`lesson-ecc67592eba3402c0a1f` · 版本：3

[本主题](index.md)

## 何时使用

实现蓝牙设备连接、断开状态与“连接/断开成功”判定时

## 适用情境

源端用 ACTION_ACL_CONNECTED/ACTION_ACL_DISCONNECTED 等设备级广播判断连接与断开；目标改用 A2DP、HFP 等分协议的 connectionStateChange 回调，同一耳机常同时挂多个协议。

## 例外与边界

- 源端本身只监听某一 profile 的 ACTION_CONNECTION_STATE_CHANGED（如只关心 A2DP 播放）时，按该协议判定，不做设备聚合

## 原因

单个协议断开不代表设备断开；把首个 false 当成设备断开或“断开成功”，会误清列表、误报成功；连接成功若在发起时就显示，也会与系统状态不符。

## 做法

1. 维护“设备 → 各协议状态”，任一协议仍为连接，或各协议 getConnectedDevices 的并集中仍含该设备时，不判定断开或断开成功。
2. 连接、配对、断开的成功提示都在收到系统回调或回读确认后再显示。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c9f54856d3fb74cbd54b](../../../store/cases/case-c9f54856d3fb74cbd54b/44393c2b1eb069a8783fb6cdaf2173655cd8ced3e5c347c5d8df872baf20fba2.json) · 结论：diagnosis, recommendation:3
  卡片版本：`44393c2b1eb069a8783fb6cdaf2173655cd8ced3e5c347c5d8df872baf20fba2`
