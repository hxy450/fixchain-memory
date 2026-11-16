# 代码里的框架颜色常量（Color.GREEN、Color.RED）

agent 会看到什么：读到源码 setTextColor(Color.GREEN) 等 android.graphics.Color 常量；规格的颜色映射按颜色名对到色值不同的应用色令牌（如「Color.GREEN → light_green」）

## 规矩

- rule-2c2138b511ab｜规格映射 Color.GREEN 等框架颜色常量时按色值对令牌，没有同值令牌就写明新增｜读到：源码里 setTextColor(Color.GREEN)、Color.RED 等 android.graphics.Color 常量；写错：规格的颜色映射写成「Color.GREEN → light_green」这类按名字对到色值不同的应用色令牌
