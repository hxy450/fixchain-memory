# 沿用已生成页面、兄弟任务的写法或已有解析函数前，回到源码核对该片段的语义

ID：`lesson-e9c6e8ef1b29a6fe9c26` · 版本：10

[本主题](index.md)

## 何时使用

页面转换、公共组件抽取、切片接线或页面重建阶段，参照已生成页面中的同名控件、弹窗、列表、顶栏或导航栈写法时；数据层为新增接口方法复用已有的解析、封装函数时；复用工程已有的共享状态 key 时；按“与 Android 1:1 对齐”修改已有页面（含基线遗留骨架）时

## 适用情境

后写的 worker 同时读到源码与先前 agent 已生成的目标代码片段（@Builder 控件、输入弹窗、弹窗承载方式、列表键函数、顶栏折叠、图标控件行、安全控件样式、全屏遮罩、onReady 取栈写法、共享状态 key、登录结果解析函数等），准备当作项目约定直接沿用。或对齐任务在一个与源端结构不同的既有页面上进行，写者已读到源布局 XML。 也包括后一批执行代理把同批尚未验收的兄弟页（如只回显接口 JSON 的页面）当作模板，照同一模式写出更多页面。也包括 1:1 返修重写已有片段时，沿用目标端已有的尺寸、颜色、限制属性（如三框统一的 maxLength、硬编码字色）或注释里的结论（“源码未设，保真”“已裁定”），以及以仓内同族页面为模板复刻输入行时照搬其图标尺寸与光标色。

## 原因

已有目标代码可能带有尚未暴露的偏差，或依赖原来的输入来源、状态更新、挂载方式与生命周期。把它直接当成项目约定，会让先例覆盖当前已经读到的源端语义，并把同一偏差复制到更多文件。来源中的这些先例尚未经相应运行验证，不能仅凭存在相似写法推断当前场景可用；对齐已有页面时，旧骨架也可能包含源端没有的结构。另一应用的返修会话三次出现同一机制：以同族页面为模板写弹窗输入行，沿用其 24×24 图标和蓝色光标而没解析源 drawable；改写密码页时把只在一个源控件上的 maxLength 写回三个框、把未声明的字色硬编码；把旧注释“组头不可点，保真”当作源端结论继续扩写。

## 做法

1. 沿用前逐个核对片段在源码里对应的行为：参数是否随状态变化、输入约束是否真的阻止显示、条目更新后键是否变化、折叠是否连续、取值来源（响应头还是响应体）是否相同、本页与先例页的挂载方式（压栈还是嵌入容器）是否相同；核对通过再落盘，已有代码不能代替对源码的核对。以同族页面为代码模板时只复用结构和逻辑，复制来的每个尺寸、颜色和修饰符都回到当前源布局逐项核对，源中没有的属性不带入。
2. 已有写法与本处源码不一致时按源码实现，并在报告写明差异，不把近似复制到新文件。
3. 先例本身没有经过运行验证（弹窗打开路径、真机截图）时，不以“先例能用”推断可运行；某处写法被修复后，搜索同一写法的其他页面一并核对。
4. 对齐既有页面时先按源 XML 列组件清单（背景、标题栏、卡片子项、主按钮文案、页签/ViewPager、空态），与现有组件树逐项比对；源端不存在的区块替换，不在旧骨架上只调尺寸。
5. 旧代码注释里的结论（“源码未设/保真/已裁定”）当作待核实的假设，用源码和框架默认行为重新验证后再保留；用 replace_all 或多控件模板批量改写前，确认一并写回的每个属性在每个对应源控件上确实存在。

来源支持：18 张卡 · 9 次迁移 · 9 个应用

## 来源（按需复核）

- [case-1740a4d06903ea105e81](../../../store/cases/case-1740a4d06903ea105e81/cf87962aef2d6207a6d5639da6272767750780198c34ce01489dbaf20cfd70d9.json) · 结论：recommendation:2
  卡片版本：`cf87962aef2d6207a6d5639da6272767750780198c34ce01489dbaf20cfd70d9`
- [case-18113e210e1369d79e1d](../../../store/cases/case-18113e210e1369d79e1d/37c16bc6650280d7876fddb5a21db4abf1271051790070ee84ba091ba04450fb.json) · 结论：recommendation:3
  卡片版本：`37c16bc6650280d7876fddb5a21db4abf1271051790070ee84ba091ba04450fb`
- [case-3045f4019d7d543e18ca](../../../store/cases/case-3045f4019d7d543e18ca/c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451.json) · 结论：diagnosis
  卡片版本：`c70e115876997fe84358e56664eb1d94839a3eaa89da89d4b73b2c4e1a132451`
- [case-31852e28af4327a408a3](../../../store/cases/case-31852e28af4327a408a3/7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b.json) · 结论：diagnosis, recommendation:3
  卡片版本：`7901de8f36fd97f41e540052b94a4d9fdf875fa7e6f69b23452e8f15f8fc467b`
- [case-37ef7d33ab4655385e6f](../../../store/cases/case-37ef7d33ab4655385e6f/fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee.json) · 结论：recommendation:2
  卡片版本：`fdcf6c3cd31bc1665c4c5019cb403126011d55c2fef18000c729355e6c5af9ee`
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
- [case-affc8177e24ce9f71b47](../../../store/cases/case-affc8177e24ce9f71b47/f804b4003f34d058922dd2194e93f12bd78d006541c928c92bb6334c33252bae.json) · 结论：recommendation:3
  卡片版本：`f804b4003f34d058922dd2194e93f12bd78d006541c928c92bb6334c33252bae`
- [case-bd76c218ac0773e443e3](../../../store/cases/case-bd76c218ac0773e443e3/e2da61f6059badfaf173eab73983fdf4e3ad82215573fad87116e60e2727ca7e.json) · 结论：diagnosis, recommendation:1
  卡片版本：`e2da61f6059badfaf173eab73983fdf4e3ad82215573fad87116e60e2727ca7e`
- [case-c4b0a71b1ff405c63013](../../../store/cases/case-c4b0a71b1ff405c63013/cf40af4452211b1663624d236fa85bb538c2147abecce670074002e2a91b17cc.json) · 结论：diagnosis, recommendation:3
  卡片版本：`cf40af4452211b1663624d236fa85bb538c2147abecce670074002e2a91b17cc`
- [case-c9cc6663456a2ef02f89](../../../store/cases/case-c9cc6663456a2ef02f89/ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace.json) · 结论：recommendation:2, recommendation:3
  卡片版本：`ae6747eccb36d26241318b2258e46b0c5b7289bd01e525c168b0fbc5b8ab4ace`
- [case-e3cd92963aa40d922fdc](../../../store/cases/case-e3cd92963aa40d922fdc/9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620.json) · 结论：diagnosis, recommendation:3
  卡片版本：`9788f0e9846113141c74603b6f4b949ae84f08bb07d5f725949650546de97620`
