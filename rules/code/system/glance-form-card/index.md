# Glance 桌面小部件迁成服务卡片

agent 会看到什么：读到源端 GlanceAppWidget（SizeMode.Exact、按 LocalSize.current 的宽高断点选布局），产物里是 FormExtensionAbility 下发卡片尺寸、FormDimension 档位映射，以及卡片页里用到的事件、组件和 struct 写法

## 规矩

- rule-ea9d770a8a7a｜Glance 按实际宽高选布局时，由 FormExtensionAbility 取卡片尺寸下发给卡片页｜读到：GlanceAppWidget 设 SizeMode.Exact，按 LocalSize.current 的宽高分支布局；规格写按实际尺寸渲染；写错：EntryFormAbility 只按 `ohos.extra.param.key.form_dimension` 的档位映射形态，没有 getFormRect 调用和 onSizeChanged；卡片页没有 @LocalStorageProp 宽高
- rule-ab05f9195fe7｜FormDimension 档位当兜底 hint 时，按各档实际 vp 宽对照源断点换算形态｜读到：源端 Glance 按 LocalSize 的 dp 宽高断点选形态；写错：按 Dimension_1_2 / Dimension_2_2 / Dimension_2_4 一档对一种形态写死映射（如 2*2→中、2*4→大），没有和源断点比
- rule-b0619c4df2c8｜卡片页用了不带 @form 的事件或组件（onAreaChange、Grid）时，改用带 @form 的写法｜读到：规格写卡片内用 onSizeChange / 宽度判断驱动条件渲染；写错：卡片页（form_config 的 src 指向的 .ets）上出现 .onAreaChange(...) 或 Grid(...)；编译报 `'onAreaChange' can't support form application`
- rule-75ffe5b4d9c9｜V1 卡片页的派生值写成 build 里调用的普通方法，不写 struct 的 get 访问器｜写错：卡片页的 @Entry / @Component struct 里写了 `get` 访问器，build 里不带括号地按属性读它
