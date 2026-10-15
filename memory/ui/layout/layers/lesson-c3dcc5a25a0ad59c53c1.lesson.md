# 运行时 addView 挂到根部的播放器面等按运行时层级实现：尺寸取 LayoutParams 或根容器默认参数，不按 XML 占位定几何

ID：`lesson-c3dcc5a25a0ad59c53c1` · 版本：4

[本主题](index.md)

## 何时使用

界面实现阶段，转换含运行时挂载子视图（播放器面等）的列表项或页面、确定视频层与浮层关系时

## 适用情境

源 Fragment/Adapter 在播放时通过 addView/LayoutParams 把视图挂到根容器（如 addView(videoView, 0)），XML 里同名区域只是封面或控制视图；目标用 Stack/Column 重建层级。

## 原因

只看 XML 会把封面/控制区当成视频区，把视频夹在标题行与按钮行之间；运行时视图的尺寸与层序由 addView 传入或自带的 LayoutParams、根容器的默认参数、插入 index 与 elevation 决定，与 XML 占位无关。

## 做法

1. 先在 Fragment/Adapter 中查 addView/removeView/LayoutParams，确认运行时视图挂在哪个容器、插入 index 与有无 elevation，再定层级：index 0 在最底层，后加的在上。
2. 尺寸先看 addView 传入或视图自身已有的 LayoutParams；都没有时取根容器的 generateDefaultLayoutParams（ViewGroup.java addView）：FrameLayout 为 MATCH_PARENT×MATCH_PARENT 才铺满，RelativeLayout（RelativeLayout.java）与 ConstraintLayout（constraintlayout 2.1.4 的 generateDefaultLayoutParams）为 WRAP_CONTENT×WRAP_CONTENT，纵向 LinearLayout 为 MATCH_PARENT×WRAP_CONTENT。WRAP_CONTENT 的一边由该视图自身的 onMeasure 决定（播放器视图可能仍测成满尺寸），读其实现或对照源端运行截图确定；结果铺满的才放在根 Stack 底层写 100%×100%。
3. XML 占位区只保留封面与播放态显隐。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-c85d8667f78c2cc8f53a](../../../../store/cases/case-c85d8667f78c2cc8f53a/0a66d146244ac3bab2016664057dd3427c0c6c210bea434eab6b298234f871bf.json) · 结论：diagnosis, recommendation:1
  卡片版本：`0a66d146244ac3bab2016664057dd3427c0c6c210bea434eab6b298234f871bf`
