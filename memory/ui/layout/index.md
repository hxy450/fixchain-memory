# ui/layout

布局与尺寸约束：Stack子项定位、自测尺寸视图、wrap_content宿主、match_parent与margin

[上一级](../index.md)

## 本级经验

- [FrameLayout子项的layout_gravity写到Stack直接子项的layoutGravity，不用align](lesson-6aa3acaf04e684c6328f.lesson.md)
  - 时机：界面实现阶段，把FrameLayout子项的layout_gravity转写为ArkUI Stack子项定位时
  - 情境：源FrameLayout内多个子项各带不同layout_gravity（左/中/右、上/下及组合），目标用Stack承载；手头映射参考可能把它写成.align()或.alignSelf()。
- [match_parent加左右margin的控件在ArkUI中写成calc宽度](lesson-5514ee45df1128bb3f27.lesson.md)
  - 时机：界面实现阶段，把带左右margin的match_parent控件转成ArkUI宽度时
  - 情境：源控件layout_width=match_parent并设左右margin，目标为Text、Divider等组件。
- [子页处在wrap_content宿主容器中时，按内容收拢match_parent栏与权重](lesson-5e78a803ed72ab47f845.lesson.md)
  - 时机：规格提取与界面实现阶段，为被Fragment或布局槽位承载的子页确定栏宽、权重和整体对齐时
  - 情境：宿主container为wrap_content（常配一个weight=1的Space留白），子页根为match_parent，内含match_parent的顶栏/底栏或带layout_weight的横屏列。
- [源视图在onMeasure中改写自身尺寸时，目标组件外框测成同一结果](lesson-c4d84310254b6c301960.lesson.md)
  - 时机：界面实现阶段，迁移在onMeasure中自定尺寸的自定义View，并决定它在线性布局中的尺寸时
  - 情境：源自定义View以wrap_content放置，在onMeasure中按可用宽高计算并setMeasuredDimension（如取min(宽,高)取整成正方形），兄弟控件紧随其后；目标用自定义组件包Canvas实现。
