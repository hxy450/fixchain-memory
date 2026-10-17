# 复用开关组件的变更事件给出目标值时，把它原样写入该开关的 setter，不改成无参回调再按旧值取反

ID：`lesson-40fc63b124b4a44e7a9f` · 版本：2 · 阶段：execute · 主题：[ui/state/binding](index.md)

概要：开关事件目标值直传 setter，不用 toggle 取反

信号：`onToggleChange`, `isOn`, `@Event`, `@Param`, `@Local`, `Toggle`

## 何时使用

界面接线阶段，把开关行接入带 @Param isOn 与 @Event onToggleChange(nextState) 的复用组件，并连到 ViewModel 的开关接口时

## 适用情境

源端每个开关点击时翻转自身字段、写偏好并刷新自身图标；目标复用组件在事件里给出下一状态，ViewModel 提供 toggleX() 取反接口，页面本地 @Local 与 ViewModel 各持一份开关值。

## 原因

取反依赖执行时刻的旧值；页面副本、ViewModel 字段与持久化各有一份值，回调又经共享模板转发时，被取反的可能是过期值或另一行的值，结果与用户点击相反或写到别的开关。来源中接线者把组件回调写成无参闭包，丢弃组件给出的目标值，改由 ViewModel 的取反接口决定；随后蓝牙页两个开关出现互相影响，修复改为显式 setter 接收目标值并回读持久化。

## 做法

1. 组件事件给出的目标值原样传给对应 setter（如 setX(enabled)），页面本地状态与持久化都用这个值；ViewModel 需要时新增显式 setter，不让页面经 toggle 取反。
2. 替换源端整行可点的实现时，保留点击热区与无障碍分组，不把热区缩到图标。

## 同源经验

由相同来源卡提炼的其他经验，按共享卡数排序；不是依赖关系。

- [必读 skill 与源码逐份读全，截断即重读再写码](../../../process/unloaded-input/lesson-42df1ac4d4030421da34.lesson.md)（共享 1 张卡）
- [状态派生值不传 @Builder，改 @Param 子组件](lesson-8d2979542fa2cd65150c.lesson.md)（共享 1 张卡）

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-ab54d746c8c33d3061ed](../../../../../store/cases/case-ab54d746c8c33d3061ed/d96e14c620706554d7f6a91e22c83b058f5f89196e5be3140058b38c7b28a017.json) · 结论：diagnosis, rec-4752a7824f
  卡片版本：`d96e14c620706554d7f6a91e22c83b058f5f89196e5be3140058b38c7b28a017`
