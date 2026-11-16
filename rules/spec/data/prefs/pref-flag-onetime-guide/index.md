# 偏好标记控制的一次性引导

agent 会看到什么：读到源码里引导图只在某个偏好标记为真时 VISIBLE、点击隐藏，显示后随即调 setter 写回标记，布局里引导 ImageView 为 match_parent 加 android:scaleType="fitXY"；行为笔记或规格里没有这个首次引导项

## 规矩

- rule-bedd2ee63ced｜由偏好标记控制的一次性引导，行为提取时列为独立项，写明资源、显示条件、关闭方式和标记｜读到：源码里引导图只在某个偏好标记为真时 VISIBLE、点击隐藏，显示后随即调 setter 写回标记；布局里引导 ImageView 为 match_parent 加 android:scaleType="fitXY"；写错：行为笔记或规格里没有这个首次引导项
