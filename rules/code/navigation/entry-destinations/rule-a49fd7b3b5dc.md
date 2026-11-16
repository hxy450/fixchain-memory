# 接入已有专页时逐项实现它的 @Event 回调契约，要回传结果的不用空值短路

审的是：代码
触发（任一种）：
- 读到：已有 ArkTS 子页声明了 @Event 回调，参数里带回传函数（如 onReady: (id: string) => void），子页只有拿到非空结果才 pushPathByName 进入下一页；写错的样子：容器实现这个回调时改调别的处理再回传空值（onReady('')），或不调用回传函数，子页自带的导航被跳过
适用范围：把源端 Fragment 对应的现有 ArkTS 子页接入父容器、实现子页 @Event 回调时
做法：
- 回调要求回传会话或结果时，要么给出真实值（onReady(realId)），要么新增一个 @Event 交父页分派，由能拿到数据的父页回传；不用空值短路子页自带的导航
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- @Event 没有初始化时自动生成一个空函数作为默认回调：父容器漏接或乱接回调时不会报错，只是行为静默不对（出处：arkts-new-event.md，概述）
- @Event 允许装饰回调方法，参数和返回值由开发者决定，只能用在 @ComponentV2 组件里：回传函数作为回调参数是子页自定的契约，要按它的参数逐项实现（出处：arkts-new-event.md，装饰器说明 / 限制条件）
- pushPathByName(name: string, param: unknown, animated?: boolean): void：子页拿到结果后自己入栈下一页（出处：鸿蒙 SDK 的 ets/component/navigation.d.ts，NavPathStack.pushPathByName）
- 回调里改调图片选择并回传空会话时子页不再进入编辑页；改成新事件交父页分派后恢复编辑路由：验证过的接法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-39f4dfac164861b33e83（组件岛Widget Island）：做法第 1 步 ← 建议 1、诊断；取值 4 ← 诊断
