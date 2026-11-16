# 锚定父页控件的 AttachPopupView 提示

agent 会看到什么：源端继承 AttachPopupView、用 atView(...) 锚定 parentFragment 控件的提示弹窗（弹出前判断 isShown 和一次性标记，onDismiss 里写标记），对应目标提示浮层放在哪一页、怎么定位、显示条件和子页怎么读它

## 规矩

- rule-d91eb27f0d87｜源端 AttachPopupView 锚定父页控件时，目标提示挂在锚点所在页并按锚点实测位置定箭头｜读到：弹窗类继承 `AttachPopupView`，调用方用 atView(...) 传入的锚点视图取自 parentFragment，箭头边距按锚点宽度计算；写错：目标的提示浮层写在子页组件的 build() 里，用写死的 right/top 数值（.position / .margin）定位，和锚点组件的位置无关
- rule-230072b2e354｜源端弹窗要求锚点 isShown 且一次性标记未写时，目标照搬两个条件并持久化标记｜读到：弹出前判断锚点 `isShown` 和一次性「已显示」标记，弹窗的 onDismiss 里写入这个标记；写错：目标只用页面里的 `@State` 布尔量控制提示显隐，关闭时不写持久化存储；或者显示条件里缺了锚点可见这一项
- rule-7e38f30a1157｜子页逻辑依赖父页提示是否显示时，经参数或回调读父页状态，不用子页私有副本｜读到：提示由父页的锚点控件承载（atView 取自 parentFragment），子 Fragment 里另有逻辑在提示显示时跳过（如显示时不计数）；写错：子页组件里自建一个表示提示是否显示的私有 `@State` 布尔量，别的逻辑以它作 if (…) return 守卫
