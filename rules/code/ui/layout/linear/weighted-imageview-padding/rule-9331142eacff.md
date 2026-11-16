# layout_weight 定高的 ImageView 带大 padding，不直接放到 Image 上

审的是：代码
触发（任一种）：
- 读到：ImageView 的 android:layout_height="0dp" 加 android:layout_weight，同时带 android:padding（上下之和可能超过分得的槽高，横屏时尤其）；写错的样子：写成 Image(...).layoutWeight(...).padding(...)，把源端 padding 直接放在 Image 上
适用范围：安卓纵向 LinearLayout 里按 layout_weight 分高的 ImageView 带固定的大内边距、槽高可能小于上下内边距之和时
做法：
- 外层用容器（如 Stack）占这个槽位并写 .layoutWeight(<layout_weight>)，用 .onSizeChange((oldValue, newValue) => …) 取实际槽高
- Image 不带 padding，绘制高度取 |槽高 − 上下 padding 之和|；槽高小于 padding 之和时给 Image 加 .rotate({ angle: 180 })
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- final int vheight = getHeight() - mPaddingTop - mPaddingBottom：源端内容高 = 视图高减上下 padding，槽高小于 padding 之和时为负（出处：android.widget.ImageView#configureBounds）
- 源端内容高为负时 FIT_CENTER 得到负缩放，按 |内容高| 倒置绘制；ArkUI Image 的 padding 会把组件撑到至少 padding 之和：两端在小槽高下行为不同，不能直译 padding（出处：卡里修好并验证过）
- onSizeChange(event: SizeChangeCallback): T：布局引起的尺寸变化时回调，用来取槽高（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onSizeChange）
- type SizeChangeCallback = (oldValue: SizeOptions, newValue: SizeOptions) => void：newValue.height 是新的槽高（出处：鸿蒙 SDK 的 ets/component/common.d.ts，SizeChangeCallback）
- layoutWeight(value: number | string): T：槽位容器按源端 layout_weight 分高（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight）
- rotate(value: RotateOptions): T；x、y、z 都不指定时旋转轴默认 (0, 0, 1)：rotate({ angle: 180 }) 即在平面内转 180°（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.rotate；ts-universal-attributes-transformation.md，rotate）
- setOnSizeChange(callback: SizeChangeCallback | undefined): void：同族接口：UICommonEvent 上设置尺寸变化回调（出处：鸿蒙 SDK 的 ets/component/common.d.ts，UICommonEvent.setOnSizeChange）
针对本应用要查的：
- 这个槽位在横竖屏下可能的最小高度：源工程的布局 XML（含 layout-land 等限定目录）里同一纵向 LinearLayout 的各子项 layout_weight 和定高子项；按权重比例估算槽高，与上下 padding 之和比较；可能更小就按本条写
未核实：卡里上机的行为出自 HarmonyOS 6.1.1（API 24），本机声明按 API 23 核实
来源：1 张卡，1 个应用
- case-5916095777c21ec74389（omni-notes-hmos）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3、诊断；取值 2 ← 诊断
