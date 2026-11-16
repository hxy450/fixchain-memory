# Stack 上叠加的覆盖层和全屏遮罩

agent 会看到什么：读到参考实现里原生地图 XComponent 铺在最底层、上面叠 ArkUI 控件，或同仓页面在无 padding 的根 Stack 里条件渲染全屏遮罩，产物里是覆盖层有没有 .hitTestBehavior(...)，以及挂在带 padding 容器上的 .overlay(...)

## 规矩

- rule-8c68e452c647｜原生地图上叠 ArkUI 控件时写明触摸分工，纯视觉层设 HitTestMode.None｜读到：参考实现里 MapViewComponent（或其他原生 XComponent 地图）100% 宽高放在最底层，上面叠搜索栏、按钮等 ArkUI 覆盖层；参考的承载页用 HitTestMode.Transparent / HitTestMode.None 划分地图和控件的触摸；写错：地图组件和覆盖层容器都没写 .hitTestBehavior(…)，覆盖层控件点不动
- rule-9a428149529e｜页面全屏遮罩用无 padding 根 Stack 的条件子节点，不在带 padding 的容器上 .overlay()｜读到：同仓已有页面在 NavDestination 下无 padding 的根 Stack 里用 if (…) 条件子节点铺全屏遮罩（保存中 loading、成功引导）；当前页根容器是带安全区 padding 的 Column；写错：在带 padding 的根 Column 上写 .overlay(this.xxxOverlay())，builder 里 if (…) 条件渲染遮罩；遮罩底部 padding 带不变暗，遮罩上的 SaveButton 点击日志是 Touch test result is empty
- rule-4612ac15c754｜源端只在播放时 addView 全屏覆盖层、播完移除时，目标用 if 条件挂载，不常驻｜读到：源端动效在触发时才 decorView / rootView.addView(overlay, MATCH_PARENT)，结束回调和取消时 removeView 移除，overlay 设 isClickable = false；写错：目标把全屏覆盖组件无条件挂在页面、弹层或 Sheet 上（.width('100%').height('100%').zIndex(...)），空闲时只 clearRect，只靠内部 Canvas 的 .hitTestBehavior(HitTestMode.None) 让出点击
- rule-11e46355518f｜接入或替换共享组件时保留挂载点的 hitTestBehavior，实例带通用属性就写 Transparent｜读到：原挂载点写着 .width('100%').height('100%').zIndex(...).hitTestBehavior(HitTestMode.None)，组件头注释称组件自身不拦截；写错：换装后删掉了挂载点的 .hitTestBehavior(...)，实例上仍保留 width / height / zIndex 等通用属性
- rule-f1f86a6b4342｜共享组件的层契约不声称自身不拦截，写明挂载实例上写 Transparent｜读到：源端 KonfettiView 这类一次性动效层不处理指针输入，叠在可点击内容之上；写错：自定义组件只在 build 根节点（如 Canvas）写 .hitTestBehavior(HitTestMode.Transparent)，头注释写成「组件根节点 Transparent，遮不住底层」
- rule-3e2e95f16d6f｜用共享组件替换页内浮层片段时核对层叠关系，改了面板挂载方式要重核宿主的全尺寸层｜读到：被替换的页内片段是 Stack 里全幅透明捕获层后接面板的 @Builder 调用，注释写「面板 z 序居上」；写错：接线时删掉面板调用、保留后声明的全幅捕获层，注释改成「浮层本体由组件 overlay 渲染」；组件里的面板已改挂 .overlay()，与宿主捕获层重叠
- rule-81e234382738｜Stack 里盖在可点内容上的全尺寸浮层容器按开合写 hitTestBehavior，关闭态 Transparent｜读到：Compose 的 ModalNavigationDrawer(drawerState)：关闭态下内容照常可交互，打开时由遮罩拦截；写错：Stack 里 width('100%').height('100%') 的抽屉浮层容器没写 hitTestBehavior（缺省 Default），只给里面的唤起条或旁边的 Snackbar 宿主层写了 HitTestMode.Transparent
