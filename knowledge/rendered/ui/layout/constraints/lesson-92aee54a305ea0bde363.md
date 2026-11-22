# Stack 中内容尺寸的子项按 alignContent 定位：子项自身的 .align() 不改变它在父容器中的位置，需要的对齐用满尺寸容器或显式 position

## 何时使用

界面转换与巡检修复阶段，把 Compose 自定义 Layout 或 Box 中的文字改写为 ArkUI Stack 子节点并确定纵向位置时；修复或编译清理删除 height('100%')、.align() 等居中手段时；把 FrameLayout 中按 layout_gravity 叠放的角标、重叠头像翻译成 Stack 时；把 Compose Box 中以 Modifier.align(BottomCenter 等) 定位的子项翻成 Stack 子节点时；把 FrameLayout/CoordinatorLayout 的 layout_gravity、RelativeLayout 的 alignParent*/centerInParent 翻译为 Stack 中 FAB、多选浮层、工具栏、装饰条的定位并确定叠层次序时；把 ConstraintLayout 标题栏（左返回、居中标题、右侧操作）转换为 ArkUI 或抽取公共标题栏组件时

## 适用情境

源端自定义 Layout 用 placeRelative(x, (maxHeight - height) / 2) 把定宽文字纵向居中，或 Box 中文字按居中对齐放置；目标用 Stack({ alignContent: Alignment.TopStart }) 同时容纳文字与图片等对齐需求不同的子项。也包括源端固定尺寸 FrameLayout 中的小角标以 layout_gravity=end|bottom 贴右下，目标写成 Stack({ alignContent: Alignment.TopStart }) 并只给角标加 .align(Alignment.BottomEnd)。也包括源 Box 中部分子项用 Modifier.align 放到非默认位置（如贴底的购买栏），目标 Stack 设了统一的 alignContent(TopStart)，规格写着“底部对齐”。也包括映射参考或兄弟页把 layout_gravity 写成 .align(Alignment.X)，工具栏、浮层、FAB 于是落在父 Stack 中部。也包括标题栏：返回图标约束到父 start、右侧入口约束到 end、标题 0dp 加左右 margin 居中，目标写成 Stack({ alignContent: Alignment.Center }) 并只给返回图标加 .align(Alignment.Start)，后写的页面与公共标题栏组件以它为模板复制。

## 原因

Stack 按 alignContent（或 Stack 自身的 align，二者后设置的生效）放置未撑满的子节点，子项设了 layoutGravity（API 20 起，只对 Stack 的直接子组件生效）时才按子项自己的对齐；Text 的 .align() 只对齐文字在自身框内的位置，内容高的 Text 在 TopStart 的 Stack 里仍落在左上角，ArkUI Alignment 也没有 Compose 的 CenterStart。来源中巡检修复者为裁剪图片把 Row 改成 TopStart 的 Stack，删去 Text 的满高后改写 .align(Alignment.CenterStart) 并自称已居中；编译修复把它改成 Alignment.Start，随后又被删除，分类卡文字一直贴左上。另一应用的成员头像角标照此写成子项 .align(BottomEnd)，角标仍在左上；该片段后来被抽进共享组件继续沿用，直到改成 position 才贴到右下。

## 做法

1. 同一 Stack 中各子项对齐需求不同时，给文字包一个满高容器：Column().width(源端比例).height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Start)，或给子项按源公式单独 position/offset。
2. 删除 height('100%')、.align() 等手段前，确认替代约束仍实现原来的纵向位置；枚举名以 ArkUI SDK 为准，不照搬 Compose 的 Alignment 名称。编译修复把 Compose 专有名（CenterEnd、CenterStart 等）换成 ArkUI 现有名（End、Start）时，若它挂在 Stack 子项的 .align() 上，换名后位置仍不变，同时改为 position 或父 Stack 的 alignContent。
3. 按 layout_gravity 单独对齐某个子项（如 end|bottom 的角标）时，在已知 W×H 的容器里写 position({ x: W - 子宽, y: H - 子高 })，或给该子项单独套一个 alignContent 为对应方向的 Stack。
4. 逐个核对源 Box 子项的 Modifier.align：非默认位置写成 position({ left: 0, bottom: 0 })、markAnchor 等实际属性；规格或报告里的“底部对齐”要落到代码属性上。
5. 子项单向贴边时可改父 Stack({ alignContent })；同一 Stack 内混合对齐用 .position({ left/right/top/bottom })、markAnchor 或满幅透明容器配 justifyContent/alignItems，并保留源 margin。
6. 叠层按源布局声明顺序复核 z 序（后声明者在上），无法按序排列时补 zIndex。
7. 标题栏按约束建互斥的水平槽位：Row 内左侧固定宽槽（宽取标题的 marginStart）放返回入口，layoutWeight(1) 的标题居中，右侧固定槽放操作入口；也可用 RelativeContainer + alignRules 对应 start/end 约束。

## 可选检查

- 沿用了映射参考或先例中的定位写法时，检索 .align(Alignment.，逐个确认它要的是内容对齐还是在父容器中的位置
- 标题栏同时打开返回与右侧入口并用较长标题预览，确认三者不重叠、标题在两侧槽位之间居中

来源支持：11 张卡 · 8 次迁移 · 7 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；安卓 Android SDK 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因；适用情境〕通用属性 align 设置的是组件自身绘制区域内子组件或内容的对齐方式，不改变该组件在父容器里的位置；它只在 Stack、FolderStack、Button、Text、TextInput、TextArea、ListItem、GridItem、Scroll 等文档列出的组件上生效，默认 Alignment.Center；在 Text 上只决定文本段落在 Text 自身框内的纵向位置（Top 系顶部、Start/Center/End 居中、Bottom 系底部），横向由 textAlign 决定。〔成立范围：对象：任意组件上的 .align()。条件：Text 高度大于文本内容时纵向对齐才看得出来，高度随内容的 Text 上设 align 没有可见效果。不成立：Column、Row、Image 等不在列表里的组件上 align 不生效；子项要在父 Stack 里单独定位得用 layoutGravity（API 20 起）、position/offset，或改父 Stack 的对齐。〕
- 〔做法第 3、4、5 步〕通用属性 layoutGravity(LocalizedAlignment) 单独设置一个 Stack 子组件在父 Stack 里的对齐，默认 LocalizedAlignment.CENTER；文档写明它与 align 同时使用时 layoutGravity 优先，LocalizedAlignment 的 START/END 随 direction 或系统语言方向镜像。〔成立范围：对象：父组件是 Stack 的组件（Stack 的直接子组件）。条件：API 20 起，仅 Stage 模型；传异常值按 CENTER 处理。不成立：父组件是 Column、Row、RelativeContainer 等其他容器，或加在 Stack 子项内部更深一层的组件上，都不生效；应用兼容的最低 API 低于 20 时只能用 position 或嵌套 Stack。〕
- 〔做法第 5 步；适用情境〕Stack 不设对齐时子组件按 Alignment.Center 居中；对齐可以由构造参数 alignContent、alignContent 属性或通用属性 align 给出，属性与构造参数同时设以属性为准，alignContent 属性与 align 同时设以后设置的为准；Android FrameLayout 子项没写 layout_gravity 时则按 TOP|START 贴左上。〔成立范围：对象：Stack 容器及其未撑满的子组件。条件：Stack 上的 align 支持镜像（Start/End 随 RTL 互换），其他组件上的 align 不支持镜像（依据是文档说明）；align 改传 LocalizedAlignment（API 20 起的重载）时，文档列出的生效组件里没有 Stack。不成立：子组件自己设了 layoutGravity（API 20 起）或 position 时不按 Stack 的对齐摆放。〕
- 〔适用情境（layout_gravity 映射）〕Android FrameLayout 子项的 layout_gravity 只写一个方向时，另一个方向取顶边或左边（LTR 下 end 落在右上，bottom 落在左下）；ArkUI Alignment 的单向值 Start、End 是纵向居中，Top、Bottom 是横向居中，所以 layout_gravity=end 对应 TopEnd 而不是 End。〔成立范围：对象：FrameLayout 的直接子 View 与 ArkUI Alignment 枚举。条件：FrameLayout.layoutChildren 中缺省轴走 default 分支（横向取 parentLeft、纵向取 parentTop）；缺省的横向取的是绝对左边，RTL 下也不换边，只写 bottom 时 RTL 仍贴左下。不成立：gravity 里写了 center、center_vertical 或 center_horizontal 的那一轴按居中。〕
- 〔做法第 3、4 步〕position 以父组件内容区（父组件尺寸减去 border、padding、safeAreaPadding）为基准：Position{x,y} 相对内容区左上角，Edges{left/top/right/bottom} 按到内容区各边的距离，只有 LocalizedEdges{start/end} 随 RTL 镜像；position 在尺寸测量完成后生效，与 offset 同时设时 offset 不生效，markAnchor 再从 position 结果里减去锚点坐标。〔成立范围：对象：任意组件的通用属性 position。条件：父组件是 Row、Column、Flex 时设了 position 的子组件不占位。不成立：父组件是 RelativeContainer 且子组件设了 alignRules 时 position 不生效；父组件没设固定宽高时，按第一个设了固定宽高的祖先组件定位（依据是文档说明）。〕
- 〔做法第 6 步〕Stack 的子组件按声明顺序入栈，后声明的盖在先声明的上面；zIndex 只调整同一父容器内兄弟组件之间的层级，默认 0，值大的在上。〔成立范围：对象：同一父容器下的兄弟组件。条件：兄弟节点不增减时动态改 zIndex 会在原顺序上稳定排序。不成立：分属不同 Stack 的组件之间，zIndex 再大也不能跨容器盖到对方上面。〕
