# PixelMap 的所有者和释放

agent 会看到什么：读到源端 Bitmap.recycle()、isRecycled、后处理后重新赋值的 bitmap、Bitmap.copy 后交给两处；产物里同一个 PixelMap 被入参、局部变量和调用方各自 release()，或画廊和 Canvas 覆盖层共用一个 PixelMap 没 cloneSync

## 规矩

- rule-d0ea834c6e06｜迁移 Bitmap.recycle 时给每个 PixelMap 定唯一所有者，只释放一次｜读到：源端 bitmap = 后处理结果.bitmap 重新赋值，缩略图和末尾 bitmap.recycle() 都针对成品，调用方另外再 recycle()；写错：后处理结果只放进局部变量，缩略图和末尾 release() 仍用入参 PixelMap；调用方在保存函数返回后又各自 release() 同一个 PixelMap
- rule-ee37fa287ff9｜同一 PixelMap 送给两个接收方时，接收方 cloneSync 后各自持有、各自 release｜写错：画廊和 Canvas 覆盖层共用同一个 PixelMap，两边各自 release()，重复释放后另一边画不出来
