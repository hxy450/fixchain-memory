# Stack 中内容尺寸的子项按 alignContent 定位：子项自身的 .align() 不改变它在父容器中的位置，需要的对齐用满尺寸容器或显式 position

## 何时使用

界面转换与巡检修复阶段，把 Compose 自定义 Layout 或 Box 中的文字改写为 ArkUI Stack 子节点并确定纵向位置时；修复或编译清理删除 height('100%')、.align() 等居中手段时；把 FrameLayout 中按 layout_gravity 叠放的角标、重叠头像翻译成 Stack 时；把 Compose Box 中以 Modifier.align(BottomCenter 等) 定位的子项翻成 Stack 子节点时；把 FrameLayout/CoordinatorLayout 的 layout_gravity、RelativeLayout 的 alignParent*/centerInParent 翻译为 Stack 中 FAB、多选浮层、工具栏、装饰条的定位并确定叠层次序时；把 ConstraintLayout 标题栏（左返回、居中标题、右侧操作）转换为 ArkUI 或抽取公共标题栏组件时

## 适用情境

源端自定义 Layout 用 placeRelative(x, (maxHeight - height) / 2) 把定宽文字纵向居中，或 Box 中文字按居中对齐放置；目标用 Stack({ alignContent: Alignment.TopStart }) 同时容纳文字与图片等对齐需求不同的子项。也包括源端固定尺寸 FrameLayout 中的小角标以 layout_gravity=end|bottom 贴右下，目标写成 Stack({ alignContent: Alignment.TopStart }) 并只给角标加 .align(Alignment.BottomEnd)。也包括源 Box 中部分子项用 Modifier.align 放到非默认位置（如贴底的购买栏），目标 Stack 设了统一的 alignContent(TopStart)，规格写着“底部对齐”。也包括映射参考或兄弟页把 layout_gravity 写成 .align(Alignment.X)，工具栏、浮层、FAB 于是落在父 Stack 中部。也包括标题栏：返回图标约束到父 start、右侧入口约束到 end、标题 0dp 加左右 margin 居中，目标写成 Stack({ alignContent: Alignment.Center }) 并只给返回图标加 .align(Alignment.Start)，后写的页面与公共标题栏组件以它为模板复制。下面两种写法位置本身是对的，不在本条改动范围：子项已用 layoutGravity（API 20 起，父组件为 Stack 时生效）单独对齐；子项撑满父 Stack（宽高 100%），.align() 只用来摆放它自己的内容。

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

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 源码 android-36.1。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1、2 步〕通用属性 align 设置组件内容在自身绘制区域内的对齐方式，默认 Alignment.Center；在 Stack 上它与 alignContent 效果一致，只设置子组件在当前组件内的对齐，写在 Stack 的子项上不移动子项本身
- 〔原因 / 做法第 5 步〕Stack 的 alignContent 默认 Alignment.Center，非法值按默认处理；alignContent 与 align 同时设置时后设置的生效；构造参数与 alignContent 属性同时设置时以属性为准，与顺序无关
- 〔原因〕layoutGravity（API 20 起）单独设置 Stack 中某个子组件的对齐，只在父组件为 Stack 时生效；与 align 同时使用时 layoutGravity 优先
- 〔原因 / 做法第 2 步〕Text 上的 align 控制文字在 Text 框内的纵向位置，Alignment.Start、Center、End 效果相同；水平对齐由 textAlign 决定，默认 TextAlign.Start
- 〔做法第 1、3、4、5 步〕position 确定子组件相对父组件内容区（父组件大小减去 border、padding、safeAreaPadding）的位置，Edges 写法（top、left、bottom、right）自 API 12 起；父组件为 Row、Column、Flex 时设了 position 的子组件不占位，全部子组件都设 position 时父组件按 (0, 0) 测算
- 〔做法第 1 步〕offset 让组件基于原本的布局位置偏移，只在绘制时调整，不影响父组件布局
- 〔做法第 6 步〕Stack 容器中的子元素依次入栈，后一个子元素覆盖前一个
- 〔做法第 6 步〕同一容器内兄弟组件按 zIndex 分层，值越大显示层级越高
- 〔做法第 1 步〕Column 的 justifyContent 默认 FlexAlign.Start；子组件不设 flexShrink 时默认不压缩，子组件主轴尺寸累加超过容器时 FlexAlign.Center、FlexAlign.End 失效
- 〔做法第 7 步〕alignRules 只在父容器是 RelativeContainer 时生效
- 〔适用情境 / 做法第 3、5 步〕安卓 FrameLayout 子项不写 layout_gravity 时按 DEFAULT_CHILD_GRAVITY = Gravity.TOP | Gravity.START 摆放（贴左上，RTL 下贴右上）；鸿蒙 Stack 不设对齐时居中，两端默认不同
- 〔适用情境 / 做法第 5 步〕RelativeLayout 中横向没有任何定位规则的子 View 放在起始边（LTR 下左边），纵向同理放在顶边，几个这样的子 View 叠在同一坐标
- 〔做法第 5 步〕RelativeLayout 设了 gravity（非 start、top）时，onMeasure 末尾把可见子项（ignoreGravity 指定的那个除外）作为一组按 gravity 平移
- 〔原因〕根 Stack 用默认居中、只在子项上写 .align(Alignment.Top) 或 .align(Alignment.Bottom) 时，设备上这些子项仍落在 Stack 中部
