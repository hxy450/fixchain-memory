# 异步数据回来后调 controller.loadData 时，以 onControllerAttached 置位为前提

审的是：代码
触发（任一种）：
- 读到：源端在数据加载完成的回调里直接调 `webView.loadDataWithBaseURL(...)`；写错的样子：目标在异步数据回来后直接调 controller.loadData(...)，Web 上没有 .onControllerAttached(...) 置位守卫，默认「异步加载足够慢、controller 已挂接」
适用范围：Web 组件的正文由异步数据（数据库、网络）产出、再用 WebviewController 装载时
做法：
- Web 上写 .onControllerAttached(() => { this.controllerAttached = true; 有缓存的数据就补发一次 loadData })
- 数据回来时未挂接就只缓存，已挂接才 loadData；用一个已装载标记保证挂接后只装载一次
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- onControllerAttached(callback: () => void): WebAttribute：WebviewController 绑定到 Web 后回调；回调前调用 Web 相关接口会抛 js-error（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.onControllerAttached）
- loadData 未挂接时抛 BusinessError 17100001（The WebviewController must be associated with a Web component.）：不加守卫时的失败方式（出处：鸿蒙 SDK 的 ets/api/@ohos.web.webview.d.ts，WebviewController.loadData）
- controllerAttached / 已装载两个标记，挂接后只装载一次：修好后的守卫（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-60d268b503cb75aa01a2（AntennaPod）：做法第 1 步 ← 建议 2、诊断；做法第 2 步 ← 建议 2、诊断；取值 3 ← 诊断
