# 弹窗与弹层

源端有 AlertDialog、DialogFragment、XPopup、BottomSheet、setView 自定义对话框，或者派工、核查清单、弹层矩阵里写到弹窗的承载形态、bindSheet、页面内弹层时

## 触发族

- [源端 AlertDialog 弹窗的核查和比对](alertdialog-parity/index.md)（3 条）：源端用 AlertDialog / AlertDialog.Builder 构造弹窗（含「去设置」跳转、按命中次数多次弹出），路由或弹窗核查清单、共享弹窗的收敛评估、source-notes 差异清单里漏列，或只比了遮罩和按钮顺序、把次数变少写成「可观察等价」
- [先落成简化弹窗的自定义对话框](simplified-dialog/index.md)（1 条）：源对话框用 setView 注入复选框等自定义内容、确认时按复选状态写偏好，交回的代码只剩 message 版 AlertDialog.show，占位登记和移交项里没有丢失的交互
- [弹窗和弹层的承载形态](dialog-hosting/index.md)（5 条）：源端弹窗是 DialogFragment、XPopup 的 CenterPopupView / AttachPopupView / BottomPopup，交接、派工、弹层矩阵或覆盖清单里写成「page-hosted popup/sheet」「页面内弹层」，或按调用 show() 的类记宿主
- [当前页弹出的底部弹窗和半模态](page-sheets/index.md)（2 条）：规格或源码里入口是在当前页 show 的 Dialog / BottomSheet，或同一页面有多个独立弹窗，计划要求「保留 HMRouter 路由和返回栈」，或派工只列 sheet 槽位、没写一组件只挂一个 bindSheet
