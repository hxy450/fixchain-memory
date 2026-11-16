# Balloon 的 setBackgroundColor 迁到 bindPopup 时写 popupColor 并关模糊

审的是：代码
触发（任一种）：
- 读到：源端 skydoves `Balloon.Builder` 调了 `setBackgroundColor(…)`，颜色作用于整个气泡（含箭头）；写错的样子：目标 `bindPopup` 的 `CustomPopupOptions` 没有 `popupColor`，只给 builder 里的 `Column` 加了 `.backgroundColor(…)` 和 `.borderRadius(…)`；或注释里写「PopupOptions 不支持背景色」
适用范围：把 Balloon、Tooltip 这类整体着色的第三方气泡迁成 ArkUI bindPopup 加自定义 builder 时
做法：
- bindPopup(show, { builder, popupColor: <源 setBackgroundColor 的颜色>, backgroundBlurStyle: BlurStyle.NONE, radius: <源圆角> })，颜色加在 popup 容器上，不只加在 builder 内容上
- 认定目标「不支持」某个源端能力前先查 CustomPopupOptions 的字段；确实只能近似时，在占位登记或转换报告里登记，供视觉验收核对
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- bindPopup 补上 popupColor、backgroundBlurStyle: BlurStyle.NONE、radius 后，箭头和外框与内容同色：修好的写法（出处：卡里修好并验证过）
- popupColor?: Color | string | Resource | number，默认 TRANSPARENT 加 COMPONENT_ULTRA_THICK；要去掉背景模糊需把 backgroundBlurStyle 设为 BlurStyle.NONE：CustomPopupOptions 的气泡颜色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomPopupOptions.popupColor）
- backgroundBlurStyle?: BlurStyle，默认 BlurStyle.COMPONENT_ULTRA_THICK；BlurStyle.NONE = 7（不模糊）：不关模糊时底色是透明加模糊（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomPopupOptions.backgroundBlurStyle、BlurStyle.NONE）
- radius?: Dimension，默认 20.0_vp：气泡圆角，源端圆角要显式写（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CustomPopupOptions.radius）
- bindPopup(show: boolean, popup: PopupOptions | CustomPopupOptions): T：绑定气泡（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.bindPopup）
- popupColor?: Color | string | Resource | number：同族接口：PopupOptions（非自定义气泡）的颜色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，PopupOptions.popupColor）
- popupColor?: ResourceColor：同族接口：PopupCommonOptions 的颜色（出处：鸿蒙 SDK 的 ets/component/common.d.ts，PopupCommonOptions.popupColor）
针对本应用要查的：
- 源气泡的颜色和圆角：源工程构建 Balloon 的代码里 setBackgroundColor / setCornerRadius 的参数，颜色引用到 res/values 的 colors.xml 或主题属性；解析出具体颜色值填 popupColor，圆角数值（dp）填 radius
来源：1 张卡，1 个应用
- case-1907ba587e6b1439f17d（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 3；取值 1 ← 诊断
