# 多列容器里的 no-op 广告位

agent 会看到什么：源端 GridLayoutManager + SpanSizeLookup 让广告项通栏，而全局决策或派工把广告定为 no-op 空容器；规格对 Grid、WaterFlow 的转换决策

## 规矩

- rule-ce152961de21｜广告定为 no-op 时，规格对 Grid、WaterFlow 等多列容器写明广告位是否参与排布｜读到：源端 GridLayoutManager 多列、SpanSizeLookup 让广告通栏；全局决策或派工把广告定为 no-op 空容器；写错：规格的转换决策只写「广告项通栏：Grid columnsTemplate '1fr 1fr' + columnSpan 等价实现」或「零高塌陷与 Android 一致」，没写 no-op 广告位在多列容器里参不参与排布
