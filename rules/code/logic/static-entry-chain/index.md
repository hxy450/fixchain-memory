# 工具类静态入口起的业务链

agent 会看到什么：读到工具类静态方法或 companion object 直接起链（先弹 loading 的 Dialog、下载、导出文件）；产物里 static 入口的签名带没带 context 和回调，直调入口有没有真的调用服务并在终态收口

## 规矩

- rule-6fa67f8a7a5f｜静态入口或全局状态单例要调需要 UI context 的服务时，在入口签名里显式注入 context 和回调｜读到：目标服务方法需要 Context 参数（如用 new picker.DocumentViewPicker(context) 导出文件），源端是工具类静态方法直接起链；写错：static 入口方法的签名里没有 context: Context、toast、结果回调参数，只能改状态；服务调用只写在组件按钮的 onClick 回调里（只有那里拿得到 context）
- rule-d1ad1b85f592｜同一业务链有弹窗确认和无弹窗直调两个入口时，每个入口都要起链调服务并在终态收口｜读到：源端工具方法在回调里先显示 loading 的 Dialog，随即直接下载并设置，fail / cancel / success 各分支都关闭这个 Dialog，中间没有选择弹窗；写错：目标的直调入口方法只置 busy = true、visible = true，服务调用和收口（busy = false）只写在弹窗「确定」的 onConfirm 里；注释却写着「直接调用」「busy 态起链」
