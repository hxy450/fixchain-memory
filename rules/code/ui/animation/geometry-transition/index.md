# 共享元素转场的 geometryTransition

agent 会看到什么：读到 Compose SharedTransitionLayout 里 Modifier.sharedBounds 包住 Modifier.sharedElement，或已写好的对端文件里的 .geometryTransition；产物里同一配对子树外层和内层各挂一个 .geometryTransition

## 规矩

- rule-f2918494e74d｜Compose 两层共享转场，每端只在外层挂一个 geometryTransition，不嵌套｜读到：SharedTransitionLayout 内用 Modifier.sharedBounds(…"<id>-bounds"…) 包住带 Modifier.sharedElement(…id…) 的内容，两层 key 不同，两端（列表卡与详情浮层）各有这两层；写错：同一配对子树里外层容器挂了 .geometryTransition(`${id}-bounds`)，内层组件根节点又挂 .geometryTransition(id)，嵌套两对
- rule-74a97117cc4a｜后写的一端与已写好的一端配对时，核对对方的键和有无嵌套，发现嵌套不照样镜像｜读到：已写好的对端文件里外层容器有 .geometryTransition(`${id}-bounds`)，它的子组件里又有 .geometryTransition(id)；写错：后写的一端照样镜像成外层加内层两处 .geometryTransition，交回报告里没提对端嵌套
