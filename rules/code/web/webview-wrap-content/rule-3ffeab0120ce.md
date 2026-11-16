# 用 onPageEnd 加 scrollHeight 给 Web 测高时，安排复测取最大值，不假定图片加载后会再触发

审的是：代码
触发（任一种）：
- 读到：安卓 WebView 的 android:layout_height="wrap_content"，加载含图片等后续资源的远程 H5；写错的样子：Web 的 .onPageEnd(...) 里只调用一次 runJavaScriptExt 取 scrollHeight 设高度，注释写「随图片加载多次触发自适应」之类
适用范围：按网页文档高度设置 ArkWeb Web 组件高度时
做法：
- 不假定图片等子资源加载后会再次触发 onPageEnd；写「多次自适应」一类注释前先核对事件语义
- 为后加载的内容安排复测：onPageEnd 后先注入锁滚动脚本，再在 0 / 1000 / 2500 ms 各取一次 scrollHeight，取最大值更新 Web 高度
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 在 0 / 1000 / 2500 ms 复测并取最大值后，图片晚到时高度也跟上：复测的时机（出处：卡里修好并验证过）
- onPageEnd(callback: Callback<OnPageEndEvent>): WebAttribute，网页加载完成时触发，只在主 frame 触发：只是一次加载结束的回调，不随子资源加载重复触发（出处：鸿蒙 SDK 的 ets/component/web.d.ts，WebAttribute.onPageEnd；arkts-basic-components-web-events.md，onPageEnd）
- runJavaScriptExt(script: string | ArrayBuffer): Promise<JsMessageExt>：取 scrollHeight 用的接口（出处：鸿蒙 SDK 的 ets/api/@ohos.web.webview.d.ts，WebviewController.runJavaScriptExt）
未核实：单次测高偏矮的时序（图片在 onPageEnd 之后加载）卡里没有复现；卡里上机所用 SDK 是 API 22（6.0.2）
来源：1 张卡，1 个应用
- case-a5865fd3dc0a3f9a028e（企业安全培训）：做法第 1 步 ← 建议 2；做法第 2 步 ← 建议 2、诊断；取值 1 ← 诊断
