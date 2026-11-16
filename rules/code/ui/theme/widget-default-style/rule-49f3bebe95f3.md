# TabLayout 不写 tabGravity/tabMode/style 时，横屏和宽屏按库默认居中，不一律均分

审的是：代码
触发（任一种）：
- 读到：源布局的 com.google.android.material.tabs.TabLayout 没写 app:tabGravity、app:tabMode、style，主题是 AppCompat 一族（几何取 Widget.Design.TabLayout）；写错的样子：Tabs 用默认 BarMode.Fixed 加 .barWidth('100%')，横屏和宽屏也均分整行；或判定「页面外壳与方向无关」
适用范围：源 TabLayout 几何全部来自库默认样式、迁成 ArkUI Tabs 时；主题不是 AppCompat 一族时按 lookups 另查默认样式
做法：
- 竖屏且最小宽 < 600vp 时各 Tab 均分整行（BarMode.Fixed）；横屏或最小宽 ≥ 600vp 时各 Tab 取最宽 Tab 的宽（文字 + 左右各 12vp）整体居中，总宽超过可用宽 − 2×16vp 时退回均分
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Widget.Design.TabLayout：tabGravity=fill、tabMode=fixed：竖屏默认均分（出处：com.google.android.material:material 包内 res/values/values.xml，Widget.Design.TabLayout（按应用依赖的版本））
- values-land 下 Widget.Design.TabLayout：tabGravity=center、tabMode=fixed：横屏默认居中（出处：com.google.android.material:material 包内 res/values-land/values-land.xml，Widget.Design.TabLayout（按应用依赖的版本））
- values-sw600dp-v13 下 Widget.Design.TabLayout：tabGravity=center、tabMode=fixed：最小宽 ≥ 600dp 时默认居中（出处：com.google.android.material:material 包内 res/values-sw600dp-v13/values-sw600dp-v13.xml，Widget.Design.TabLayout（按应用依赖的版本））
- tabPaddingStart = 12dp、tabPaddingEnd = 12dp：每个 Tab 文字左右的内边距（出处：com.google.android.material:material 包内 res/values/values.xml，Base.Widget.Design.TabLayout（按应用依赖的版本））
- BarMode.Fixed = 1：each tab width = bar width ÷ tab 数：ArkUI Tabs 默认 Fixed 只等价竖屏的 fill（出处：鸿蒙 SDK 的 ets/component/tabs.d.ts，BarMode.Fixed）
- 竖屏且最小宽 < 600 均分，否则取最宽 Tab 居中（手算 tab 宽和起点）：修复后的写法（出处：卡里修好并验证过）
针对本应用要查的：
- TabLayout 实际用的默认样式：源工程 AndroidManifest 的 android:theme 所指主题及其父主题里的 tabStyle；没有 tabStyle 时是 Material 库的 Widget.Design.TabLayout；到应用依赖版本的 com.google.android.material:material 包内 res/values*/ 下，读这个样式在 values、values-land、values-sw600dp-v13 里的 tabGravity、tabMode
未核实：Material 库样式按 material 1.12.0 核实，应用依赖别的版本时按 lookups 重查
来源：1 张卡，1 个应用
- case-b0d293fe50601628c722（Privacy Friendly 2048）：做法第 1 步 ← 建议 3、诊断；取值 6 ← 诊断
