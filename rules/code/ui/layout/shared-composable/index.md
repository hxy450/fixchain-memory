# 项目自定义 Compose 组件和共享组件

agent 会看到什么：源端调用项目自己的 @Composable 组件（CircleShape、ContentScale.Crop、裁切写在组件定义里，调用点只传尺寸和资源），对应目标的 Image 外观、共享 @Component 的参数和页内副本

## 规矩

- rule-3e2ca890de8e｜源码调用项目自定义图片组件时，打开其定义把形状、裁剪和 contentScale 一起翻译｜读到：调用点是从项目 ui/components 包 import 的自定义图片组件，只传 imageRes 和 Modifier.size(...)；`CircleShape`、`ContentScale.Crop` 在组件定义里；写错：ArkTS 写成 Image(...).objectFit(ImageFit.Contain)，没有 borderRadius 和 clip
- rule-3d0b380ba3a0｜把共享组件替换进已有页面时按源码调用点和组件默认，不为旧外观覆写形状参数｜读到：源码调用点没有传形状参数，组件定义里默认 CircleShape；写错：给共享组件新增 `cornerRadius` 参数并在调用处传 `cornerRadius: 0`，沿用旧页面的矩形外观
- rule-a5383afb5b98｜共享组件已存在且验收目标指向它时，页内副本要替换成共享组件，不能两套并存到交付｜读到：规格的验收目标是 components 下的共享组件，页内却有一份等价的 @Component / @Builder 副本；写错：交付时页内副本仍在用，components 下的共享 @Component 没有任何页面 import；理由写成修改范围只有本页、只解除标记
- rule-32e0e4979095｜按计划把页面局部实现换成共享组件前，先比对被删的 builder，缺的补进共享组件｜读到：计划或派工要求把页面里局部的 @Builder 实现换成共享组件调用；写错：改动删掉了页面里原有的 @Builder 调用、换成共享组件，被删的 builder 里有共享组件对应变体没有的子节点（如勾选、第二行文案）
- rule-6e6778df5d05｜页面源码用了共享组件时，复用目标共享件，不内联近似版、不照搬先例｜读到：页面源码调用了源工程公共文件里定义的共享组件或修饰符（如包着 `LinearProgressIndicator()` 的加载条、自定义滚动条 Modifier）；写错：页面里内联了近似版（如 `Progress({ value: 30 })`、24vp 的 `LoadingProgress`），或注释写照兄弟页写法、「既有决策」「无 ArkUI 等价」后照搬
- rule-daac83717d2a｜源端由调用方 Modifier.size 给图片子组件定尺寸时，目标在槽外层或调用处写 .width/.height｜读到：Compose 调用方把 Modifier.size(...) 当作 modifier 参数传给图片子组件，有图和无图分支共用同一个尺寸修饰符；被嵌的图片组件自身没有尺寸参数；写错：拆成 @Builder 槽或接线调用被嵌组件后，有图分支的槽外层容器和调用处都没有 .width(...)/.height(...)，只有占位分支写了尺寸；FWD-REF 注释里也没写尺寸
- rule-6a5d719c0de0｜用共享包装组件替换页内副本、去掉宿主显式高度前，先查组件 build() 里的 '100%'｜写错：宿主外层原来写死的 .height(N) 被删掉、改用共享包装组件，而组件 build() 里有 .height('100%') / .width('100%') 的节点，父级没有确定尺寸
