# dp 尺寸在目标端的单位

agent 会看到什么：读到源端以 dp 给出的尺寸（布局 XML 的 1dp、vector drawable 的 android:width / height）或在 dp 列宽内折行的 TextView；产物里写成 'px' 字符串、按密度除过的数，或对本按 vp 解析的宽度又做了 vp2px

## 通用查法

### 源端 dp 尺寸迁到 ArkUI 时，按目标参数写明的单位写：number 即 vp，写明 px 的才换算

审的是：代码
触发（任一种）：
- 读到：源端尺寸以 dp / dip 给出（布局 XML 的 android:layout_height="1dp"、@dimen/ 引用、vector 根元素的 android:width），或按 dp 列宽排版；写错的样子：目标写成 'Npx' 字符串、把 dp 数除以密度，或对本按 vp 解析的参数（如 measureTextSize 的 constraintWidth）又包了 vp2px
适用范围：把安卓以 dp 给出的尺寸写成 ArkUI 长度，或传给带单位约定的测量、绘制接口时
做法：
- 先查源端值的单位：后缀是 dp / dip 的照数值写成 number（vp），源端明确写 px 时才写 'Npx'
- 再查目标参数和返回值的单位：声明注释或文档写 px 的才在两边做 vp2px / px2vp；写 vp 或按 Length 解析的 number 直接传 vp 数，不按密度乘除
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- Length 为 number 时默认单位 vp；string 要显式写像素单位，不写单位也按 vp：直接写数字即 vp（出处：ts-types.md，Length）
- px 是屏幕物理像素单位；vp 按屏幕像素密度换算成物理像素：把 dp 数写成 'Npx' 在高密度屏上会小几倍（出处：ts-pixel-units.md，像素单位）
- measureTextSize(options: MeasureOptions): SizeOptions，返回的宽和高都是 px：例：返回值写明 px，和 vp 常量比较前要 px2vp（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureTextSize）
- MeasureOptions.constraintWidth 默认单位为 vp，不支持百分比字符串：例：参数按 vp 解析，传 vp 列宽本身（出处：js-apis-measure.md，MeasureOptions）
针对本应用要查的：
- 源端尺寸的单位和数值：源工程布局 XML 的属性值后缀（dp、dip、px）、@dimen/ 引用到的 values*/dimens.xml，vector drawable 根元素 <vector> 的 android:width / android:height；顺着 @dimen/ 读到最终的数和后缀；dp / dip 的数就是目标端的 vp 数
- 目标参数和返回值的单位：鸿蒙 SDK 声明里这个接口、参数或返回值的注释（找 unit、px、vp 字样），声明没写的查文档里这个接口的小节；写 px 的才换算；写 vp 或按 Length 解析的 number 直接用 vp 数
来源：3 张卡，2 个应用
- case-d54a9506e30031090325（Jetsnack）：做法第 2 步 ← 建议 7
- case-deff0a401e40f1faa419（Privacy Friendly 2048）：做法第 2 步 ← 建议 1
- case-fe1caa813d814978decf（Privacy Friendly 2048）：做法第 1 步 ← 建议 7

## 规矩

- rule-441144e11f9f｜安卓 dp 尺寸写成 ArkUI 数字（vp），不写 'px' 字符串；1dp 细线也按 1vp｜读到：源端尺寸以 dp 给出（如 `list_divider_material` 的 `android:height="1dp"`）；写错：ArkUI 写成 `'1px'` 这类 px 字符串（物理像素）
- rule-4b2c6fe10a1a｜Image 用 vector drawable 不设尺寸时，目标按 vector 的 dp 尺寸写，不再除以密度｜读到：Compose `Image(painterResource(...))` 不设尺寸，资源是 vector drawable，`android:width`/`android:height` 写的是 dp，放在无密度限定的 drawable 目录；写错：目标 `Image` 只写 `objectFit` 没有尺寸，或宽高写成 vector 的 dp 数除以 3（自动修复按回退密度当像素换算）
- rule-60e9e39496c5｜measureTextSize 按列宽测折行时 constraintWidth 直接传 vp 宽，不先 vp2px｜读到：源端 TextView 为 android:layout_height="wrap_content"，文字在列宽内折行后自身变高并把后续视图下推；写错：目标端 getMeasureUtils().measureTextSize({ …, constraintWidth: ui.vp2px(width) })，width 本是 vp 列宽
