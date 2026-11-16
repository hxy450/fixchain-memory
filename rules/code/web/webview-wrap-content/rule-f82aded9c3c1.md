# wrap_content 的 WebView 转 Web 时锁住 H5 滚动，PARENT_FIRST 不能代替

审的是：代码
触发（任一种）：
- 读到：安卓布局里 WebView 的 android:layout_height="wrap_content"，位于整页 ScrollView 内；写错的样子：Scroll 里的 Web 只写了 .nestedScroll({ scrollForward: NestedScrollMode.PARENT_FIRST, scrollBackward: NestedScrollMode.PARENT_FIRST }) 当作「不自滚」，H5 侧没有锁定滚动（没有注入 overflow:hidden）
适用范围：把整页滚动容器内高度随内容的 WebView 迁成 Scroll 包裹的 ArkWeb Web 时
做法：
- 「高度等于内容」和「Web 自身不滚」分两条实现：高度用 controller.runJavaScriptExt 取 document 的 scrollHeight 设给 Web 的 height；不自滚在 H5 侧锁定
- 测高前先注入锁滚动脚本：controller.runJavaScriptExt("document.documentElement.style.overflow='hidden';document.body.style.overflow='hidden';")，再测高；nestedScroll(PARENT_FIRST) 只调先后，留着也不能代替这一步
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 对 html、body 设 overflow:hidden 后，页底 Web 区域不再单独内滚，滑动带动整页：锁滚动的写法（出处：卡里修好并验证过）
- NestedScrollMode.PARENT_FIRST：Parent scrollable component priority response scrolling：只定父容器先滚；外层到边界后 Web 仍会自己滚（出处：鸿蒙 SDK 的 ets/component/enums.d.ts，NestedScrollMode.PARENT_FIRST）
- nestedScroll(value: NestedScrollOptions | NestedScrollOptionsExt): WebAttribute，不写时各方向默认 NestedScrollMode.SELF_FIRST：Web 的嵌套滚动设置（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.nestedScroll）
- runJavaScriptExt(script: string | ArrayBuffer): Promise<JsMessageExt>：注入锁滚动脚本、取 scrollHeight 用的接口（出处：鸿蒙 SDK 的 ets/api/@ohos.web.webview.d.ts，WebviewController.runJavaScriptExt）
- nestedScroll(value: NestedScrollOptions): ScrollAttribute：同族接口：Scroll 的嵌套滚动设置（出处：鸿蒙 SDK 的 ets/component/scroll.d.ts，ScrollAttribute.nestedScroll）
- nestedScroll(value: NestedScrollOptions): ListAttribute：同族接口：List 的嵌套滚动设置（出处：鸿蒙 SDK 的 ets/component/list.d.ts，ListAttribute.nestedScroll）
未核实：卡里上机所用 SDK 是 API 22（6.0.2），声明按本机 API 23 核实
来源：1 张卡，1 个应用
- case-a5865fd3dc0a3f9a028e（企业安全培训）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1、诊断；取值 1 ← 诊断
