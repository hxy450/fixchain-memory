# 源方法按选择对象分图片、单色、渐变几支时，目标绑定逐支实现，不只迁 url 分支

审的是：代码
触发（任一种）：
- 读到：源方法按一个选择对象分支：url 非空加载图片；否则 colors.size == 1 生成 ColorDrawable，colors.size == 2 按 orientation 生成 GradientDrawable；写错的样子：目标绑定只读选择对象的 `url` 字段设图片源，没有任何 `colors` / `orientation` 处理；`url` 为空时不清图片
适用范围：迁移以一个选择对象同时表达图片、单色、渐变（或为空恢复默认）的源方法，绑定到目标渲染属性时
做法：
- 先把源方法的每个分支列成清单（url 图片 / 单色 / 双色渐变 / 为空恢复默认），逐项落到目标绑定，做不了的明确标注未实现
- url 为空且 colors 非空时清掉运行时图片；colors 映射为背景的填充色（一个为纯色、两个为渐变色），orientation 映射为渐变角度
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- url 为空且 colors 非空时清空运行时图片，colors → 填充色、orientation → 角度，预览区变色：修好的写法（出处：卡里修好并验证过）
- GradientDrawable(Orientation orientation, int[] colors)；Orientation 取 TOP_BOTTOM、TR_BL、RIGHT_LEFT、BR_TL、BOTTOM_TOP、BL_TR、LEFT_RIGHT、TL_BR：源端渐变分支的构造和八个方向（如 TL_BR 是左上到右下）（出处：android.graphics.drawable.GradientDrawable#GradientDrawable(Orientation, int[])；android.graphics.drawable.GradientDrawable.Orientation）
针对本应用要查的：
- orientation 数值（45 / 90 / 135 …）到渐变方向的对应：源工程里构造 GradientDrawable 的那个方法（按 orientation 分支选 Orientation 枚举的地方）；逐个记下数值对应的 Orientation，再换算成目标渲染属性的角度定义
来源：1 张卡，1 个应用
- case-1cd334ad60ab3aef8cfa（组件岛Widget Island）：做法第 1 步 ← 建议 1；做法第 2 步 ← 诊断；取值 1 ← 诊断
