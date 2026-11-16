# 固定宽高的可点 ImageView 迁成同尺寸的点击容器，不缩成图标本身大小

审的是：代码
触发（任一种）：
- 读到：源布局里返回键等 ImageView 写了固定的 android:layout_width / android:layout_height（dp）加 paddingVertical，图标画在这个点击区里；写错的样子：鸿蒙端只按图标尺寸写 Image(...) 的 .width / .height 加上下 padding，没有和源端同宽高的点击容器
适用范围：UI 转换阶段迁移带固定尺寸点击区的图标按钮（返回键等）时
做法：
- 按源端尺寸建点击容器：外层写 .width(<layout_width 的 dp 数>).height(<layout_height 的 dp 数>) 并挂 onClick，图标放在里面，源端 padding 照搬
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 返回键按源端 dp 宽高建同尺寸点击区：修复后返回热区与源端一样大（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-436d1b16d79796c667d6（android-panorama-map-vest7）：做法第 1 步 ← 建议 4、诊断；取值 1 ← 诊断
