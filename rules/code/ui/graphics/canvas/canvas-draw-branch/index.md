# 自绘 Paint / Canvas 的绘制分支和坐标

agent 会看到什么：源端 Paint / Canvas 的绘制（paint.style、strokeWidth、drawPath、ItemDecoration.onDraw 的 y 换算），对应目标 Canvas 共享绘制分支里的 ctx.lineWidth、按 key 的特判和诊断日志，或 Polyline 的 points 与 position

## 规矩

- rule-1109387e348c｜源端 helper 不分 key 定描边宽时，目标共享分支统一 px2vp 换算，不按 key 特判｜读到：源端通用绘制 helper 对所有图形统一设 paint.style = Paint.Style.STROKE 或 Paint.Style.FILL_AND_STROKE、paint.strokeWidth = 传入值 ?: 默认 px 值，没有指标 key 参与；写错：目标多个指标共用的 Canvas 绘制分支写成 ctx.lineWidth = key === '某指标' ? 新值 : 旧值，只给被反馈的那个指标改线宽
- rule-6dc9c5725639｜临时诊断可以按 key 加条件，样式修复不绑在诊断条件上，交付前清掉诊断日志和 key 特判｜写错：交付的绘制代码里还留着 TEMP-DIAG 前缀的临时诊断日志，或样式赋值和诊断用的同一个 key 条件绑在一起（if (key === '某指标') { 打日志; 改 ctx.lineWidth }）
- rule-79419e876a2c｜复刻 ItemDecoration 折线时点和标签共用原点，点已含留白就不再给 Polyline 设 position｜读到：源端 RecyclerView.ItemDecoration 在同一个 Canvas 上用同一个 y 换算（已含 paddingTop 和文字高度）画折线和节点温度标签；写错：Polyline 的 points 用的是已含顶部留白的绝对 y，又给 Polyline 设了 .position({ y: <留白> })，折线相对标签整体下移、超出容器被裁
