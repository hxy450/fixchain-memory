# 子组件内部创建的 ViewModel 和页面的注入点

agent 会看到什么：读到占位登记或派工要求页面给覆盖层、子组件的 ViewModel 注入数据源，而这个 VM 由子组件在内部 new 出来；产物里页面只写 Overlay({ … }) 一类构造，子组件没有 @Param / @Event 回调把内部 VM 交给页面

## 规矩

- rule-1cfa3f6d8d02｜注入点在子组件内部创建的 VM 上时，子组件加回调参数把 VM 交给页面｜读到：占位登记要求页面给覆盖层的 ViewModel 注入数据源（捕获结果读面、振幅源），而 VM 由子组件在内部 new 出来；写错：页面只写 Overlay({ engine }) 这类构造，子组件 aboutToAppear 里只登记别的 sink，没有把内部 VM 交出去的回调，页面够不着注入点
