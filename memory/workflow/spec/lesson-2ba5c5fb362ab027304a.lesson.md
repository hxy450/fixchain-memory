# 跨栈映射写“行为等价”前，先核对决定行为的量与目标API是否一致

ID：`lesson-2ba5c5fb362ab027304a` · 版本：1

[本主题](index.md)

## 何时使用

规格提取阶段，编写跨栈映射基线、页面转换决策，或给候选实现标“等价/HARD”时

## 适用情境

源端行为由某个隐含量决定（资源限定符的判档量、绘制单位、帧节奏、Drawable默认填充、窗口方向等），目标端准备用看似相近的机制代替（窗口宽断点、vp单位、固定间隔定时器、Cover、只做响应式布局、未核实的合成模式）。

## 例外与边界

- 当前任务已批准与源端不同的产品行为，并在台账中登记为有意差异

## 原因

“等价”断言会被下游当作权威规约照抄；替代机制只要换了判档量、单位、节奏或填充方式，即使常量照搬，可见行为也会偏离，而下游很少再回到源码复核。

## 做法

1. 每条映射先写出决定源端行为的量及其语义（如sw为设备最短边dp、装载时选定；Android Canvas按物理像素计；无sleep的lockCanvas循环按合成节奏逐帧推进；BitmapDrawable默认FILL；未声明screenOrientation时随传感器转屏），再写目标实现所用的同一个量；两者不同就不能标等价。
2. 候选目标API只写已在本机SDK声明中核实存在的；未核实的标“待查”，并注明每个候选与源语义的差别，不写成HARD。
3. 有多个候选时，把与源语义逐值等价的那条列为首选（如对角ColorMatrix对应逐像素乘法），其余写明会丢失什么。

来源支持：6 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-3db3942c6851402bc500](../../../store/cases/case-3db3942c6851402bc500/251127f8fa91acb01a08f4eeeba1c14342af29fc1a80fd401b2697d8efd65249.json) · 结论：recommendation:1
  卡片版本：`251127f8fa91acb01a08f4eeeba1c14342af29fc1a80fd401b2697d8efd65249`
- [case-3e5c96c55e58edbac2bb](../../../store/cases/case-3e5c96c55e58edbac2bb/6bb50c22a76ee9622c6ab7037de6ac6422508ba90bb0452d903b24846bc9fb9c.json) · 结论：diagnosis, recommendation:1
  卡片版本：`6bb50c22a76ee9622c6ab7037de6ac6422508ba90bb0452d903b24846bc9fb9c`
- [case-4ded9779080f194c96e2](../../../store/cases/case-4ded9779080f194c96e2/2fe8af238707f4e11a9b5ab402f6eba6988194f7e8d5d61864ba4d42d455cc58.json) · 结论：recommendation:1
  卡片版本：`2fe8af238707f4e11a9b5ab402f6eba6988194f7e8d5d61864ba4d42d455cc58`
- [case-54a52d5695dea4698a31](../../../store/cases/case-54a52d5695dea4698a31/4dc5f3295462170d0e4f6d531d425237b4d789eff42d88bdffb7be637b173bbb.json) · 结论：diagnosis, recommendation:1
  卡片版本：`4dc5f3295462170d0e4f6d531d425237b4d789eff42d88bdffb7be637b173bbb`
- [case-a9bc5d0e97c73f878586](../../../store/cases/case-a9bc5d0e97c73f878586/8c43c37fbfb766d31357daa70f317c72c8fa5bf02768ee97119c13ab1d61c3a5.json) · 结论：recommendation:3
  卡片版本：`8c43c37fbfb766d31357daa70f317c72c8fa5bf02768ee97119c13ab1d61c3a5`
- [case-f867226ee0ecc1276ea5](../../../store/cases/case-f867226ee0ecc1276ea5/8ba60ca57800b1dcd11579d6190281db36dee81004d9706279984974c32206c9.json) · 结论：recommendation:4
  卡片版本：`8ba60ca57800b1dcd11579d6190281db36dee81004d9706279984974c32206c9`
