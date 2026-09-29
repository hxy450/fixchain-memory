# APPROXIMATELY_LOCATION 与 LOCATION 按一组判定：任一授予就继续定位，不套用“全部授予”的通用权限模板

ID：`lesson-b72e0d67fe27db2ae041` · 版本：1

[本主题](index.md)

## 何时使用

定位能力实现阶段，编写定位权限申请结果的判定逻辑时

## 适用情境

目标同时申请 ohos.permission.APPROXIMATELY_LOCATION 与 ohos.permission.LOCATION；工程 skill 提供通用的权限辅助模板（遍历 authResults，任一不为 0 即返回失败）；功能规格只要求两项权限都声明、都处理。

## 原因

用户可以只授予模糊位置，此时精确权限为拒绝；按“全部授予”判定会把这种情况当成无权限，定位按钮直接失败。来源中实现者照搬通用模板写出全部授予的循环，skill 与规格都没有说明定位权限组可以只授予模糊位置。

## 做法

1. authResults 中任一定位权限授予（至少模糊位置为 0）就继续定位；只有精确权限缺失时按降级精度处理，两项都拒绝才走失败提示。

## 来源（按需复核）

- case-f9c6cd0dc22c13bdcdd8 · 结论：diagnosis, recommendation:1
  卡片版本：`0733ddacf58cadb79303b036efa25804fce5a35e5d75266245e127e5c75299d3`
