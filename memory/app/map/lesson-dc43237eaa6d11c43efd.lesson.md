# 系统 geoLocationManager 定位结果（WGS-84）交给高德地图的相机中心或当前位置显示前，先转换为 GCJ-02

ID：`lesson-dc43237eaa6d11c43efd` · 版本：2

[本主题](index.md)

## 何时使用

定位与地图接线阶段，把系统定位坐标交给高德等使用 GCJ-02 的地图 SDK 接口时

## 适用情境

定位来源是 HarmonyOS geoLocationManager.getCurrentLocation（返回 WGS-84），底图与当前位置显示用高德鸿蒙 SDK（GCJ-02）；源端 Android 可能直接用高德定位 SDK，结果本就是 GCJ-02。

## 例外与边界

- 定位来源已是高德定位 SDK 等返回 GCJ-02 的接口，或坐标已在其他层转换过时，不再重复转换

## 原因

GCJ-02 是在 WGS-84 上加偏后的坐标系，两者在国内存在偏移；不转换时相机中心与当前位置蓝点错位。源端用高德定位 SDK 时不需要这一步，换成系统定位后容易漏掉。

## 做法

1. 确认定位坐标的来源坐标系：geoLocationManager 结果为 WGS-84，高德地图的相机与当前位置显示按 GCJ-02 解释；要把坐标交给高德其他接口（如周边搜索中心）时，先读该接口 d.ets 的坐标系说明再决定是否转换。
2. 进入高德接口前用 SDK 的 CoordinateConverter（GPS 类型）或参考工程已有的坐标适配器转换一次，集中在定位结果出口处，避免多处重复转换。

## 可选检查

- 真机上比对相机中心点与当前位置蓝点是否重合。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-f9c6cd0dc22c13bdcdd8](../../../store/cases/case-f9c6cd0dc22c13bdcdd8/49829f5fdc419a33101e6e6ef4b3c0cc17771d6649145267def11b9498e45dfc.json) · 结论：diagnosis, recommendation:3
  卡片版本：`49829f5fdc419a33101e6e6ef4b3c0cc17771d6649145267def11b9498e45dfc`
