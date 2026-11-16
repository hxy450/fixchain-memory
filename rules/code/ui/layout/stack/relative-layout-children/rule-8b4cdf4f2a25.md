# SeekBarPreference 行按源 RelativeLayout 让数值和滑条同起于标题下方叠放，不拆成两行

审的是：代码
触发（任一种）：
- 读到：SeekBarPreference 的行布局 XML 是 RelativeLayout，数值 TextView 和 SeekBar 都 layout_below 标题、互相重叠；写错的样子：数值 Text 单独占一行，下面再放一个 Slider
适用范围：源端 SeekBarPreference 的行布局里数值和 SeekBar 都位于标题下方并重叠时
做法：
- 标题下面放一个叠放容器（Stack），数值 Text 和 Slider 都放进去，按源 RelativeLayout 的对齐叠在一起，不拆成上下两行
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 返修把滑条行改成数值与滑条重叠后与源端一致：按源布局叠放（出处：卡里修好并验证过）
针对本应用要查的：
- 数值和滑条的相对位置：源工程 res/layout 里 SeekBarPreference 用的行布局 XML；看 RelativeLayout 里两者的 layout_below、layout_align* 和 margin，照着在叠放容器里对齐
未核实：卡里没写返修用的具体容器，用 Stack 叠放是按做法推的写法
来源：1 张卡，1 个应用
- case-a8bb009f2c5e1b854f32（Blockinger）：做法第 1 步 ← 建议 2、诊断；取值 1 ← 诊断
