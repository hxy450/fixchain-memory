# 公共组件与页面结构

源端有多页共用的 @Composable、经 replace / add 放进 Activity 容器的 Fragment，或者派工里有公共组件表、共享原语清单、页内等价实现、几个并行任务都要写的共享组件时

## 触发族

- [多页共用的自定义组件](shared-component-callsites/index.md)（2 条）：源码里同一个自定义组件（@Composable）被多个页面调用，或 UI 清单把它列为共享组件；页面转换派工或巡检单只顾到眼前这一处调用点
- [公共组件库和共享原语的派工清单](shared-component-dispatch/index.md)（2 条）：派工要逐个写公共组件或把页面内联原语收敛到共享实现，读写顺序把被依赖的 Modifier 源文件排在后面，或清单只点名了规格 mapping 里的部分共享原语小节
- [拆成共享组件或子组件的 Fragment 的宿主](fragment-host/index.md)（3 条）：源端 Fragment 经 replace / add 放进某个 Activity 的容器、根布局带 padding 或背景、宿主 Fragment 有 ImmersionBar，派工、接线归属表或移交项按目标页结构给别的页加槽位，没写宿主和根布局的 padding、背景、沉浸由谁实现
- [公共组件未完成时的页内等价实现](inline-before-shared/index.md)（3 条）：公共组件库还没完成，派工写「同页内联等价实现优先」，没附 feature 规格里的显示公式条目，也没安排之后改用公共组件
- [公共组件表和 brief 的 PASS](component-layout-anchor/index.md)（1 条）：派工给了共享组件表、每行标着安卓 Adapter/item 布局或现有框架组件，brief 写回 final_state: PASS，却没逐个组件指回表里的一行
- [并行任务都要写的共享组件](shared-file-ownership/index.md)（1 条）：几个并行的页面转换任务都要用到同一个共享组件；派工没指定它的唯一作者，也没要求后来者先读已有文件再增量改
