# 自绘弹窗的打开、关闭和触摸穿透

agent 会看到什么：读到 setCancelable / setCanceledOnTouchOutside、循环里逐个 show 的模态窗或会重建的 Activity；产物里遮罩的 onClick 和 HitTestMode.Block、ComponentContent 的关闭回调、方向变化时的关闭路径，以及一次开几个弹窗

## 规矩

- rule-771d45826594｜页内遮罩复刻可点外取消的源对话框时，遮罩 onClick 关闭最上层，与返回键共用取消处理｜读到：源端 AlertDialog.Builder 没调用 setCanceledOnTouchOutside(false) 或 setCancelable(false)；写错：遮罩层 .hitTestBehavior(HitTestMode.Block) 加空 onClick 吞掉点击，注释写「源 AlertDialog 模态语义——外触不 dismiss」；宿主页没有点外部关闭
- rule-938fc528dd3d｜弹窗内容面板包着可点子控件时不用 HitTestMode.Block，防穿透只放在无子控件的遮罩上｜写错：弹窗或底部面板的内容 Column、根 Stack 上写 .hitTestBehavior(HitTestMode.Block)，里面有 Button、Checkbox、列表项等要点击的子控件
- rule-e9baf2addd75｜页内浮层改成 DialogHelper 真弹窗后，删掉全部自绘遮罩和 Block 防穿透写法｜写错：改成 DialogHelper.showCustomDialog / showBindSheet 后，弹窗内容根仍有 .hitTestBehavior(HitTestMode.Block)，或根 Stack 还留着 visible ? HitTestMode.Block : HitTestMode.None
- rule-bc80b3db9e3d｜ComponentContent 构造后才赋值的回调，builder 里写成箭头函数在点击时取值｜读到：源端 DialogFragment / MaterialAlertDialogBuilder 的 setPositiveButton、setNegativeButton 点击后关闭或确认弹窗；写错：builder 里写 onClose: args.onClose 这类把 args 回调字段直接交给内容组件 @Param 的写法，而该字段在 new ComponentContent(...) 之后才赋值（典型是 args.onClose = () => closeCustomDialog(content)），args 类里的默认值是 no-op
- rule-4b2f0b4b880e｜页内浮层承载源端非托管对话框、源 Activity 会重建时，补横竖翻转的关闭路径｜读到：源 Activity 没有 android:configChanges 也没有 screenOrientation 锁定，对话框用 AlertDialog.Builder(...).show() 直接弹出；写错：目标端用 @Local / @State 布尔量驱动的页内浮层，只在 Back、遮罩、返回键和 aboutToDisappear 时关闭，没有方向或配置变化的关闭路径
- rule-341a32d16119｜源端在循环里对每个命中元素各弹一个模态窗时，目标用计数信号叠放弹窗，确认只关最上面一个｜读到：判定方法只在循环外检查一次防重标志，双层 `for` 循环不 `break`，每个命中元素都先落盘统计再 `new AlertDialog.Builder(…).setCancelable(false).create().show()`；写错：引擎的 pending 信号是 `boolean`，consume 方法返回 `boolean`；页面用一个 `@Local` 布尔只渲染一个弹窗，确认、取消都直接置 `false`；注释写「幂等收敛为单窗」「罕见路径」
- rule-e0e67dc08492｜openCustomDialog 承载点外取消时，起于框内可消费控件的 TOUCH_OUTSIDE 不关闭｜读到：规格写「点外取消」，或源端 Dialog / AlertDialog 没调 setCanceledOnTouchOutside(false)，对话框里有按钮、列表、输入框或可滚动正文；写错：openCustomDialog 只靠 autoCancel: true（或默认值）、不设 onWillDismiss；或 onWillDismiss 里对 DismissReason.TOUCH_OUTSIDE 无条件 action.dismiss()
- rule-c71a9d866323｜共享弹层组件只有遮罩点击关闭时，注释写明宿主须在 onBackPressed 关闭它｜读到：要复用的共享弹层组件只提供遮罩点击的 onDismiss 回调，靠宿主页的 Stack 承载；写错：共享弹层组件的注释和接口没写「宿主页须在 onBackPressed 关闭本弹层」；复用它的页面 NavDestination 上没有 .onBackPressed
