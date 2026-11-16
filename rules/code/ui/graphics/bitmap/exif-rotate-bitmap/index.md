# 按 EXIF 方向旋转的位图

agent 会看到什么：读到源端 ExifInterface 按整数读 TAG_ORIENTATION（ORIENTATION_ROTATE_90 等）、经 Matrix.postRotate 旋转 Bitmap；产物里对 getImageProperty(image.PropertyKey.ORIENTATION) 的结果做 Number(...) / parseInt(...)，或手写像素平面旋转的下标公式

## 规矩

- rule-f3b1e4141075｜读 EXIF 方向用 getImageProperty(ORIENTATION) 时按描述字符串映射角度，不当数字解析｜读到：源端 ExifInterface 按整数读 TAG_ORIENTATION（ORIENTATION_ROTATE_90 等）再旋转；写错：目标对 getImageProperty(image.PropertyKey.ORIENTATION) 的结果写 Number(...) / parseInt(...)，拿不到角度
- rule-a51271b40364｜源端用 Matrix 旋转位图、目标手写像素平面旋转时，索引按新行乘输出宽加新列写｜读到：源端经 `Matrix` 按 EXIF 方向旋转 `Bitmap`；写错：手写平面旋转 90° 写成 `out[(H-1-y)*out.width + x]`、270° 写成 `out[y*out.width + (W-1-x)]`，把新 x 当成行号
