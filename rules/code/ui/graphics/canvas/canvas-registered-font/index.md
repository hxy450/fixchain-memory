# Canvas 上用的注册字体

agent 会看到什么：读到源端 Typeface.createFromAsset 后 paint.setTypeface、measureText 参与布局；交回的代码 registerFont 后立刻 measureText，或 ctx.font 带引号、多了 bold

## 规矩

- rule-6f64babb191e｜Canvas 用注册字体时 ctx.font 写 `${size}px 字族名`，不加引号、不加源端没有的 bold｜读到：源端 Typeface.createFromAsset(...) 后 paint.setTypeface(...)，没有额外的 Typeface.BOLD；写错：目标端 ctx.font 组装成 `bold ${size}px '${字族名}'`：字族名外包了单引号，或多了源端没有的 bold
- rule-60279d428d88｜注册字体参与 measureText 布局时，首次布局前做就绪检查，几何经布局完成回调同步｜读到：源端 Typeface.createFromAsset 同步装载，measureText 测宽参与布局；写错：目标端调 registerFont 后马上 measureText 做首次布局；页面在尺寸变化回调之后立刻同步读布局结果算几何
