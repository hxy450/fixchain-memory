# wrap_content 的 WebView

agent 会看到什么：读到 android:layout_height="wrap_content" 的 WebView（常在整页 ScrollView 里）；产物里 Scroll 内 Web 的测高（onPageEnd、scrollHeight）和滚动锁定

## 规矩

- rule-f82aded9c3c1｜wrap_content 的 WebView 转 Web 时锁住 H5 滚动，PARENT_FIRST 不能代替｜读到：安卓布局里 WebView 的 android:layout_height="wrap_content"，位于整页 ScrollView 内；写错：Scroll 里的 Web 只写了 .nestedScroll({ scrollForward: NestedScrollMode.PARENT_FIRST, scrollBackward: NestedScrollMode.PARENT_FIRST }) 当作「不自滚」，H5 侧没有锁定滚动（没有注入 overflow:hidden）
- rule-3ffeab0120ce｜用 onPageEnd 加 scrollHeight 给 Web 测高时，安排复测取最大值，不假定图片加载后会再触发｜读到：安卓 WebView 的 android:layout_height="wrap_content"，加载含图片等后续资源的远程 H5；写错：Web 的 .onPageEnd(...) 里只调用一次 runJavaScriptExt 取 scrollHeight 设高度，注释写「随图片加载多次触发自适应」之类
