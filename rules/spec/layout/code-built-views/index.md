# 代码里循环 new 再 addView 搭出的视图

agent 会看到什么：读到源码在循环里 new TextView 或自定义 View、逐个 addView 进容器（单个符号加大字号画的圆点指示器、只构造不刷新的一层格子）；规格写成「Html.fromHtml("&#8226;") → Text('•')」这类字符加字号的硬映射，或只按绘制方法写可见状态

## 规矩

- rule-3348b5bdc118｜源端用单个字形（•、●）大字号画指示器时，规格写源字体下的几何，不写字符加字号的硬映射｜读到：源码在循环里 new TextView、setText(Html.fromHtml("&#8226;")) 或单个符号（•、●、·、★）、setTextSize(远大于正文的字号)，逐个 addView 到 gravity=center 的 LinearLayout；内容只有一个符号，无标签、无链接；写错：规格的跨栈映射或组件契约写成「Html.fromHtml("&#8226;") 圆点 → Text('•')」「• U+2022, textSize 字号」这类字符加字号的硬映射，没写单点步进、直径、垂直位置
- rule-9697db6c306b｜同一源控件既有只构造的实例又有经绘制方法刷新的实例时，规格按层分别写可见状态｜读到：源码为某一层逐个 new 自定义 View 并 addView，之后没有调用绘制方法或 setVisibility（或 setVisibility(View.INVISIBLE) 被注释掉）；另一层经绘制方法刷新，绘制方法在值为 0 时 setVisibility(View.INVISIBLE)；写错：规格只写绘制方法的映射（「空块隐藏、非空块可见」），没写只构造的那一层保持构造态（可见、构造时设的背景和底色、空文本）
