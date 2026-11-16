# 刷新时被重建的列表内容

agent 会看到什么：产物里 ForEach / Repeat 的键拼了请求序号、加载状态等易变字段，条目模型是整体替换的普通 interface，或 if (加载中) 把内容整块换成 LoadingProgress，翻页、切换时内容被销毁重建

## 规矩

- rule-bbf47d9cee08｜ForEach 的键里拼了请求序号、加载状态等易变字段时，键只用数据的查询键｜写错：ForEach(arr, itemGenerator, keyGenerator) 的 keyGenerator 返回值里拼了请求序号、加载状态、事件列表这类每次请求都会变的字段，翻页或切换时页面反复销毁重建、抖动
- rule-722ee8c700a7｜稳定 ForEach/Repeat 的 key 时，条目模型改成 @ObservedV2/@Trace 并原位更新｜读到：ForEach / Repeat 的 key 里拼了请求状态或数据（如 requestId、loadState、条目内容），条目模型是普通 interface，更新时用新对象整体替换数组项；写错：key 改成只含稳定标识后，模型仍是普通 interface、仍整体替换；子组件以 @Param 接普通对象，或把 RepeatItem.item 解包后往下传
- rule-459e1386706c｜本地查询期间用 if 把内容整块换成 LoadingProgress 时，去掉这层加载遮罩｜写错：页面写成 if (加载中) { LoadingProgress() } else { 内容 }，每次本地查询（翻页、切换模式）都切到 LoadingProgress 分支，内容子树被移除再重建
