# 源 @dimen 有宽度限定覆盖时，目标按窗口宽度取值，不写单值 $r('app.float…')

审的是：代码
触发（任一种）：
- 读到：源布局用 @dimen/… 设 padding 或 margin，而源 res 的 values-w<N>dp 或 values-sw<N>dp 下的 dimens.xml 覆盖了同名键；写错的样子：目标各处写成 $r('app.float.…') 单值（只有基础值）；或者把水平、垂直等几个源 dimen 合成一个常量
适用范围：界面实现阶段，源布局引用的 dimen 在宽度、最小宽度限定目录里有覆盖时
做法：
- 在共享窗口模型里存当前窗口宽（vp）：EntryAbility 里先取一次，再用 mainWindow.on('windowSizeChange', (size) => { … }) 更新，size.width 是 px，先 px2vp；提供一个取值方法：可用宽 ≥ 阈值返回覆盖值，否则返回基础值
- 引用这个 dimen 的各处统一调用该方法，不再用 $r('app.float.…')；源端是不同 dimen 的（水平、垂直边距）即使基础值相同也分开取值
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- on(type: 'windowSizeChange', callback: Callback<Size>): void：Window 的窗口尺寸变化回调（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.on('windowSizeChange')）
- Size.width：窗口宽度，单位为 px：回调里的宽度要先 px2vp 再和 dp 阈值比较（出处：arkts-apis-window-i.md，Size）
- getWindowProperties(): WindowProperties，其中 windowRect: Rect：启动时取一次当前窗口的位置和大小（出处：鸿蒙 SDK 的 ets/api/@ohos.window.d.ts，Window.getWindowProperties / WindowProperties.windowRect）
- Configuration.screenWidthDp 对应 available width 资源限定词：values-w<N>dp 的阈值比较的是应用可用显示区的宽度（dp）（出处：android.content.res.Configuration#screenWidthDp）
- 共享窗口模型存窗口宽、EntryAbility 同步窗口宽并监听 windowSizeChange、取值方法按阈值返回覆盖值或基础值；各页改用该方法后宽窗口取到覆盖值：返修后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- 被覆盖的键、基础值、覆盖值和阈值：源工程 res 下 values-w<N>dp、values-sw<N>dp 目录里的 dimens.xml，和 values/dimens.xml 按键名对照；目录名里的 N 是阈值（dp，比较时当 vp）；两边同名键的值分别是覆盖值和基础值，dp 写成 vp
来源：1 张卡，1 个应用
- case-99fd06c7bad0581426fb（Privacy Friendly 2048）：做法第 1 步 ← 诊断、建议 3；做法第 2 步 ← 建议 3、诊断；取值 5 ← 诊断
