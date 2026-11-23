# 负责上抛自身可见性的组件必须常建，不被条件构建或 Visibility.None 包住

## 何时使用

界面实现阶段，翻译“容器初始隐藏、内部组件常驻并自行通知宿主显示”的结构，或向他人预留的条件槽位嵌入组件时

## 适用情境

源容器 visibility=gone，但内部 Fragment 在 onCreate 即挂载，并由它调用宿主的可见性方法；目标用 if 或 Visibility 控制容器。

## 例外与边界

- 常建之后仍要保住源端 gone 的两点：不占位、不可点。opacity 设为 0 只是透明，组件在布局中照样占位，要同时把高度压到 0 或移出布局流；命中要另外关，整棵子树都不响应用 hitTestBehavior(HitTestMode.BLOCK_DESCENDANTS)（API 20 起），HitTestMode.None 只让自身不响应、不挡子节点。

## 原因

ArkUI 中 if 为假或 Visibility.None 下的自定义组件不会实例化（aboutToAppear 不执行，修复期实测），唯一能把可见性置真的组件不存在，形成死锁。

## 做法

1. 让该组件常建（高度 0 加 clip，或用 opacity、命中控制显示），不用 if 或 Visibility.None 包住。
2. 向宿主槽位嵌入组件前读取包住槽位的构建条件；若条件依赖本组件上抛的状态，先改宿主为常建或登记接线问题。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕if 的条件分支变化时，先移除此前分支构建的全部子组件，再执行新分支的构建函数；条件为假且没有 else 时不创建任何内容
- 〔原因〕Visibility.Hidden 隐藏但参与布局占位；Visibility.None 隐藏且不参与布局、不占位（文档没有写 None 下组件是否实例化）
- 〔原因〕卡里设备上，条件构建为假以及 Visibility.None 下的自定义组件都没有实例化（aboutToAppear 不执行）；强制设为 Visible 后 aboutToAppear 随即执行
- 〔做法第 1 步〕组件没有另设 clip 时不裁剪超出自身范围的子组件；设为 true 后子组件超出部分不可见，也不响应绑定的手势事件
