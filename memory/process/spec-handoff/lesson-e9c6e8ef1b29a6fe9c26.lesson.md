# 沿用已生成页面、兄弟任务的写法或已有解析函数前，回到源码核对该片段的语义

ID：`lesson-e9c6e8ef1b29a6fe9c26` · 版本：14

[本主题](index.md)

## 何时使用

页面转换、公共组件抽取、切片接线或页面重建阶段，参照已生成页面中的同名控件、弹窗、列表、顶栏或导航栈写法时；数据层为新增接口方法复用已有的解析、封装函数时；复用工程已有的共享状态 key 时；按“与 Android 1:1 对齐”修改已有页面（含基线遗留骨架）时；在已有按钮、工具栏或面板上按 Android 契约改写时

## 适用情境

后写的 worker 同时读到源码与先前 agent 已生成的目标代码片段（@Builder 控件、输入弹窗、弹窗承载方式、列表键函数、顶栏折叠、图标控件行、安全控件样式、全屏遮罩、onReady 取栈写法、共享状态 key、登录结果解析函数等），准备当作项目约定直接沿用。或对齐任务在一个与源端结构不同的既有页面上进行，写者已读到源布局 XML。 也包括后一批执行代理把同批尚未验收的兄弟页（如只回显接口 JSON 的页面）当作模板，照同一模式写出更多页面。也包括 1:1 返修重写已有片段时，沿用目标端已有的尺寸、颜色、限制属性（如三框统一的 maxLength、硬编码字色）或注释里的结论（“源码未设，保真”“已裁定”），以及以仓内同族页面为模板复刻输入行时照搬其图标尺寸与光标色。 也包括目标页面在本轮前已有一版可用实现（占位按钮各带回调、页内简化面板、既有字号与字数上限），本轮契约已写明 Android 的按钮 → 动作绑定、跳转目标与参数及数值，写者只换图标、文字或颜色。也包括先例里夹带登记为不确定、近似或“需真机校对”的取值（弹窗族底色与圆角、折叠头部近似、M2 工具栏度量），或行为类先例（弹窗回调接线时序、链式弹层参数、解析循环、定位写法）只经过类型检查。

## 原因

已有目标代码可能带有尚未暴露的偏差，或依赖原来的输入来源、状态更新、挂载方式与生命周期。把它直接当成项目约定，会让先例覆盖当前已经读到的源端语义，并把同一偏差复制到更多文件。来源中的这些先例尚未经相应运行验证，不能仅凭存在相似写法推断当前场景可用；对齐已有页面时，旧骨架也可能包含源端没有的结构。另一应用的返修会话三次出现同一机制：以同族页面为模板写弹窗输入行，沿用其 24×24 图标和蓝色光标而没解析源 drawable；改写密码页时把只在一个源控件上的 maxLength 写回三个框、把未声明的字色硬编码；把旧注释“组头不可点，保真”当作源端结论继续扩写。 已有回调与数值同样是待核对的先例：只换显示内容会把旧槽位的回调带到新按钮上，页内简化面板、旧字号与旧字数上限也会以“保留既有实现”为名留下。另一应用的漫画阅读页如此：“票”按钮沿用旧槽位回调跳到购买章节页，底部目录仍开页内面板，字号与字数上限未按契约修改。

## 做法

1. 沿用前逐个核对片段在源码里对应的行为：参数是否随状态变化、输入约束是否真的阻止显示、条目更新后键是否变化、折叠是否连续、取值来源（响应头还是响应体）是否相同、本页与先例页的挂载方式（压栈还是嵌入容器）是否相同；核对通过再落盘，已有代码不能代替对源码的核对。以同族页面为代码模板时只复用结构和逻辑，复制来的每个尺寸、颜色和修饰符都回到当前源布局逐项核对，源中没有的属性不带入。
2. 已有写法与本处源码不一致时按源码实现，并在报告写明差异，不把近似复制到新文件。
3. 先例本身没有经过运行验证（弹窗打开路径、真机截图）时，不以“先例能用”推断可运行；某处写法被修复后，搜索同一写法的其他页面一并核对。
4. 对齐既有页面时先按源 XML 列组件清单（背景、标题栏、卡片子项、主按钮文案、页签/ViewPager、空态），与现有组件树逐项比对；源端不存在的区块替换，不在旧骨架上只调尺寸。
5. 旧代码注释里的结论（“源码未设/保真/已裁定”）当作待核实的假设，用源码和框架默认行为重新验证后再保留；用 replace_all 或多控件模板批量改写前，确认一并写回的每个属性在每个对应源控件上确实存在。
6. 在已有按钮或面板上对齐时，先按源端监听代码列“按钮 → 点击目标”表，并把契约中的数值与跳转（字号、字数上限、目标页与参数）逐条映射到现有表达式，再逐个改写；只换图标、文字或颜色不算对齐。改完列出每个按钮的资源与 onClick 目标：两个按钮指向同一目标、或某个分支失去入口时回源码复核；单独改一个按钮的动作时，把它原来承担的动作迁到 Android 中对应的按钮。
7. 先例中登记为不确定、近似或“需真机校对”的值不当作已验证的族定值沿用；行为类先例（回调接线、弹层参数、定位写法、解析循环）先确认已运行验证，类型检查通过不代表行为正确。发现先例与源不符时改正先例或登记，不为“保持一致”沿用。

## 可选检查

- 对齐既有页面后，用契约关键值（目标页名、数值、状态参数）检索本次改动处，确认没有只停留在样式层。

来源支持：40 张卡 · 13 次迁移 · 13 个应用

## 来源（按需复核）

- [case-0693d5ce6cf6356203d5](../../../store/cases/case-0693d5ce6cf6356203d5/215bdc9ac1103e9697c93c8c076a503330e1d6fb5026300ff05dde38528e0adf.json) · 结论：recommendation:2
  卡片版本：`215bdc9ac1103e9697c93c8c076a503330e1d6fb5026300ff05dde38528e0adf`
- [case-1740a4d06903ea105e81](../../../store/cases/case-1740a4d06903ea105e81/cf87962aef2d6207a6d5639da6272767750780198c34ce01489dbaf20cfd70d9.json) · 结论：recommendation:2
  卡片版本：`cf87962aef2d6207a6d5639da6272767750780198c34ce01489dbaf20cfd70d9`
- [case-18113e210e1369d79e1d](../../../store/cases/case-18113e210e1369d79e1d/37c16bc6650280d7876fddb5a21db4abf1271051790070ee84ba091ba04450fb.json) · 结论：recommendation:3
  卡片版本：`37c16bc6650280d7876fddb5a21db4abf1271051790070ee84ba091ba04450fb`
- [case-1a45d524753afa529084](../../../store/cases/case-1a45d524753afa529084/2807a4c69a6232bb5edd6e4702d1bef0293be11ece7d3f34b6704c7718fb981c.json) · 结论：diagnosis
  卡片版本：`2807a4c69a6232bb5edd6e4702d1bef0293be11ece7d3f34b6704c7718fb981c`
- [case-1ff61bb8eea97c7cac7f](../../../store/cases/case-1ff61bb8eea97c7cac7f/cc69235df441f52f2023b37f688670cb3c8ffddec1751b9653b3aefd35c321f7.json) · 结论：recommendation:4
  卡片版本：`cc69235df441f52f2023b37f688670cb3c8ffddec1751b9653b3aefd35c321f7`
- [case-3045f4019d7d543e18ca](../../../store/cases/case-3045f4019d7d543e18ca/c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451.json) · 结论：diagnosis
  卡片版本：`c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451`
- [case-31852e28af4327a408a3](../../../store/cases/case-31852e28af4327a408a3/7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b.json) · 结论：diagnosis, recommendation:3
  卡片版本：`7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b`
- [case-37ef7d33ab4655385e6f](../../../store/cases/case-37ef7d33ab4655385e6f/fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee.json) · 结论：recommendation:2
  卡片版本：`fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee`
- [case-50d84809509dfadabf5c](../../../store/cases/case-50d84809509dfadabf5c/3a16a2374d1dd50247cc80dd1707340b25e9c600e8417b561842d26f604cac71.json) · 结论：recommendation:3
  卡片版本：`3a16a2374d1dd50247cc80dd1707340b25e9c600e8417b561842d26f604cac71`
- [case-5b1b0e2ce03be0dc6d37](../../../store/cases/case-5b1b0e2ce03be0dc6d37/c2112b78bf1d0d405234089df63fe6c8009042f68c7baccf3b7dfbd9a1685e48.json) · 结论：diagnosis, recommendation:3
  卡片版本：`c2112b78bf1d0d405234089df63fe6c8009042f68c7baccf3b7dfbd9a1685e48`
- [case-605ca2c835a2d8b2950f](../../../store/cases/case-605ca2c835a2d8b2950f/5885d2629daf3e1bd7b6e0ace40ac6b4389e87598667a069721cffe49353fd43.json) · 结论：recommendation:3
  卡片版本：`5885d2629daf3e1bd7b6e0ace40ac6b4389e87598667a069721cffe49353fd43`
- [case-6597b7f7858db941262c](../../../store/cases/case-6597b7f7858db941262c/5df98131b17c6e84b2f61d4e454c9248bb40405f74bd41c3851a51f49d4e9697.json) · 结论：recommendation:5
  卡片版本：`5df98131b17c6e84b2f61d4e454c9248bb40405f74bd41c3851a51f49d4e9697`
- [case-66f3c1649b7b5c4f38b5](../../../store/cases/case-66f3c1649b7b5c4f38b5/686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140.json) · 结论：diagnosis, recommendation:2
  卡片版本：`686410a72e498ff1fb1d9233686e5ebc690a444c3056d62bc78d50dbcb257140`
- [case-701f2e2280bcc31423bd](../../../store/cases/case-701f2e2280bcc31423bd/f3ba6e8fd8e3b02acb710d8e9c4e889fa2e3cfd632ab2397ed300b3104f1c6c7.json) · 结论：recommendation:5
  卡片版本：`f3ba6e8fd8e3b02acb710d8e9c4e889fa2e3cfd632ab2397ed300b3104f1c6c7`
- [case-747484a613e86334516d](../../../store/cases/case-747484a613e86334516d/c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9.json) · 结论：recommendation:4
  卡片版本：`c17375c37c6410806f89e51707baf458f2a7269ddea6fe33e4ea348696489ff9`
- [case-7825d414bc05105dc41b](../../../store/cases/case-7825d414bc05105dc41b/3c1b1d29d57d0b890df4df71974dce93e548d9e54df40104b4a10e10cdaf3e12.json) · 结论：diagnosis, recommendation:3
  卡片版本：`3c1b1d29d57d0b890df4df71974dce93e548d9e54df40104b4a10e10cdaf3e12`
- [case-784ba4ab52f98f7156b6](../../../store/cases/case-784ba4ab52f98f7156b6/4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5.json) · 结论：diagnosis, recommendation:2
  卡片版本：`4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5`
- [case-7bc774bebe74d00dfa24](../../../store/cases/case-7bc774bebe74d00dfa24/9c871169a262da0828e8a64300d27a2cb61b81ca47dfcf4c5c08cadc35d48fa1.json) · 结论：recommendation:3
  卡片版本：`9c871169a262da0828e8a64300d27a2cb61b81ca47dfcf4c5c08cadc35d48fa1`
- [case-84754321501fb68838ca](../../../store/cases/case-84754321501fb68838ca/3f3463ed3d961b5111a1ac32e6c7a95587c06d7746f3ab9a54fe09afe015fd8a.json) · 结论：recommendation:2
  卡片版本：`3f3463ed3d961b5111a1ac32e6c7a95587c06d7746f3ab9a54fe09afe015fd8a`
- [case-85baa9234cc4f4798784](../../../store/cases/case-85baa9234cc4f4798784/1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a.json) · 结论：recommendation:2
  卡片版本：`1243dc28f5a4e89619d55835bc7a7b43cb63a97563ee91bef4b9ea9ed506757a`
- [case-8f78074db5808aa23638](../../../store/cases/case-8f78074db5808aa23638/b3b6cde3990bb317b9ab43ba04abccd05baf1f5541c2c9e770a36df00b18dd13.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`b3b6cde3990bb317b9ab43ba04abccd05baf1f5541c2c9e770a36df00b18dd13`
- [case-9058ac868b6feb3a04e0](../../../store/cases/case-9058ac868b6feb3a04e0/d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4.json) · 结论：recommendation:1
  卡片版本：`d8e013afe2706da7f1b19c1a0d603c05f971b4ebc0c4542f6fb5e8a956b3ebc4`
- [case-997587966a65e79790b5](../../../store/cases/case-997587966a65e79790b5/b893e565c641c2141df0a6dae2afe87d78c68ad3e20a1cc0aa1a5b41593261ab.json) · 结论：recommendation:4
  卡片版本：`b893e565c641c2141df0a6dae2afe87d78c68ad3e20a1cc0aa1a5b41593261ab`
- [case-9c819765c4d3d422d7bb](../../../store/cases/case-9c819765c4d3d422d7bb/edb469cf43fa95e5f671d901b420faffde0e1854f7090f89b85e3fd4d635e247.json) · 结论：recommendation:2
  卡片版本：`edb469cf43fa95e5f671d901b420faffde0e1854f7090f89b85e3fd4d635e247`
- [case-a3dc4d0187d7ddc456e8](../../../store/cases/case-a3dc4d0187d7ddc456e8/f859e7871c0c6c7b9d5e869a46ae4f3510862fa498179e0840d4b2f955a32599.json) · 结论：recommendation:3
  卡片版本：`f859e7871c0c6c7b9d5e869a46ae4f3510862fa498179e0840d4b2f955a32599`
- [case-ae26f8358584821ce4d4](../../../store/cases/case-ae26f8358584821ce4d4/739279181a7edf61aaddc81bc6550a650a12740e302f5bf7fdd385d674e76364.json) · 结论：diagnosis, recommendation:3
  卡片版本：`739279181a7edf61aaddc81bc6550a650a12740e302f5bf7fdd385d674e76364`
- [case-affc8177e24ce9f71b47](../../../store/cases/case-affc8177e24ce9f71b47/f804b4003f34d058922dd2194e93f12bd78d006541c928c92bb6334c33252bae.json) · 结论：recommendation:3
  卡片版本：`f804b4003f34d058922dd2194e93f12bd78d006541c928c92bb6334c33252bae`
- [case-b5cceb2aa00d9c09058a](../../../store/cases/case-b5cceb2aa00d9c09058a/4a5b768fc91e1626772278892e1df919da88d742482acc9977b4ebc4b3b94418.json) · 结论：recommendation:4
  卡片版本：`4a5b768fc91e1626772278892e1df919da88d742482acc9977b4ebc4b3b94418`
- [case-bd76c218ac0773e443e3](../../../store/cases/case-bd76c218ac0773e443e3/e2da61f6059badfaf173eab73983fdf4e3ad82215573fad87116e60e2727ca7e.json) · 结论：diagnosis, recommendation:1
  卡片版本：`e2da61f6059badfaf173eab73983fdf4e3ad82215573fad87116e60e2727ca7e`
- [case-c40332380c19d002090d](../../../store/cases/case-c40332380c19d002090d/20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9.json) · 结论：recommendation:4
  卡片版本：`20bb7342349e54c008f9c46196d69487091c394890d3a5be07f12a43862455f9`
- [case-c4b0a71b1ff405c63013](../../../store/cases/case-c4b0a71b1ff405c63013/cf40af4452211b1663624d236fa85bb538c2147abecce670074002e2a91b17cc.json) · 结论：diagnosis, recommendation:3
  卡片版本：`cf40af4452211b1663624d236fa85bb538c2147abecce670074002e2a91b17cc`
- [case-c4e5b6ca6da92a568d18](../../../store/cases/case-c4e5b6ca6da92a568d18/7fd836a3b3b3874e2f2f95df046b726804dddfab303ad8497ada8936a28e0940.json) · 结论：recommendation:2
  卡片版本：`7fd836a3b3b3874e2f2f95df046b726804dddfab303ad8497ada8936a28e0940`
- [case-c9cc6663456a2ef02f89](../../../store/cases/case-c9cc6663456a2ef02f89/ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace.json) · 结论：recommendation:2, recommendation:3
  卡片版本：`ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace`
- [case-ca8dec09be8655edbb02](../../../store/cases/case-ca8dec09be8655edbb02/dfbbf6d269dc5f5443ab807c7dcd9499347ae85860a1e024533fbcff818efb49.json) · 结论：diagnosis, recommendation:3
  卡片版本：`dfbbf6d269dc5f5443ab807c7dcd9499347ae85860a1e024533fbcff818efb49`
- [case-caa0a4c6289286b0e6ba](../../../store/cases/case-caa0a4c6289286b0e6ba/b624132bc14cc2155a05833b935147b64bcfa0f884e37d7ede212a5e2200f31f.json) · 结论：recommendation:4
  卡片版本：`b624132bc14cc2155a05833b935147b64bcfa0f884e37d7ede212a5e2200f31f`
- [case-cdc57384e71fa7c70345](../../../store/cases/case-cdc57384e71fa7c70345/037233e15fe0fb44c8cc98e82060508d223a5a4eed01a1c90f1e7f451bdb00c7.json) · 结论：diagnosis, recommendation:2
  卡片版本：`037233e15fe0fb44c8cc98e82060508d223a5a4eed01a1c90f1e7f451bdb00c7`
- [case-d53f19cb359b879b340c](../../../store/cases/case-d53f19cb359b879b340c/fdb06a9c57661465138e471a87aa9c64a2610ed9246cc863781e5acd92e42761.json) · 结论：recommendation:3
  卡片版本：`fdb06a9c57661465138e471a87aa9c64a2610ed9246cc863781e5acd92e42761`
- [case-e364fc4ed310fa72992c](../../../store/cases/case-e364fc4ed310fa72992c/2b4a4e92f4bcdcd4672326d483f8ad02c9f7ab2e80432ffdf3280f4ed19f2cbb.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`2b4a4e92f4bcdcd4672326d483f8ad02c9f7ab2e80432ffdf3280f4ed19f2cbb`
- [case-e3cd92963aa40d922fdc](../../../store/cases/case-e3cd92963aa40d922fdc/9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620.json) · 结论：diagnosis, recommendation:3
  卡片版本：`9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620`
- [case-f226842558d82e3f3ad9](../../../store/cases/case-f226842558d82e3f3ad9/1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7.json) · 结论：recommendation:4
  卡片版本：`1ae9be15ea67757c6cc912d634ea8b20b6d5e09d750e9e93dd6fa6131ccf14a7`
