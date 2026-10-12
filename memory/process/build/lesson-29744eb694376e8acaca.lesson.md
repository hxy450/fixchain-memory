# 编译修复只改报错定位的行与符号，不以删掉功能或语义不同的替代换取通过；必须整文件重写时逐段对照上一版，未报错的写法原样保留

ID：`lesson-29744eb694376e8acaca` · 版本：6

[本主题](index.md)

## 何时使用

编译修复阶段，为修某条编译错误决定局部修改还是整文件重写时

## 适用情境

修复循环用 here-string 或 Write 整文件重写页面来处理导入导出、@Entry 等报错，文件里还有未被报错的组件用法（页签 builder、状态绑定、导入等）。或报错只涉及某个导入或符号，修复者考虑把相关功能块（如自绘趋势图）整体换成占位以通过编译。也包括报错来自调用了 SDK 不存在的参数字段（如在 AlertDialog 参数里写自定义内容 builder），修复者准备删掉该字段连同其中承载的控件。也包括编译报某 API 在当前上下文不受支持（如服务卡片页不支持通用尺寸事件），删掉该调用后能编译但行为退化（取不到尺寸、状态永不赋值）。 也包括报错指向 SDK 中不存在的 API（如映射给单调时钟的 Web API），修复者准备换成语义不同的替代（如会随校时跳变的墙钟）。也包括报错指出枚举没有某成员（如 FontWeight.SemiBold），修复者准备按名称就近批量替换成相邻成员（如 Medium）。也包括类型不符的报错（如 Resource 不能赋给只收 string 的 PopupOptions.message），修复者准备把本地化资源换成枚举名、原始标识等字面串。

## 原因

整文件重写时顺手换掉未报错的写法，会引入新的编译错误或行为变化；修复者只盯着原报错，新错误被当成原问题的延续，一直拖到交付。来源中为修导入导出错误重写主页，把未见报错的 @Builder 页签改成不存在的 { title } 重载，构建因此在生成结束时仍失败。又一应用中构建修复者看到的日志只报 '@kit.ArkUI' 未导出两个 Canvas 相关类型，却把整个 Canvas 趋势图换成文字点列，规格要求的 15 日折线随之消失，直到用户返修才重建。第三个应用里，修复者为消除 AlertDialog 不存在的 builder 字段引发的连锁错误，把警告文本降成 message，同时删掉了“不再提示”复选框及其偏好写入，只留注释待后续切片回补；它自己也判断真正对等的是自定义弹窗，截至观察截止复选框仍缺失。删掉承载行为的调用后，若注释与文件头仍声称该行为存在，后续读者会以为功能完整，退化被掩盖到运行时。第四个应用里，编译门把找不到的单调时钟换成墙钟，只把差异作为缺口上报，主线程也只记入遗留披露，帧计时语义一直错到返修。

## 做法

1. 只改报错指向的行和符号；必须重写时先与上一版逐段对照，未报错的组件用法保持原样，确需改动的先按 API 签名或编译器重载提示确认可用形态。
2. 报错只指向导入或单个符号时，修正导入（如改用全局可用的类型）并保留功能；确需降级时回写规格、把对应验收保持未完成，不以占位替换后报告通过。
3. 报错指向不存在的 API 字段时，改用能承载同一内容的可用 API（例如用自定义弹窗承载复选框），而不是连内容一起删掉；替换缺失的 API 或枚举成员时，按原调用注释与规格写明的语义在本地 d.ts 中检索候选并读完声明，包括属性方法是否另接受数值、字符串等能精确表达原值的形式（如 fontWeight 接受 600），不按名称就近换成相邻成员；只剩语义不同的替代时不在门内落地，作为决策缺口回报，由主线程在生成期补查修正，不只记入遗留披露；只能临时降级时按占位规则登记丢失的控件与写入、回补位置，并在报告中列为行为差异。
4. 确需删除承载核心行为的调用时，同步改掉仍声称该行为存在的注释与文件头，把行为退化和可替代的平台 API 列为待修项回报，不以“编译通过”收口。
5. 类型不符时只转换类型、不换数据来源：Resource 赋给只收 string 的字段时，用 resourceManager.getStringSync($r(...).id) 一类写法取当前语言的字符串，或改用接受 Resource 或自定义 builder 的重载；不以枚举名、rawName 等字面串代替本地化文案。要以“源端本来如此”解释改动时，先回读对应源码。

来源支持：9 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-036361d8949e7daf5247](../../../store/cases/case-036361d8949e7daf5247/c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79.json) · 结论：recommendation:4
  卡片版本：`c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79`
- [case-0848ab137044cb92d1bc](../../../store/cases/case-0848ab137044cb92d1bc/1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37.json) · 结论：recommendation:7
  卡片版本：`1b8dbd30951aec40912fda717800da9383cdc52429f479cbae2d27c1fd708e37`
- [case-11c15d99c36e52d8aa59](../../../store/cases/case-11c15d99c36e52d8aa59/13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af.json) · 结论：diagnosis, recommendation:1
  卡片版本：`13cf01300f38651f13dba6e9eab38436d577ff8111953ca3aa037fc488b886af`
- [case-3b8b620c1c7fa2848a34](../../../store/cases/case-3b8b620c1c7fa2848a34/2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd.json) · 结论：diagnosis, recommendation:4
  卡片版本：`2c8f9548575702e3dd4840957d2d99053daa0e3fe45f93f40765b5cabcb618bd`
- [case-77c6596fcdf362f9e832](../../../store/cases/case-77c6596fcdf362f9e832/c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a.json) · 结论：recommendation:6
  卡片版本：`c81c56fb66d294cfd767c2c43e5bcfb480ef9cccbdcfc212d5d607410c13675a`
- [case-7ced02d9c41ab6f4919a](../../../store/cases/case-7ced02d9c41ab6f4919a/9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d.json) · 结论：recommendation:4
  卡片版本：`9fd2c38d185384a27ad8b217bf729215c10890cf8902cf113c94de01745a600d`
- [case-9d7fa754a567e2ecec7e](../../../store/cases/case-9d7fa754a567e2ecec7e/08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28.json) · 结论：diagnosis, recommendation:2
  卡片版本：`08068dd456a4c32cc1327c39f339215b49dab4ffc8f5a25dc8024b7112ebbd28`
- [case-abb1f63235ed950c4841](../../../store/cases/case-abb1f63235ed950c4841/f5b824a9ef757f00ab0eb7c877fdd33947c2fdd54420510962728ba20a259f79.json) · 结论：recommendation:1, recommendation:2
  卡片版本：`f5b824a9ef757f00ab0eb7c877fdd33947c2fdd54420510962728ba20a259f79`
- [case-d8867d30fe76e4d44ceb](../../../store/cases/case-d8867d30fe76e4d44ceb/3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932.json) · 结论：diagnosis, recommendation:3
  卡片版本：`3537efdf372896502b8a0b63e22b06ece4e7d54e2c06ca2c8c0ff730e6a5f932`
