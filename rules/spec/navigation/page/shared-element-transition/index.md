# Compose 的共享元素转场（sharedElement、sharedBounds）

agent 会看到什么：读到源端 Modifier.sharedBounds("<id>-bounds") 包住 Modifier.sharedElement(id)、两层 key 不同；规格把 id 值域写成两对、只写「geometryTransition(id) 双端绑定」或原样列出源端两层 key，没写每端用哪个键、挂在哪个节点、内层不再挂

## 规矩

- rule-74fe111a0b73｜两层共享转场写成目标契约时，规格写明每端一对、用哪个键、挂哪个节点、内层不再挂｜读到：源端 Modifier.sharedBounds("<id>-bounds") 包住 Modifier.sharedElement(id)，两层 key 不同；写错：规格把 id 值域写成「`${id}` 与 `${id}-bounds` 两对」，或只写「geometryTransition(id) 双端绑定」而没写用哪个键、挂在哪个节点、内层不再挂第二个；页面结构一节原样列出源端两层 key
