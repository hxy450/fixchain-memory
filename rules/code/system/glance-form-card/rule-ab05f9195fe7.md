# FormDimension 档位当兜底 hint 时，按各档实际 vp 宽对照源断点换算形态

审的是：代码
触发（任一种）：
- 读到：源端 Glance 按 LocalSize 的 dp 宽高断点选形态；写错的样子：按 Dimension_1_2 / Dimension_2_2 / Dimension_2_4 一档对一种形态写死映射（如 2*2→中、2*4→大），没有和源断点比
适用范围：服务卡片在拿到实际宽高之前、或拿不到时，用 FormDimension 档位推形态
做法：
- 先按手机上各档的实际宽估值（2*2 约 160vp、2*4 约 330vp），拿源端宽度断点比，落在哪一段给哪种形态；只看高度的分支同样按各档高度比，只给够高的档（如 4*4）
- 这张映射表只作兜底；实际宽高仍由 getFormRect / onSizeChanged 下发后覆盖
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Dimension_1_2 = 1、Dimension_2_2 = 2、Dimension_2_4 = 3、Dimension_4_4 = 4：FormDimension 的枚举值，`ohos.extra.param.key.form_dimension` 读到的是这些数字（出处：鸿蒙 SDK 的 ets/api/@ohos.app.form.formInfo.d.ts，formInfo.FormDimension）
- 手机上 2*2 约 160vp 宽、2*4 约 330vp 宽：按源断点换算时用的估值（出处：卡里修好并验证过）
针对本应用要查的：
- 源端的宽高断点：源工程里 Glance 内容 Composable 中对 LocalSize.current.width、height 的比较；拿各档估值逐一比，得出每档对应的形态
未核实：2*2、2*4 的 vp 宽是卡里按手机估算的，不同设备桌面不同
来源：1 张卡，1 个应用
- case-77c6596fcdf362f9e832（Jetsnack）：做法第 1 步 ← 建议 4；做法第 2 步 ← 建议 1、建议 4；取值 2 ← 建议 4
