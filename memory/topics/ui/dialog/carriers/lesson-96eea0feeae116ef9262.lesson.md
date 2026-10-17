# 页内遮罩承载源端对话框时，显示期间把背景内容移出无障碍树：accessibilityLevel('no-hide-descendants')

ID：`lesson-96eea0feeae116ef9262` · 版本：2 · 阶段：execute · 主题：[ui/dialog/carriers](index.md)

概要：页内遮罩弹窗显示时背景移出无障碍树

信号：`accessibilityLevel`, `no-hide-descendants`, `openCustomDialog`, `showAlertDialog`, `@CustomDialog`, `bindSheet`, `Stack`

## 何时使用

界面实现阶段，为源端独立窗口对话框选择承载方式，或按项目已有写法用页内 Stack 遮罩加卡片实现对话框时

## 适用情境

源端对话框是独立窗口（Compose Dialog/AlertDialog、Android Dialog），读屏焦点限制在对话框内；目标以可见性状态在页面根 Stack 中条件渲染遮罩与卡片，背景页面仍在同一组件树；规格或共享弹窗组件头注可能已指定 openCustomDialog、@CustomDialog 等系统通道，兄弟页已有同款页内遮罩可参照。

## 例外与边界

- 使用 openCustomDialog、showAlertDialog、bindSheet 等系统弹窗通道：窗口级模态由系统提供

## 原因

遮罩只拦截点击，不改变无障碍树；页内弹层显示时，读屏仍能遍历并激活背景页面的控件，源端对话框的窗口模态丢失。因“更简单、可控”改走页内遮罩，或照兄弟页先例沿用时，这一差异最容易被漏掉。

## 做法

1. 源对话框为独立窗口时，按规格与共享组件约定使用系统弹窗通道。
2. 确需页内遮罩时，给背景内容的根节点设 .accessibilityLevel(弹层可见 ? 'no-hide-descendants' : 'auto')，弹层自身保持可访问；同页有多个页内弹层时按任一可见计算，并同时交付返回键关闭。
3. 偏离规格映射时在实现报告中说明，不把规格表改写成实际实现。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [真弹窗迁成系统弹窗或半模态，不用可见性叠层充当](lesson-368c4592e4c7075c1871.lesson.md)（共享 1 张卡）
- [可点击行卡转写 role、enabled 与朗读合并](../../accessibility/lesson-5caf7eadb69e940926f9.lesson.md)（共享 1 张卡）
- [规格与源码冲突按源实现，例外只认决策 ID](../../../process/secondary-over-source/lesson-7a065e8fe384b8c462cc.lesson.md)（共享 1 张卡）
- [无障碍文本按源描述用 $r，空不臆造](../../accessibility/lesson-d80ced7be82765244889.lesson.md)（共享 1 张卡）
- [沿用已生成页面或兄弟写法前回源码核对语义](../../../process/secondary-over-source/lesson-e9c6e8ef1b29a6fe9c26.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-8dd5c1f1f269d142cc22](../../../../../store/cases/case-8dd5c1f1f269d142cc22/20e8fe0eb12d923dd2187f8efe7cbc824971502cc6456d7985b1f26b5e5e94d9.json) · 结论：diagnosis, rec-bf9d522807
  卡片版本：`20e8fe0eb12d923dd2187f8efe7cbc824971502cc6456d7985b1f26b5e5e94d9`
