# values-vNN 下另有同名定义的应用主题

agent 会看到什么：读到 manifest 的 android:theme 指向的应用主题在 res/values/ 和 values-v21 等 values-vNN 下各有一份同名 <style>（values/ 继承 Theme.Light、values-v21 继承 Theme.Material.*）；规格的主题行、ActionBar 行、按压反馈按 values/ 的父主题写

## 通用查法

### 规格写由应用主题决定的项前，先按 API 级解析 values-vNN 覆盖后的生效主题链

审的是：规格
触发（任一种）：
- 读到：android:theme 指向的应用主题在 res/values/ 和 values-v21 等 values-vNN 下各有一份同名 <style>；写错的样子：规格按 values/ 的父主题（如 Theme.Light）写主题行和外观，没写覆盖后的生效链和从它读出的值
适用范围：规格里写主题行和由主题提供的标题栏、控件外观时
做法：
- 按 android:theme 名在 res/values/ 和各 values-vNN/ 的 styles.xml、themes.xml 找同名 <style>，取不高于参照 API 级（不低于 minSdk）的最高 vNN 那份的 parent，顺链到平台主题，各层覆写的 item 一并记下
- 由主题决定的项按属性名（colorPrimary、actionBarItemBackground 等）在这条链上取离应用主题最近的定义，写出提供方和解析值
- 主题行写成「API 21+：应用主题 → 父主题 → 平台主题（values-v21）」，values/ 的父主题只作低版本回落
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- <style name="Theme.Material.Light" parent="Theme.Light">：Material.Light 在 Theme.Light 之上重新定义状态栏、窗口底色和 ActionBar，停在 Theme.Light 会漏掉这些项（出处：Android SDK 平台资源 data/res/values/themes_material.xml，Theme.Material.Light（按应用的 compileSdk 取对应平台））
针对本应用要查的：
- 参照设备 API 级下应用主题的生效父主题链：源工程 res/values/ 和各 res/values-vNN/ 下的 styles.xml、themes.xml，按 manifest android:theme 的名字找同名 `<style>`；取不高于参照 API 级的最高 vNN 那份的 parent，再顺着 parent 往上到平台主题；各份覆写的 item 也一并记下
- 生效主题给某一项外观的值：先看应用主题各层覆写的 item，再看 Android SDK 平台资源 data/res/values/themes_material.xml、styles_material.xml（按应用的 compileSdk 取对应平台），按属性名找；取生效链上离应用主题最近的那个定义；值是 ?attr/colorPrimary 这类主题属性的，再回到生效链上读出它的颜色值
来源：3 张卡，1 个应用
- case-1a1c2ec5cf0140821002（Sokoban）：做法第 1 步 ← 建议 1；做法第 3 步 ← 建议 1
- case-3d6b5f99f326a3e5e8e9（Sokoban）：做法第 2 步 ← 建议 3
- case-b76baecf687e5ab5817a（Sokoban）：做法第 2 步 ← 建议 6

## 规矩

- rule-463715377642｜应用主题在 values-vNN 下另有同名定义时，规格的主题行按 API 级写覆盖后的生效链｜读到：manifest 的 android:theme 指向的应用主题在 values/ 和 values-v21 等 values-vNN 下各有一份同名 `<style>`；values/styles.xml 的注释写着 replaced by … from res/values-vXX/styles.xml on newer devices；写错：规格（ui-manifest）的主题行写成 values/ 里的父主题，如「主题 extends android:Theme.Light」，没提 values-vNN 的覆盖；页面元数据 style_sources 列了 values-v21 却没反映到主题行
- rule-bb2e0a47496d｜规格的 ActionBar 行写明主题提供方、解析出的栏底色和标题色，以及应接的共享标题栏｜读到：源 Activity 主题（含 values-vXX 覆盖）继承带窗口 ActionBar 的框架主题，如 android:Theme.Material.Light.DarkActionBar，colorPrimary 指向应用色；计划列了共享顶栏组件；写错：规格的 ActionBar 行只写「标题 + Up 尖角」，安全区写「常规 NavDestination 标题栏」，主题只按 values/styles.xml 写成 Theme.Light，没写栏底色、标题色和应接的共享标题栏组件
- rule-e2052d992296｜规格写按压反馈时，按 values-v21 实际父主题写出提供方 drawable、类型和半径｜读到：源主题在 values/ 继承 Theme.Light、在 values-v21 继承 android:Theme.Material.Light.DarkActionBar 等；列表 listSelector、标题栏按钮背景都来自主题；写错：规格只写「按压色取平台资源」「stateStyles pressed 底色层」，按 values/ 的 Theme.Light 写，没写 drawable 是 ripple 还是 selector、有界无界和半径
