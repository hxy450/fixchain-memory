# process/secondary-over-source

规格、合成快照、清单映射或已生成代码等二手产物取代源码成为实现依据而发生漂移

[上一级](../index.md)

## 本级经验

- [共享组件挂载页面以源宿主容器 replace/add 为准](lesson-34c8ac69ad849f8c24e1.lesson.md) · 阶段：spec/plan/execute · 信号：FragmentTransaction, replace(, add(, Fragment
- [共享组件替换页面片段前逐项比对源码视觉](lesson-ad6f23b88f09b55dd92a.lesson.md) · 阶段：execute/converge · 信号：orphan component, @Builder, borderRadius, fontColor
- [写页前读源 ViewModel/Service 列行为清单](lesson-1997518f92b444368073.lesson.md) · 阶段：execute · 信号：ViewModel, Service, Screen, DAO
- [合成快照点击清单空时按源布局 onClick 绑定实现跳转](lesson-3ea52b78643f49c13cd1.lesson.md) · 阶段：spec/execute · 信号：android:onClick, @{page::, view_xml_synthesized, clickable_elements
- [多模块同名布局按页面类模块与 Binding 类解析](lesson-d75ddb53d6609b35d025.lesson.md) · 阶段：spec/execute · 信号：layout_sources, ViewBinding, DataBinding, fragment_mine.xml
- [沿用已生成页面或兄弟写法前回源码核对语义](lesson-e9c6e8ef1b29a6fe9c26.lesson.md) · 阶段：execute/repair · 信号：@Builder, onReady, maxLength, replace_all
- [派工要求按源码确认的值回源码核对，没读到标未核实](lesson-93214f5a49c4d1d82316.lesson.md) · 阶段：plan/execute · 信号：kapt stub, .kt, Interceptor, grep
- [规格与源码冲突时按源端语义实现并标注差异](lesson-7a065e8fe384b8c462cc.lesson.md) · 阶段：execute/repair · 信号：decision ledger, .d.ts, AC, HARD
