# 控制进度显示的加载状态

agent 会看到什么：读到源码先 progressBar.setVisibility(View.VISIBLE) 显示进度，再调用遇到空查询等情况会提前 return 的方法；产物里控制进度显示的布尔 @Local 置 true 之后，某个分支直接 return、没有复位为 false

## 规矩

- rule-d522d2613099｜置了加载状态的路径要提前 return 时，先把加载状态复位｜读到：源码先 progressBar.setVisibility(View.VISIBLE) 显示进度，再调用遇到空查询等情况会提前 return 的查询方法；写错：目标代码先把控制进度显示的布尔 @Local 状态置 true，之后某个分支直接 `return`，没有把它复位为 false
