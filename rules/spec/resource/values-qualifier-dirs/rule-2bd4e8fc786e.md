# 规格登记 sw 限定目录覆盖时，写明判定量是屏幕短边 min(宽,高)、与方向无关，再叠方向

审的是：规格
触发（任一种）：
- 读到：源工程有 values-sw<N>dp 或 values-sw<N>dp-land 限定目录里的覆盖值（注释常写给平板用）；写错的样子：规格只写“横屏 + 最小宽度≥N”或“断点宽 N vp + 横屏”，没写明比较的是设备屏幕短边 min(宽,高)、与方向无关，也没举手机横屏不命中的例子
适用范围：规格提取阶段登记最小宽度（sw）限定目录的覆盖、要求目标运行期取值时
做法：
- 规格里写成：判定量是设备屏幕短边 min(宽, 高)（vp），与方向无关；-land 目录再叠加横屏条件；并举例“手机横屏时窗口宽超过 N，但短边不足 N，不命中”
- 不只写“最小宽度”四个字：它和 mediaquery 的 min-width 同名，后者比的是当前窗口宽
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- smallestScreenWidthDp 是 screenWidthDp 与 screenHeightDp 在竖屏、横屏两种方向下的最小值，对应 smallest width 资源限定符：sw 限定符的判定量是短边，与当前方向无关（出处：android.content.res.Configuration#smallestScreenWidthDp）
- mediaquery 的 min-width：应用页面可绘制区域的最小宽度：比的是当前窗口宽，手机横屏也会超过阈值，和 sw 不是一回事（出处：arkts-layout-development-media-query.md，媒体特征（media-feature））
来源：1 张卡，1 个应用
- case-db3da49c14f06085f3b8（Sokoban）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断
