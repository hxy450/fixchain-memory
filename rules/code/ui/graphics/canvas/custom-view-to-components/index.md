# 自绘 View 改成组件组合

agent 会看到什么：读到自定义 View 在 onDraw 里用 drawCircle、drawRoundRect 画角标、指示条；产物里改用 Circle、Blank、padding 等组件拼出，尺寸和内边距没按源端绘制公式算

## 规矩

- rule-c72f3de31a15｜从自绘角标推导无数字红点尺寸时，按实际计数分支的绘制半径求直径｜读到：源端自定义 View 用计数切换无数字红点和带数字角标（计数为 0 是红点），尺寸由 dp 半径基数、计数分支和 DisplayMetrics.density 分支算出，onDraw 里 canvas.drawCircle(cx, cy, radius, paint)；写错：目标端红点写成 Circle().width(16).height(16) 这类：把半径基数乘 2、或带数字角标分支的高度当成无数字红点的直径，和承载它的入口相比明显过大
- rule-2001d1f124d2｜自绘指示条改写成组合布局时，底部内边距照源值，不把指示条高度扣掉｜读到：自定义 View 的 onDraw 在 height − paddingBottom 之上画选中指示条和文字基线，布局 XML 给了 android:paddingBottom；写错：鸿蒙端在 Text 下另加一个指示条高度的 Blank，又把 bottom padding 写成源值减去指示条高度
