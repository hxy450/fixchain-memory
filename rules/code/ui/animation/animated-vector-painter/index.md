# Compose 的 AnimatedVectorDrawable 动画图标

agent 会看到什么：读到 Compose 用 AnimatedImageVector.animatedVectorResource(R.drawable.…) 加 rememberAnimatedVectorPainter(icon, atEnd)，产物里是 Image($r('app.media.…')) 静态图、SymbolGlyph 按状态切换或 Path / Canvas 的 pathData 插值

## 规矩

- rule-f135b2607438｜rememberAnimatedVectorPainter 迁成两组 pathData 间插值，不用静态图或符号切换｜读到：源 Compose 用 AnimatedImageVector.animatedVectorResource(R.drawable.…) 加 rememberAnimatedVectorPainter(icon, atEnd)；写错：目标端写成 SymbolGlyph 在 sys.symbol.play_fill / pause_fill 间按状态切换，或 Image($r('app.media.…')) 只显示静态首帧
- rule-8264f96941d7｜rememberAnimatedVectorPainter 按 atEnd 切帧时，目标按同一状态分支给起点和终点图形｜读到：Compose 里 rememberAnimatedVectorPainter(AnimatedImageVector.animatedVectorResource(R.drawable.…), atEnd)，atEnd 由步骤完成、计时运行等状态决定；写错：各状态都写同一个 Image($r('app.media.…'))（资源迁移导出的同名静态 SVG），atEnd 的状态条件没有落到输出
