# ui/interaction

点击、触外取消与按钮状态：抬起判定、selector与选中态

[上一级](../index.md)

## 本级经验

- [安卓点击与触外取消按抬起判定实现，不直接映射为onClick](lesson-8ec999dc451bf75c8373.lesson.md)
  - 时机：规格提取与界面实现阶段，把setOnClickListener按钮、遮罩点按和对话框触外取消映射为ArkUI事件时
  - 情境：源按钮用setOnClickListener（由View.onTouchEvent在抬起时判定），对话框依赖默认触外取消；目标准备用组件或遮罩的onClick。
  - 例外：产品明确接受按住超过约800ms不触发的差异
- [按钮selector按各自状态集合映射，setSelected态建成独立UI状态](lesson-c932cb8b23a56b4dc8e4.lesson.md)
  - 时机：界面实现与功能接线阶段，把按钮selector与setSelected/setEnabled调用点翻译成ArkUI图片状态，并接入恢复流程时
  - 情境：同屏多个按钮引用状态集合不同的selector（有的含state_pressed，有的只有selected/enabled）；源码只在少数方法里调用setSelected，onResume等恢复路径只回填业务字段；目标用状态变量直接计算图片资源。
