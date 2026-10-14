# values-swNNNdp分档按设备最短边dp判档，不换成窗口宽断点

ID：`lesson-9d9da10ec790154f53de` · 版本：1

[本主题](index.md)

## 何时使用

规格提取、派工与界面实现阶段，把swNNNdp限定符的多档取值翻译成目标端选档逻辑时

## 适用情境

源工程用values-swNNNdp为同一dimen提供多档取值，目标端没有等价资源限定符，需要在代码中按设备尺寸选档。

## 原因

sw判档量是设备最短边dp，资源装载时选定，与方向和窗口宽无关；窗口宽断点是另一个量，横屏或窗口变化时会选错档；运行时条件写法未经实测，也可能在目标机上整体不生效。

## 做法

1. 规格写明判档量（min(宽,高)/密度）、各档阈值和无限定符的默认档。
2. 实现时用display.getDefaultDisplaySync()计算最短边vp，按阈值取档，在组件初始化时选定。
3. 若改用mediaquery等运行时条件判档，至少用一次日志或设备读数确认各档条件的实际取值；无法核对时改用可直接计算的尺寸来源。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-54a52d5695dea4698a31](../../../store/cases/case-54a52d5695dea4698a31/4dc5f3295462170d0e4f6d531d425237b4d789eff42d88bdffb7be637b173bbb.json) · 结论：diagnosis, recommendation:1, recommendation:3, recommendation:4
  卡片版本：`4dc5f3295462170d0e4f6d531d425237b4d789eff42d88bdffb7be637b173bbb`
