# 子页只写共享回传通道时，来源页在 NavDestination.onShown 里读取，不只在 onPop 里读

审的是：代码
触发（任一种）：
- 读到：子页成功后只把结果写进共享回传通道（AppStorageV2 槽位、单例一类，无回调无事件），再 pop()；写错的样子：来源页只在 pushPathByName(..., onPop) 的回调里读共享通道，NavDestination 上没有 .onShown(...) 读取
适用范围：回传走共享通道（生产端写、消费端读）而不是 pop(result) 时的消费端
做法：
- 来源页在 NavDestination(...).onShown(...) 里读并消费共享通道；要在 onPop 回调里读，就必须让生产端改成 pop(result)
- 收尾统一两条回传轨时，生产端出栈调用和消费端触发点一起核对、一起改
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onShown(callback: Callback<VisibilityChangeReason>): NavDestinationAttribute：NavDestination 页面显示时回调，回到来源页时会走到（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onShown）
- 生产端保持写通道的同时改成 pop(结果实例)，来源页另在 NavDestination.onShown 兜底消费后，回传恢复：修好后的组合（出处：卡里修好并验证过）
- onPop 仅在 pop、popToName、popToIndex 设置了 result 参数后触发：放在 onPop 里的通道读取，生产端裸 pop() 时不会执行（出处：ts-basic-components-navigation.md，pushPathByName11+）
未核实：onShown 的 Callback<VisibilityChangeReason> 签名标 @since 21，更早版本是无参回调；卡里的行为出自 HarmonyOS 6.1.1(24)
来源：1 张卡，1 个应用
- case-60576c483fb94367a81b（jerboa）：做法第 1 步 ← 建议 1、建议 3；做法第 2 步 ← 建议 3；取值 2 ← 诊断
