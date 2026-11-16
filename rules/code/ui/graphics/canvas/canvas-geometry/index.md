# 自绘 View 的尺寸推导和画布单位

agent 会看到什么：读到自定义 View 在 onSizeChanged / onMeasure 的 px 尺寸上按常量和公式推导行高、格高、字号；产物里画布上下文的单位、参照常量、行高常量与容器高度对不上，或几何按值传进 @Builder

## 规矩

- rule-8836fb808013｜源 View 按 int px 布局和 Paint 度量时，画布上下文用 LengthMetricsUnit.PX 构造｜读到：安卓自定义 View 在 onSizeChanged(int w, int h) 的 px 尺寸上推导布局，Paint.setTextSize / measureText 按 px 算字号和派生内边距；写错：目标写的是默认构造 new CanvasRenderingContext2D(settings)，却把 ctx.width / height 当 px 用、字体串拼 `${n}px`，测宽结果偏小、字号被钳小
- rule-7aed4d6ee617｜源端自适应尺寸公式用固定参照基数时，目标保留成独立常量，不用当前实际格高代替｜读到：源端自绘 View 的尺寸推导里有一个固定参照基数常量（如月历自动行高的参照周数 = 6），先用内容总高 / 参照基数得到参照格高，再减去固定区、除以最少可见行数求行高；写错：目标 Canvas 组件里行高直接由当前实际格高（可用高度 / 当月实际行数）推算，参照基数常量不见了，行数多少的两种情形被算成同一行数
- rule-eb6c32bee87e｜带 clip(true) 的容器按行数×行高定高时，行高和画布绘制行高引用同一常量｜读到：源端自定义 View 在 onDraw 里按固定行高（@dimen/ 资源或常量）画一行行单元，外层布局的高度和折叠距离也由同一行高推出；写错：目标容器 .height(行数 × 行高 + …).clip(true) 和折叠范围用的行高数值，与 Canvas 组件里画行用的常量不同；或者只改了容器的行高，画布的行高常量没动
- rule-0a774fe09be1｜几何来自 onAreaChange 写入的状态时，不把宽高按值传给 @Builder｜写错：@Builder 函数带 (w: number, h: number) 这类参数，调用处传 onAreaChange 写进 @State 的宽高，旋转后布局不重算
- rule-413f06b74d20｜px 画布上下文里拿触点和 vp 窗口避让值比几何时，先 vp2px；vp 上下文不换｜写错：上下文按 LengthMetricsUnit.PX 构造，onTouch 里 TouchObject.x / y 或以 vp 保存的窗口避让值没 vp2px 就和画布几何比较；或上下文是默认 vp 构造，却对触点做了 vp2px
- rule-eb374bc58551｜px 画布上下文里用到 dp 声明的圆角等长度，先 vp2px 再交给 roundRect｜读到：源端 drawable 的 <corners android:radius="…dp"> 等 dp 尺寸被自绘几何使用，迁成按 vp 1:1 的数值常量；写错：上下文按 LengthMetricsUnit.PX 构造，ctx.roundRect(x, y, w, h, radii) 的 radii 仍直接用 dp/vp 数值常量，没有 vp2px
