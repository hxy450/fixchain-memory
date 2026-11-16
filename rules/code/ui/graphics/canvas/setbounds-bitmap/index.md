# setBounds 拉伸的预烘焙位图和取整坐标

agent 会看到什么：读到源端把圆角底和文字烘焙进 Bitmap、用 Drawable.setBounds((int)(…)) 把位图拉伸到新边界；产物里改成逐帧 roundRect + fillText 只缩了字号、台账批准的 OffscreenCanvas 缓存没沿用，或坐标没按 (int) 截断

## 规矩

- rule-8a13b5c945e8｜矢量重绘替代被 setBounds 拉伸的位图时，圆角、字号、基线一起乘缩放比｜读到：源端把圆角底 drawable 和文字一起画进固定尺寸的 `Bitmap`，动画期用 `Drawable.setBounds(...)` 把位图整体拉伸到新边界；写错：目标改成逐帧 `roundRect` + `fillText` 矢量绘制，只把字号乘了缩放比，`roundRect` 的圆角半径仍是常量
- rule-111601ff9983｜台账已批准离屏位图缓存时，沿用 OffscreenCanvas 预渲染加 drawImage 拉伸｜读到：决策台账或规格写着位图「以 `OffscreenCanvas` 预渲染缓存」（对应源端 `createBitmap` 预烘焙 + `setBounds` 拉伸）；写错：代码改走逐帧 `roundRect` + `fillText` 矢量绘制，注释却声明「行为等价」
- rule-6f09541ddf73｜源端坐标有 (int) 强转时，目标用 Math.trunc 截断后再绘制，不用 Math.floor｜读到：源端坐标表达式里有 `(int)` 强转，如 `setBounds((int)(...), ...)`、`int dX = (int)(...)`；写错：目标对应的边界或位移保留浮点直接绘制，或者用了 `Math.floor` / `Math.round`
