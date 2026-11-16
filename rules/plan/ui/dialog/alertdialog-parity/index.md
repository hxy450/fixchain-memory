# 源端 AlertDialog 弹窗的核查和比对

agent 会看到什么：源端用 AlertDialog / AlertDialog.Builder 构造弹窗（含「去设置」跳转、按命中次数多次弹出），路由或弹窗核查清单、共享弹窗的收敛评估、source-notes 差异清单里漏列，或只比了遮罩和按钮顺序、把次数变少写成「可观察等价」

## 规矩

- rule-9be22674c4ee｜路由或弹窗核查清单缺源端 AlertDialog.Builder 弹窗时，回源文件补查并补进清单｜读到：源控制器里有 AlertDialog.Builder 构造的弹窗、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 跳转，或多个失败分支各有不同 UI；写错：路由核查清单、fix-plan 只列了 MessageDialog.show、startActivity 抽出来的边（失败弹窗、登录跳转），AlertDialog.Builder 构造的弹窗和它的“去设置”跳转不在清单里
- rule-30bc213c3e49｜共享弹窗晚于页面就绪时，收敛评估要按源端平台外观逐项比对，不只比遮罩和按钮顺序｜读到：占位登记里有一项「页内弹窗改用共享平台对话框件」，共享件晚于页面就绪；写错：评估只写「与共享件行为一致」「更贴源」就保留页内实现，比的只是遮罩、按钮顺序，没有逐项比对源端平台外观
- rule-9d3148c08db5｜目标偏离源端可观察行为时，按次数核对等价性，要偏离就写进 decision_gaps 或决策台账待批｜读到：源码里弹窗、回调或副作用按命中次数发生多次；写错：source-notes 差异清单或代码注释写「收敛」「幂等」「罕见路径」「可观察等价（用户只见前窗）」，目标触发次数少于源端；handback 的 decision_gaps 为空，决策台账里没有这一项
