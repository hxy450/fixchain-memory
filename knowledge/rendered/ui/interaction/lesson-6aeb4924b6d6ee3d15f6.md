# 源端 clickable 吞触摸或组件实例带通用属性时显式写 hitTestBehavior：空 onClick 不阻断，实例外有缺省命中的包装节点

## 何时使用

界面实现阶段，把 Android 的 clickable、不可点击 View 与 FrameLayout 层序翻成 ArkUI 叠放层（撤销条、浮动按钮组、提示条、窗口级图层），决定触摸由谁消费、是否透传时

## 适用情境

源端条体或按钮 clickable=true 吞掉触摸、不下穿到下层列表，或不可点击的提示条覆盖工具栏而不拦截；目标在 Stack 中叠放自定义组件，宿主层可能已设 Transparent，组件实例上写了 margin、padding、position 等通用属性，或用 OverlayManager 挂 ComponentContent；写者准备用空 .onClick 表示“吞触摸”，或依赖组件缺省命中模式。

## 例外与边界

- 源端触摸归属随状态变的叠放层（例如抽屉打开时拦截、关闭时让下层可点），按各状态分别写命中模式并随状态切换；代码里已有按状态切换的 hitTestBehavior 保留，不统一改成某个固定值。

## 原因

ArkUI 是否拦截由命中测试决定，与有没有 onClick 无关：空 onClick 不改变命中模式，Transparent 宿主下的条体仍会让下层同时命中，下层的按下回调可能先执行并改掉状态。给自定义组件实例写通用属性时框架会生成缺省命中的 __Common__ 包装节点，它按自身区域参与命中、盖住其他控件；OverlayManager 上以自定义组件为根的 ComponentContent 也被包进缺省命中的代理节点（BuilderProxyNode），只给内层设 None 不起作用。

## 做法

1. 按源端触摸归属给每个叠放节点显式写 hitTestBehavior，不依赖缺省值：源端吞触摸、没有可点击子控件的节点用 HitTestMode.Block；含可点击子控件，或位于 Transparent 宿主下仍要阻断下层的条体，用 HitTestMode.BLOCK_HIERARCHY（自身与子节点响应、阻止优先级更低的兄弟与父节点，API 20 起提供）；只做定位或占位的包装节点用 None 或 Transparent。不用空 onClick 表示吞触摸。
2. 给自定义组件实例写 margin、padding、position 等通用属性时，同时在该实例上写 hitTestBehavior：只展示、不接收触摸的覆盖条用 None，子控件要可点而空白处透传的用 Transparent；也可以把这些属性移到外层系统容器上，再给该容器设命中模式。 width/height/zIndex 同样会生成包装节点；组件作者写层契约或头注释时写明“挂载实例上写命中模式，或调用处不写通用属性”，不声称组件内部根节点已不拦截；替换或换装挂载的组件时保留挂载点已有的 hitTestBehavior，组件契约不作为删除它的依据。
3. 用 OverlayManager.addComponentContent 挂窗口级图层时，只在需要显示的时段挂载，结束即 removeComponentContent；必须常驻时用 Stack 等系统组件作 ComponentContent 的根，并按交互态切换根节点的 hitTestBehavior，不依赖内层自定义组件上的 None。

## 可选检查

- 对每个叠放层实际点按：点目标节点时其下层的按下与点击回调不触发，点空白区时下层仍可达。

来源支持：2 张卡 · 已知 1 次迁移（部分未记录） · 已知 1 个应用（部分未记录）

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因 / 做法第 2 步〕给自定义组件设置通用样式时，相当于给它套了一个不可见的容器组件，样式设在这个容器上，而不是组件内部的根节点上
- 〔原因 / 做法第 2 步〕自定义组件实例上写了 margin、padding、position 等通用属性时，设备上出现缺省命中的 __Common__ 包装节点，它按自身区域参与触摸测试，会盖住它下面的其他控件
- 〔做法第 2 步〕只在组件内部的 Canvas 上设 HitTestMode.Transparent、而调用处给实例写了 width、height、zIndex 时，外层包装节点按缺省模式拦截触摸，下层控件点不到
- 〔原因 / 做法第 3 步〕以自定义组件作 ComponentContent 的根、经 OverlayManager.addComponentContent 挂载时，它被包进缺省命中的代理节点（BuilderProxyNode），只给内层自定义组件设 HitTestMode.None 时图层仍拦截触摸
- 〔做法第 1、2 步〕hitTestBehavior 不设时为 HitTestMode.Default：自身及子节点响应触摸测试，但阻塞兄弟节点的触摸测试，不影响祖先节点
- 〔做法第 1、2 步〕HitTestMode 各值：Block 自身响应，阻塞子节点、兄弟节点和祖先节点；Transparent 自身和子节点响应，不阻塞兄弟节点和祖先节点；None 自身不响应，不阻塞子节点、兄弟节点和祖先节点；BLOCK_HIERARCHY（API 20 起）自身和子节点响应，阻止所有优先级较低的兄弟节点和父节点参与触摸测试
