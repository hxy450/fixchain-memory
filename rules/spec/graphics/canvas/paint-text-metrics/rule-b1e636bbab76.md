# 源端用 getTextBounds 取文字高时，规格映射到 actualBoundingBox，不列字体行框

审的是：规格
触发（任一种）：
- 读到：源端自绘 View 用 Paint.getTextBounds(text, start, end, rect) 后取 rect.height() 定行高、行距或自适应字号；写错的样子：映射行写 getTextBounds.height → fontBoundingBoxAscent + fontBoundingBoxDescent，或把 fontBoundingBox* 列为候选、注「字段待实测（对照字体 hhea）」，验收条目不断言字段
适用范围：规格提取阶段写 Paint 文字度量到 TextMetrics 的映射行时
做法：
- 先按源 API 判断度量层级：getTextBounds / Rect.height() 是所测字符的墨迹紧包围盒，Paint.ascent / descent / getFontMetrics 才是字体级行框
- 映射行写成：getTextBounds 高度 → Math.ceil(m.actualBoundingBoxAscent) + Math.ceil(m.actualBoundingBoxDescent)（m = ctx.measureText(所测子串)），写清所测子串（text 的 start 到 end）和取整方式，不把 fontBoundingBox* 列为候选
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- getTextBounds 返回包住所有字符的最小矩形，原点隐含在 (0,0)（基线起点）：源端是墨迹级度量（出处：android.graphics.Paint#getTextBounds）
- Paint.ascent() 按当前字体和字号返回基线以上的距离（负值）：字体级度量，和 getTextBounds 不是一个层级（出处：android.graphics.Paint#ascent）
- actualBoundingBoxAscent / actualBoundingBoxDescent：textBaseline 指示的水平线到渲染文字矩形边界顶部 / 底部的距离：目标端的墨迹级度量，对应 getTextBounds（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.actualBoundingBoxAscent、TextMetrics.actualBoundingBoxDescent）
- fontBoundingBoxAscent / fontBoundingBoxDescent：到所有字体渲染文字最高矩形边界顶部 / 底部的距离：字体级行框，不对应 getTextBounds（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，TextMetrics.fontBoundingBoxAscent、TextMetrics.fontBoundingBoxDescent）
- 两项各自 Math.ceil，对应 Skia 的 roundOut 外扩取整；字体行框约比墨迹包围盒大 1.4 倍：取整方式和用错字段时的偏差量级（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-dcca102a6a4baff0e7a7（Blockinger）：做法第 1 步 ← 建议 1；做法第 2 步 ← 建议 1；取值 5 ← 诊断
