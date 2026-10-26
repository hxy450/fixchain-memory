# 源端 clickable 吞触摸或组件实例带通用属性时显式写 hitTestBehavior：空 onClick 不阻断，实例外有缺省命中的包装节点

ID：`lesson-6aeb4924b6d6ee3d15f6` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android 的 clickable、不可点击 View 与 FrameLayout 层序翻成 ArkUI 叠放层（撤销条、浮动按钮组、提示条、窗口级图层），决定触摸由谁消费、是否透传时

## 适用情境

源端条体或按钮 clickable=true 吞掉触摸、不下穿到下层列表，或不可点击的提示条覆盖工具栏而不拦截；目标在 Stack 中叠放自定义组件，宿主层可能已设 Transparent，组件实例上写了 margin、padding、position 等通用属性，或用 OverlayManager 挂 ComponentContent；写者准备用空 .onClick 表示“吞触摸”，或依赖组件缺省命中模式。

## 原因

ArkUI 是否拦截由命中测试决定，与有没有 onClick 无关：空 onClick 不改变命中模式，Transparent 宿主下的条体仍会让下层同时命中，下层的按下回调可能先执行并改掉状态。给自定义组件实例写通用属性时框架会生成缺省命中的 __Common__ 包装节点，它按自身区域参与命中、盖住其他控件；OverlayManager 上以自定义组件为根的 ComponentContent 也被包进缺省命中的代理节点（BuilderProxyNode），只给内层设 None 不起作用。

## 做法

1. 按源端触摸归属给每个叠放节点显式写 hitTestBehavior，不依赖缺省值：源端吞触摸、没有可点击子控件的节点用 HitTestMode.Block；含可点击子控件，或位于 Transparent 宿主下仍要阻断下层的条体，用 HitTestMode.BLOCK_HIERARCHY（自身与子节点响应、阻止优先级更低的兄弟与父节点，以本机 SDK 的 HitTestMode 声明为准）；只做定位或占位的包装节点用 None 或 Transparent。不用空 onClick 表示吞触摸。
2. 给自定义组件实例写 margin、padding、position 等通用属性时，同时在该实例上写 hitTestBehavior：只展示、不接收触摸的覆盖条用 None，子控件要可点而空白处透传的用 Transparent；也可以把这些属性移到外层系统容器上，再给该容器设命中模式。
3. 用 OverlayManager.addComponentContent 挂窗口级图层时，只在需要显示的时段挂载，结束即 removeComponentContent；必须常驻时用 Stack 等系统组件作 ComponentContent 的根，并按交互态切换根节点的 hitTestBehavior，不依赖内层自定义组件上的 None。

## 可选检查

- 对每个叠放层实际点按：点目标节点时其下层的按下与点击回调不触发，点空白区时下层仍可达。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

## 来源（按需复核）

- [case-2f1588d16e333f764904](../../../store/cases/case-2f1588d16e333f764904/41137c9c24a737ad0b84d76a9778aff790e746f40c6871c34300524f64e73aa1.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`41137c9c24a737ad0b84d76a9778aff790e746f40c6871c34300524f64e73aa1`
- [case-d38fbc2e9b64b7c3338b](../../../store/cases/case-d38fbc2e9b64b7c3338b/0c81ee0d0f88b740ca143860bd386d61a44268d1703fbe3e4e239c5375013a71.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:5
  卡片版本：`0c81ee0d0f88b740ca143860bd386d61a44268d1703fbe3e4e239c5375013a71`
