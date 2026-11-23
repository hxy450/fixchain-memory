# sharedBounds 包住 sharedElement 的两层共享转场，每端只挂一个 geometryTransition（外层容器），不逐层各配一对

## 何时使用

界面实现与规格提取阶段，把 Compose SharedTransitionLayout 内 sharedBounds 包住 sharedElement、两层 key 不同的共享转场落为 ArkUI geometryTransition，确定每端挂几个配对键、挂在哪个节点时

## 适用情境

源端在 SharedTransitionLayout 内用 sharedBounds("${id}-bounds") 包住带 sharedElement(id) 的内容，两层 key 不同，列表卡与同页详情浮层两端各有这两层；目标用同页条件浮层加 geometryTransition 做展开和收起，规格页面结构一节可能把源端两层 key 原样列出。

## 原因

同一配对子树里嵌套两对 geometryTransition 时，过渡后配对节点的子树会丢失：设备控件树里浮层卡与收起后的列表卡都成了没有子节点的空节点。外层一对已经承担形变，内层内容随容器一起过渡即可。

## 做法

1. 同一配对子树只挂一个 geometryTransition 承担形变，挂在外层容器上（对应外层 sharedBounds 的节点与键），内层不再挂第二个；规格写“geometryTransition(id) 双端绑定”时按每端一对理解。
2. 后写的一端与已写好的一端配对时，核对对方的键，也核对对方有没有嵌套第二个 geometryTransition；发现嵌套就在 handback 里报告，不照样镜像。规格写共享转场契约时写明每端只挂一对、用哪个键、挂在哪个节点，不把源端两层 key 写成“两对”。

## 可选检查

- 两端写完后在设备上打开并关闭一次，用控件树确认浮层与收起后的列表项都还有子节点，不只看截图里有没有动画。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕geometryTransition 必须配合 animateTo 才有动画；同一个 id 只能有两个组件绑定，分别作 in（新视图）与 out（旧视图）角色；绑定同一 id 的组件不能相互嵌套，否则转场动画异常
- 〔原因〕同一配对子树里嵌套两对不同 id 的 geometryTransition 时，展开再收起之后，设备控件树里浮层卡与收起后的列表卡都成了没有子节点的空节点
