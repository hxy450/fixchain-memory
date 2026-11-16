# 显隐切换带的淡入淡出动画

agent 会看到什么：读到源码在 setVisibility(View.VISIBLE / View.GONE) 前后调淡入淡出（fade 辅助方法、startAnimation、res/anim 的 <alpha>），动画结束才切显隐；产物里直接改 if 条件渲染依赖的状态让节点瞬显瞬隐，没有 animateTo

## 规矩

- rule-70ef08d2eb92｜源端显隐带淡入淡出动画时，目标用 animateTo 带源时长并在 onFinish 里切显隐｜读到：源码在 setVisibility(View.VISIBLE / View.GONE) 前后调用淡入淡出（fade 辅助方法、startAnimation、res/anim 的 alpha 动画），动画结束才切显隐；写错：目标直接改 if 条件渲染所依赖的状态（如置空串）让这一行瞬显瞬隐，没有 animateTo，注释写「fade 等价：状态驱动可见性」之类
