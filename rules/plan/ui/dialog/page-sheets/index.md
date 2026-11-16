# 当前页弹出的底部弹窗和半模态

agent 会看到什么：规格或源码里入口是在当前页 show 的 Dialog / BottomSheet，或同一页面有多个独立弹窗，计划要求「保留 HMRouter 路由和返回栈」，或派工只列 sheet 槽位、没写一组件只挂一个 bindSheet

## 规矩

- rule-b32305ddbf48｜源端是当前页弹窗时，计划任务不写「保留 HMRouter 路由和返回栈」｜读到：规格或源码说明入口是在当前页 show 的底部弹窗（Dialog / BottomSheet）；写错：计划任务要求「保留 HMRouter 路由和返回栈」，或者让宿主带参数 push 一个路由页来打开这个面板
- rule-cb71200a09e5｜派工让一个页面承载多个半模态弹层时，写明一组件只挂一个 bindSheet、各用零尺寸锚点｜读到：规格把同一页面的多个弹窗列为各自独立的弹出目标；写错：派工只列 sheet 槽位（如「某某 Sheet + 某某 Dialog 槽位留给后续切片」），没有写「一组件只能有效挂一个 bindSheet，每个 sheet 挂独立零尺寸锚点」这条约束
