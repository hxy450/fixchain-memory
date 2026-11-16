# 控件经 style 继承圆角、元素没覆写时，borderRadius 取样式里的值，不按半高或邻近控件推

审的是：代码
触发（任一种）：
- 读到：布局 XML 里控件写 `style="@style/…"`，圆角、高度等形状值写在样式的 `<item>` 里，元素本身没有写圆角覆写；写错的样子：对应组件的 `.borderRadius(...)` 用了外层卡片、相邻按钮或别处显式覆写的值，或按高度一半写成胶囊；注释里写不出圆角来自样式还是哪一处覆写
- 读到：同一个 `style="@style/…"` 在多个布局复用，其中有的元素显式覆写了圆角；写错的样子：把某处的覆写值当成样式默认值，写进没覆写元素的 `.borderRadius(...)`，或把有覆写的元素改回样式值
适用范围：把引用了 style 的安卓控件（含返修时重写的弹窗、按钮）迁成 ArkUI 组件并定圆角等形状值时
做法：
- 先展开样式的全部 item（圆角、高度、渐变起止色），再逐项叠加元素上的显式属性；元素没覆写的形状值一律取样式值，写成 `.borderRadius(样式里的圆角)`
- 按控件逐个核对有没有显式覆写：有覆写的照覆写值（如胶囊按钮保持胶囊），没覆写的取样式值；不按高度一半、不照搬外层卡片或相邻按钮的圆角
- 在 borderRadius 旁的注释里写明值来自哪个样式还是哪一处 XML 覆写；写不出来源、只是估算的，先去读样式定义再写
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 属性取值的先后：元素上的属性 > style 属性指定的样式 > defStyleAttr/defStyleRes 默认样式 > 主题的基础值：元素没写的属性才取样式值，元素写了的覆写样式（出处：android.content.res.Resources.Theme#obtainStyledAttributes）
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses): T：组件圆角；半径受组件尺寸限制，最大为宽或高的一半，所以写到半高就成了胶囊（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
- borderRadius(value: Length | BorderRadiuses | LocalizedBorderRadiuses, type?: RenderStrategy): T：同族接口：带圆角绘制策略的重载，@since 22（出自声明）（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.borderRadius）
针对本应用要查的：
- 控件引用的样式里的圆角、高度等形状值：源工程 res/values 下的样式 XML 里 `<style name="…">` 这一项，没写的项沿 `parent` 往上找；读 `<item name="…">` 的取值；再看布局 XML 里这个元素自己有没有写同名属性，写了就以元素的为准
未核实：卡里的界面行为出自 HarmonyOS 6.1.1(24)，核对声明用的是本机 API 23
来源：1 张卡，1 个应用
- case-4a9e750abf5d6293ab33（免费来电多多）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 2、建议 3；做法第 3 步 ← 建议 2、建议 4
