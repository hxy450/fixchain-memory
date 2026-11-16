# 安卓上下文菜单（registerForContextMenu / onCreateContextMenu）

agent 会看到什么：读到源端 registerForContextMenu、openContextMenu、onCreateContextMenu（setHeaderTitle、MenuInflater.inflate、MenuItem.setVisible）和菜单 XML 的 <item>；产物里的长按回调、菜单卡浮层、openCustomDialog / openMenu、bindMenu / bindPopup 承载的菜单

## 规矩

- rule-ac6a6dd0ee34｜源列表用 registerForContextMenu 弹上下文菜单时，目标长按打开菜单，不直接进多选｜读到：源列表或 Fragment 调 registerForContextMenu，并实现 onCreateContextMenu / onContextItemSelected，多选只在菜单里某一项被点时开始；写错：目标列表项的长按（LongPressGesture().onAction 或列表组件的长按回调）直接进入多选，注释写「长按进入多选」，全文没有上下文菜单
- rule-82491fd47cbd｜上下文菜单的点击入口做居中模态列表，长按入口用跟随触点的菜单，不用 bindMenu/bindPopup 锚定｜读到：源码 registerForContextMenu(view) 加点击时 openContextMenu(view)，onCreateContextMenu 设 setHeaderTitle / setHeaderIcon；写错：目标只在按钮上挂 .bindMenu(...) 或 .bindPopup(..., { placement: Placement.Bottom }) 锚定下拉，没有长按入口，标题图标丢失
- rule-3936ea621e30｜区段组件承载长按菜单时用 openCustomDialog，不用区段内 Stack 浮层或 bindSheet｜读到：首页区段等嵌入式 Fragment 走 registerForContextMenu / onCreateContextMenu 弹浮动上下文菜单；写错：区段组件 build 尾部插 if (...) Stack{遮罩+菜单卡} 页内浮层，或用 bindSheet 半模态承载菜单，或菜单做成 justifyContent(FlexAlign.End) 贴底面板
- rule-98128235a86c｜openMenu 是 PromptAction 成员，经 getPromptAction() 调用｜读到：源端长按弹出菜单（PopupMenu、showContextMenu）；grep @ohos.arkui.UIContext.d.ts 只看到 openMenu / closeMenu 的声明行；写错：写成 this.getUIContext().openMenu(...) / uiContext.closeMenu(...)，编译报 UIContext 上不存在
- rule-3df86bef9672｜ContextMenu、ActionMode 改写成页内 @Local 浮层时，同步实现返回键先关浮层、退多选｜读到：源端 registerForContextMenu / setOnCreateContextMenuListener + onCreateContextMenu 弹系统 ContextMenu 窗口，或 startActionMode 进入多选；写错：目标把长按菜单写成页面 @Local 状态浮层（遮罩 + 菜单卡）、多选写成一个布尔状态，只靠遮罩点击、菜单动作或清空选中关闭，没有返回键处理；照抄已有页内浮层写法
- rule-80cab2366fa0｜源 onCreateContextMenu 在多选态早返回时，目标长按回调先判多选态再返回｜读到：onCreateContextMenu 第一行判断多选（ActionMode）是否开着，开着就直接 return，不建菜单；写错：目标长按回调（LongPressGesture().onAction 或列表组件的长按回调）只记下条目就打开菜单，多选态下长按照样弹菜单
- rule-63bfca94c257｜源 onCreateContextMenu 调 setHeaderTitle 时，目标菜单卡顶部显示被长按条目的标题｜读到：onCreateContextMenu 里有 menu.setHeaderTitle(...)，参数是被长按条目的标题；写错：目标菜单卡没有标题 Text，或宿主传给菜单卡的标题参数是空串 ''，注释称源端没有 setHeaderTitle
- rule-bc4223887fd0｜源上下文菜单由菜单 XML 膨胀再按判据 setVisible 时，目标按 XML 顺序并调已移植的判据｜读到：onCreateContextMenu 里 MenuInflater.inflate 一份菜单 XML，再调一个按条目状态逐项 MenuItem.setVisible 的判据函数；写错：目标共享菜单组件用自写的 `switch` 定可见项（注释自称简化），条目顺序和源菜单 XML 里 `<item>` 的先后不同
- rule-482f19347685｜菜单 XML 里默认隐藏的项，目标只在源端 setVisible(true) 的宿主里显示｜读到：菜单 XML 的某个 <item> 写了 android:visible="false"，只有某个子类的 onCreateContextMenu 里 setVisible(true)；写错：目标菜单在源端没有这句 setVisible(true) 的宿主（如首页区段）里也渲染了这一项（例如「多选」），点了只收起菜单
- rule-162590a6a13c｜源端局部派生值迁成模型字段时，使用点写成判空后的对象字段，不当组件成员｜读到：源方法里有局部派生值 `boolean 名 = 当前对象 instanceof 某类`，再用它 `setVisible(...)` 控制菜单项；规格的状态接口里没有这个状态；写错：目标在组件里用 `this.` 加源端局部变量名引用它，而组件只声明了可空的 `@Local` 对象，这个值是对象上的字段
