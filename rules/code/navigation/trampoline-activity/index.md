# 开头即跳走的跳板 Activity

agent 会看到什么：读到 Activity 的 onCreate / initView 开头不经操作就 startActivity 到别的页并 finish()，或调用方 Intent 指向这种 Activity；产物里把它渲染成可停留的页、跳转放进按钮 onClick，或 pushPathByName 到它对应的页

## 规矩

- rule-ccf2e5743462｜Activity 开头无条件跳走并 finish() 的按跳板转，鸿蒙页进入即替换到实际目标｜读到：Activity 的 onCreate 或 initView 开头不经用户操作就 startActivity(Intent(...)) 到别的页并紧接 finish()（可按条件分几支，每支都跳走），它的布局 XML 里仍有按钮等可渲染控件；写错：对应的鸿蒙页照布局渲染成可停留的页面，跳转放进按钮的 onClick 里才调用 replacePathByName / pushPathByName
- rule-fb198f363c3d｜调用方 Intent 指向开头即跳走的 Activity 时，鸿蒙路由直接指向用户实际看到的首屏页｜读到：调用方 startActivity(Intent(context, X::class.java))，而 X 的 onCreate 或 initView 开头无条件 startActivity 到别的页并 finish()；写错：调用方的鸿蒙代码按 Activity→Page 的名称映射写成 pushPathByName 到 X 对应的页，没有复核 X 一进入就跳走
