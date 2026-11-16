# drawBitmap 加 Matrix 的位图绘制

agent 会看到什么：读到源端 canvas.drawBitmap(bitmap, matrix, paint)，Matrix.setRectToRect 把位图像素矩形映射到画布；产物里变换矩阵按 PixelMap 的 getImageInfoSync().size 算，绘制却用三参数 ctx.drawImage(pm, 0, 0)

## 规矩

- rule-05849352a14f｜drawBitmap+Matrix 迁到 ArkUI Canvas 时，PixelMap 用五参数 drawImage｜读到：源端 canvas.drawBitmap(bitmap, matrix, paint)，Matrix.setRectToRect 把位图像素矩形映射到画布；写错：目标端变换矩阵的源矩形取 PixelMap 的 getImageInfoSync().size（像素），绘制却用三参数 ctx.drawImage(pm, 0, 0)
