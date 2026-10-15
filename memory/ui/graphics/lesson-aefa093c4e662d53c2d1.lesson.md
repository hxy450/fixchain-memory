# 由 vector drawable 转来的 SVG 图标按源 android:width/height 的 dp 取固有尺寸，不再按密度目录换算

ID：`lesson-aefa093c4e662d53c2d1` · 版本：2

[本主题](index.md)

## 何时使用

界面实现阶段，为不设尺寸的 Compose Image(painterResource(vector drawable)) 或 ImageView 引用的矢量图确定目标 Image 尺寸时；收口阶段按密度自动校正图标尺寸时

## 适用情境

源端 Image(painterResource(R.drawable.x)) 不设尺寸、按 drawable 声明的 dp 固有尺寸显示，或 ImageView 引用 vector drawable；源 drawable 是 <vector android:width="…dp" android:height="…dp">，常在无密度限定的 drawable 目录；目标 SVG 由它转换而来。

## 例外与边界

- 资源是位图（png/webp/jpg）：按所在密度目录把像素换算成 dp

## 原因

vector drawable 的 android:width/height 已是 dp，转出的 SVG 宽高沿用这组数值；再按密度目录相除，会把图标缩小数倍。无密度限定目录里的矢量图没有像素意义上的密度档。

## 做法

1. 固有尺寸取源 drawable 的 android:width/height（dp），直接作为目标 vp 尺寸，不做 ÷ 密度；viewportWidth/viewportHeight 是绘制画布的坐标（platforms/android-<api>/data/res/values/attrs.xml 的 VectorDrawable 定义），不当作尺寸。
2. 源端图片可能随父宽缩小时写 width('100%') + constraintSize({ maxWidth: 固有宽 }) + aspectRatio(固有宽/固有高)。
3. 自动校正图标尺寸的脚本遇到矢量来源时只报告、不按 3x 回写；用源 drawable 的 android:width/height 对照一次。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-d54a9506e30031090325](../../../store/cases/case-d54a9506e30031090325/86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1.json) · 结论：diagnosis, recommendation:7
  卡片版本：`86a488ddb6c31e5655996133c63edcc32569e729e74e510755e2f806ac20fae1`
