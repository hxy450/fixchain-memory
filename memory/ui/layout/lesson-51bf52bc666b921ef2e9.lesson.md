# values-sw<N>dp(-land) 覆盖按设备屏幕短边 min(宽,高) 判定再叠加方向，不译成 mediaquery min-width

ID：`lesson-51bf52bc666b921ef2e9` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，把源端 sw<N>dp 限定目录（可带 -land/-port）的覆盖值落成运行期分支时

## 适用情境

源 res 有 values-sw720dp-land 一类最小宽度限定目录，覆盖尺寸、边距等取值，注释常写“for sw720dp devices (e.g. 10" tablets)”；目标没有对应资源限定词，要在运行期按屏幕配置取值，可用 mediaquery 或 display 查询；规格里写成“横屏 + 最小宽度≥N”。

## 例外与边界

- 源限定目录是 values-w<N>dp、values-h<N>dp（当前可用宽高）：按当前窗口宽高取值，不按短边

## 原因

sw<N>dp 比较的是设备屏幕短边（smallestScreenWidthDp），与方向无关：手机横屏时当前宽可以超过平板阈值，短边却远小于它。ArkUI mediaquery 的 min-width/width 比较当前窗口宽，把“最小宽度≥N”对译成 (min-width: Nvp) 会让手机横屏也命中平板覆盖值。规格的中文“最小宽度”与媒体特性 min-width 同名，容易被直接对译。

## 做法

1. 按短边判定：从 display.getDefaultDisplaySync() 取宽高（px 换成 vp），取较小者与阈值 N 比较，再按限定目录与当前方向组合（-land 即横屏且短边≥N）；方向或窗口变化时重算。不用 mediaquery 的 min-width/width 代替短边条件。
2. 规格登记 sw 覆盖时写明判定量是设备短边、与方向无关，再写方向条件，并给出手机横屏不命中的样例；不只写“最小宽度”。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-db3da49c14f06085f3b8](../../../store/cases/case-db3da49c14f06085f3b8/c679bb6c86541e5f34f87ce8cdf2a5916c70d1427e62bba1d5228300a4ad8967.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`c679bb6c86541e5f34f87ce8cdf2a5916c70d1427e62bba1d5228300a4ad8967`
