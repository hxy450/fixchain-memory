# 源码证据与页面元数据

交回的 meta.json、基线快照或源码理解笔记里有页面元数据、合成的快照，或写了没读到定义的谓词、空子模块里的实现、声明没保证的回调顺序、实现建议的出处这类不确定项时

## 触发族

- [页面的源码布局和合成的 meta.json](layout-meta-json/index.md)（3 条）：读到页面类用 ViewBinding / DataBinding（.databinding 包里的绑定类、android:onClick="@{…}"），多模块里有同名布局 XML；合成的 meta.json 里 layout_sources 指向别的模块，clickable_elements 是 []、navigation_targets 为 {}
- [没有真机 dump、由源码合成的基线快照](synthesized-snapshot/index.md)（2 条）：基线快照的 meta.json 标 view_xml_synthesized 或 confidence medium、bounds 为空、没有真机 UIAutomator dump，规格把源码字面 dp 直接写成「判:visual」判据，或写「近乎不可见」「parity 保留」这类定论
- [只读到调用、没读到定义的辅助谓词](undefined-helper-predicate/index.md)（1 条）：读到的源码片段只有辅助谓词（如「是否在播放态」）的调用，没有它的定义；源码理解笔记写「谓词 = state == PLAYING || PAUSED」这类凭名称推断的定义，没标未读到
- [实现建议里的去重和上限属性](advice-dedupe-limit/index.md)（1 条）：审计或规格的「最小链」一类实现建议里写的去重、上限属性（如「有界去重队列」），以及它是源端已核行为还是鸿蒙适配建议
- [声明没写先后的平台回调](callback-order-unknown/index.md)（2 条）：@ohos.xml 等声明里没写先后、也没保证返回值的回调（attributeWithTagCallbackFunction 与 START_TAG、getNamespace()）；源码笔记里对这类不确定项的说法
- [未检出子模块里的关键实现](missing-submodule/index.md)（1 条）：源端读写流交给子模块里的工具函数，.gitmodules 有 URL 而子模块目录为空、只见调用点；规格里按读侧反推出的数据格式和逐字段 AC
- [仓库里没有源码的三方库（二进制依赖）](binary-third-party-lib/index.md)（11 条）：读到 Gradle 依赖里的三方库坐标（implementation、@aar、jar、libs.versions.toml），源码只 extends 或调用库类、布局里只有库的自定义 View，库的源码和资源不在仓库里；规格写「源码不在本仓库」「内部 UI 不可见 → 自研」「默认样式即可对齐」「待核自由度」，或跨栈映射只写「→ Toast / 自研 / 自实现」、把猜出的库行为写成确定契约
- [规格里标「[推断]」写入的平台行为](inferred-platform-behavior/index.md)（1 条）：交回的规格条目标「[推断：框架…标准行为]」写入 ActionBar、showAsAction、平台主题外观这类平台默认行为，没附框架源码或平台资源的核对来源，也没列为待核
- [被当作先例照抄的同批生成代码](unverified-generated-precedent/index.md)（1 条）：要照着写的兄弟实现是同一次迁移里生成的代码、没有运行验证的记录；源码理解笔记或注释把这套写法称作「已验」的形态或先例
