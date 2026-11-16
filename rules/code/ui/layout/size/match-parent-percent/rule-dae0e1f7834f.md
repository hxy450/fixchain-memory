# match_parent 加水平 margin 时用 calc 宽度或父级 padding，不写 100% 宽

审的是：代码
触发（任一种）：
- 读到：android:layout_width="match_parent"（或 0dp 两端约束到 parent）加 layout_marginHorizontal / marginStart/End / marginLeft/Right / layout_margin；写错的样子：同一链里 .width('100%') 又有水平 .margin({ left/right/start/end … }) 或 .margin(N) 简写
- 读到：wrap_content 加 android:minWidth、实际占满可用宽，带 layout_marginLeft/Right；写错的样子：.width('100%') 另加 .margin({ left, right })
适用范围：安卓子视图占满父宽又带水平外边距，迁成 ArkUI 容器的子组件时
做法：
- .width('calc(100% - Nvp)')，N = 源两侧水平 margin 之和（marginHorizontal=16dp → calc(100% - 32vp)），运算符两侧留空格；竖直 margin 照写，左右 margin 照源保留或去掉
- 或把水平间距下沉到父容器（或包装 Row/Column）的 .padding({ left, right })，子组件只写 .width('100%') 和竖直 margin，加大边距改 padding 数值；有要贴边的兄弟项时用包装容器或 .layoutWeight(1)
- 写完逐处查同一链里 .width('100%') 与水平 .margin(...) 并存的组合，同页按钮、卡片、列表行一起改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在 Row、Column、Flex 交叉轴上布局时，子组件交叉轴的大小与 margin 的和为整体：width('100%') 已等于父宽，再加水平 margin 就超出父容器（出处：ts-universal-attributes-size.md，margin）
- 百分比尺寸参考最近设置了固定大小的祖先节点的尺寸：'100%' 不会自动扣掉自身 margin（出处：ts-universal-attributes-size.md，尺寸设置）
- width(value: Length): T；组件宽大于父容器宽时绘制超出父容器；API 10 起支持 calc，运算符与数值之间要用空格隔开，如 'calc(50% + 50vp)'：calc(100% - 32vp) 这种写法可直接传给 width（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.width；ts-universal-attributes-size.md，width、尺寸设置）
- padding(value: Padding | Length | LocalizedPadding): T，默认 0：父容器或包装容器上写水平内边距（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.padding）
- layoutWeight(value: number | string): T：在 Row/Column/Flex 主轴上按权重分剩余空间，分配时忽略元素本身的尺寸设置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.layoutWeight；ts-universal-attributes-size.md，layoutWeight）
- measureChildWithMargins 用 mPaddingLeft + mPaddingRight + lp.leftMargin + lp.rightMargin 扣掉已用宽度再算子视图的 MeasureSpec：源端 match_parent 的宽是父内容区减去两侧 margin（出处：android.view.ViewGroup#measureChildWithMargins）
- 并写 '100%' 与水平 margin 时组件右缘超出父宽，超出量为两侧 margin 之和；改成 calc(100% - Nvp)（有的页面只留 top margin），或把边距移到外层 padding 后不再越界：修好的写法（出处：卡里修好并验证过）
未核实：改成 calc 之后左右 margin 保不保留，卡与卡写法不同（case-6a2ee155bd552b418d50 的候选写成再加左右 margin，case-be590c45de6e4195a7aa 只留 top margin），各自页面都修好了，卡里没有比较；case-28bedbfdb77e8d050b15 的修复出自 API 24（6.1.1），本机声明是 API 23
来源：5 张卡，5 个应用
- case-28bedbfdb77e8d050b15（免费来电多多）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、建议 3、诊断；做法第 3 步 ← 建议 2；取值 7 ← 诊断
- case-6a2ee155bd552b418d50（骑行记录）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 7 ← 诊断
- case-be590c45de6e4195a7aa（实时公交）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3；取值 7 ← 诊断
- case-c42ad6674b3abc0daece（AntennaPod）：做法第 1 步 ← 建议 1、诊断；做法第 2 步 ← 建议 1；做法第 3 步 ← 建议 2；取值 7 ← 诊断
- case-cdc57384e71fa7c70345（组件岛Widget Island）：做法第 1 步 ← 建议 3、诊断；做法第 2 步 ← 建议 3；做法第 3 步 ← 建议 3；取值 7 ← 诊断
