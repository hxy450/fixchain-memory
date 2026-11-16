# Swiper/Tabs 预构建子页的原生地图不在 onReady 创建，隐藏时暂停、卸载才释放

审的是：代码
触发（任一种）：
- 读到：页面除路由外还在宿主的 Swiper / Tabs 子页里被直接实例化（一次性预构建）；参考桥接把 MapView.onResume、MapView.onPause 和 MapView.onDestroy 分成激活、暂停、释放三个接口；写错的样子：在 NavDestination 的 .onReady(…) 或 aboutToAppear 里创建原生地图；在 .onDisAppear(…) 里调完整释放（MapView.onDestroy），从不调用暂停/恢复
适用范围：把原生地图接入可能被 Swiper / Tabs 预构建的已有页面时，地图的初始化、暂停、释放挂在哪个回调上
做法：
- 先查页面在哪被实例化；在 Swiper / Tabs 等预构建容器里时，地图初始化挂到页面实际可见时（卡里保留的写法是 .onAppear(...)），不放 NavDestination.onReady / aboutToAppear
- 页面隐藏时调暂停（对应 MapView.onPause），回来时恢复（MapView.onResume）；完整释放（MapView.onDestroy）只在真正卸载时调用
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onReady(callback: Callback<NavDestinationContext>): NavDestinationAttribute：在 NavDestination 将要构建子组件时回调，这时地图组件还没创建（出处：鸿蒙 SDK 的 ets/component/nav_destination.d.ts，NavDestinationAttribute.onReady）
- onAppear(event: () => void): T：组件挂载显示时触发（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onAppear）
- onDisAppear(event: () => void): T：组件卸载消失时触发（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.onDisAppear）
- 地图初始化和首次定位放 .onAppear(...)；.onDisAppear(...) 改调暂停（桥接的 deactivate → MapView.onPause），不再销毁仍挂载的原生组件：卡里最终保留的可见性驱动写法（出处：卡里修好并验证过）
针对本应用要查的：
- 页面是不是被预构建：目标工程里搜这个页面组件名被实例化的地方（宿主页的 build），看是否在 Swiper / Tabs 的子项里；在 Swiper / Tabs 里就按预构建子页处理：隐藏的页面启动时也会构建
未核实：Swiper / Tabs 一次性构建的子页里，onAppear / onDisAppear 是否随切页触发，卡里没核实；高德鸿蒙 SDK 里 MapView 的 onResume / onPause / onDestroy 语义按卡写，三类来源里查不到
来源：1 张卡，1 个应用
- case-31b1116c0e0aec40a307（android-panorama-map-vest7）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2；取值 4 ← 诊断
