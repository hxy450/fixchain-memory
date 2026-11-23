# 播放器面等运行时 addView 挂到根部的层，按运行时层级实现，不按 XML 里的占位区域定几何

## 何时使用

界面实现阶段，转换含运行时挂载子视图（播放器面等）的列表项或页面、确定视频层与浮层关系时

## 适用情境

源 Fragment/Adapter 在播放时通过 addView/LayoutParams 把视图挂到根容器（如 addView(videoView, 0) 无约束铺满），XML 里同名区域只是封面或控制视图；目标用 Stack/Column 重建层级。

## 例外与边界

- 放到最底层只对插在子视图列表开头（addView(view, 0)）的情形成立；不带 index 或 index 靠后的 addView 把视图画在已有子项之上，按插入位置放到 Stack 的对应层；addView 带了有尺寸或约束的 LayoutParams 时按那份参数定几何，不一律铺满。

## 原因

只看 XML 会把封面/控制区当成视频区，把视频夹在标题行与按钮行之间；运行时视频其实铺满、标题与按钮浮在其上。来源中写者读到了 addView 调用，仍按 XML 区域写，视频区结构性偏小、标题错位。

## 做法

1. 先在 Fragment/Adapter 中查 addView/removeView/LayoutParams，确认运行时视图挂在哪一层、有无约束，再定层级：无约束挂到根部的，放在根 Stack 最底层铺满；XML 占位区只保留封面与播放态显隐。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 1 步〕ViewGroup.addView 时，应用没有给子 View 另设 LayoutParams 的，用该 ViewGroup 的默认参数；index 是插入子 View 列表的位置，子 View 都没有 Z 值、也没开自定义绘制顺序时按列表顺序绘制，index 0 最先画、在最底层
- 〔做法第 1 步〕Stack 中的子元素依次入栈，后一个子元素覆盖前一个子元素，第一个子组件在最底层
