# 源基类 dispatchTouchEvent 带多项副作用时，目标基类逐项映射，不承接的列为裁剪项

审的是：代码
触发（任一种）：
- 读到：源页面基类重写 dispatchTouchEvent，ACTION_DOWN 分支同时做几件事（刷新触摸时间、触摸计数上报、点外收键盘如 isShouldHideInput / hideKeyBoard）；规格里同一条也列出这些副作用；写错的样子：目标基类写成 dispatchTouchEvent → onTouch() 的对等，onTouch 只承接其中一部分（如两行计数），收键盘等其余副作用既没有映射注释，也没在报告里列为裁剪项
适用范围：把安卓页面基类的 dispatchTouchEvent 等全局触摸行为迁到 ArkTS 页面基类时
做法：
- 按规格把源基类方法的副作用逐项列出，在目标基类的映射注释里一项对一项写明落在哪里（如 onTouch 里 event.type === TouchType.Down 时依次做触摸时间、计数、点外收键盘），不只按「鸿蒙：」映射行实现
- 某项不承接时，在映射注释里写明折叠理由，并在交回报告里列为裁剪项
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onTouch(event: (event: TouchEvent) => void): T：组件的触摸回调，源端 dispatchTouchEvent 的对等承接位置（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onTouch）
- TouchType.Down：手指按下时触发：对应源端 MotionEvent.ACTION_DOWN 分支（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，TouchType.Down）
- 只承接计数时点外收键盘被静默丢掉，判别器报告无承接：漏项的后果（出处：卡里修好并验证过）
针对本应用要查的：
- 源基类方法的全部副作用：规格里该基类的那一条，以及源工程基类 Java/Kotlin 里 dispatchTouchEvent 的完整方法体；逐行列出每个副作用（含调用的工具方法），逐项在目标基类里对应或写折叠理由
未核实：卡里观察到的行为出自鸿蒙 SDK API 24/21，本机核实用 API 23；卡里观察截止时目标的收键盘链还没在运行时触发，收键盘的目标写法未验证
来源：1 张卡，1 个应用
- case-104a365629bd48069967（DeepAI全能PPT）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 3 ← 诊断
