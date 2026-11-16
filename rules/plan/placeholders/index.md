# 占位登记与前向引用

交回的产物里有 placeholder-registry 条目、FWD-REF / UNC 标记、// HANDOFF: 行、resolve_by、近似项或资源未就绪的登记，或者有留给后续切片的交互、数据和事件时

## 触发族

- [延后交互的占位登记内容](deferred-interaction-registry/index.md)（12 条）：源端的点击、跳转、来源分支、外部入口和数据钩子被延后给别的切片时，FWD-REF 标记、占位登记和移交项里写了什么（槽名、resolve_by、目标页、源端行为）
- [占位的关闭和解除](placeholder-closing/index.md)（14 条）：收口或收敛时把 forward-ref / UNC 占位关单、标 resolved、删掉 FWD-REF 标记，或把占位对应的入口记成已接通
- [占位改挂延后和延后项的归属](placeholder-retag-defer/index.md)（10 条）：收口或复审时把占位的 resolve_by 改成「集成期」、外部视觉核验（a2h-verify）或 deferred，或保持 registered 推给别人；页面报告里的延后项没有落到谁的任务
- [新登记占位的必要性和写法](placeholder-registering/index.md)（10 条）：实现或转换时新登记的 UNC / forward-ref-uncertain 占位、待收敛项、交给收口者的 HANDOFF，以及 FWD-REF 和登记里写的源方法名
- [不确定项和近似项的保留与复核](uncertain-retained-items/index.md)（7 条）：登记里的 UNC 不确定项、retained 近似项、「平台无此 API」类占位，在回执、派工、收口里被保留、预写「保留」、改挂 verify 阶段或标成已解决
- [HANDOFF 和待分配 P-ID 的登记](handoff-registration/index.md)（8 条）：「由某入口装配 / 接线阶段决定」的散文注释、上游报告的 open_question、Base handoff 里的 Suggested P-ID、留给后续批次的媒体尺寸，和源码 // HANDOFF: 行、registry、被点名切片的派工之间对不对得上
- [未就绪资源资产的登记](pending-asset-registry/index.md)（4 条）：占位登记或交付说明里有资源未就绪的条目（resource-pending-asset、P-RES-ASSET、资产类 FWD-REF），触发条件写「资产就绪」、owner 或 resolve_by 留空、资源到位后仍是 registered，或源图分辨率远低于目标显示区却被放大充当正式资源
- [占位登记里的前向引用和不确定项](fwd-ref-and-uncertain/index.md)（2 条）：规格或派工里有由后续切片提供的依赖、用自拟正则近似的校验，交回的占位登记里缺前向引用条目，或 UNC 不确定项的说明只有猜测
- [动画和阴影的保真度降级登记](fidelity-downgrade/index.md)（4 条）：源端有动画矢量图标、Compose elevation 阴影，交回的占位登记把永久降级登成 resolve_by 后续切片的 forward-ref 或 resource-pending-asset，或者单层 .shadow 近似没有登记成近似项
- [就绪事件和缓存键的前向引用](ready-event-fwd-ref/index.md)（1 条）：规格或源码写明某就绪事件在「计数满或定时兜底」后发布、启动流程在缓存为空时等它，占位登记把兜底也列为悬置，FWD-REF 说明称「与源等待语义等价」却没列等待方和发布者
- [FWD-REF 的 resolve_by 承接切片](fwd-ref-resolve-by/index.md)（4 条）：覆盖矩阵里承接的切片标为 simple/stub，或页面要加载远端数据而 UI-only 转换写成数据前向引用，占位登记里 FWD-REF 的 resolve_by 指向一个没有 wires、没有数据提供方的切片
- [留给功能切片的长按 ContextMenu](context-menu-fwd-ref/index.md)（1 条）：页面规格的菜单或导航表写「长按 ContextMenu」、交互留给后面的功能切片，占位登记里没有这项 FWD-REF，页面代码里长按已照兄弟页写成直接进多选
- [占位登记里的条目](placeholder-entries/index.md)（2 条）：占位登记里某组件只记了一项近似（如溢出判定用字符数阈值），源组件的其他能力（链接、overflow、按压反馈、容器色）既没实现也没登记；或者条目只写「等价于源端某谓词」，没列条件和出处
