# LinearLayout 的 weightSum 与子权重之和不等，或 wrap_content 子项带权重时，不用 layoutWeight 归一化：余量（可用尺寸减各子项自然尺寸）按 w/剩余 weightSum 依次分配，份额耗尽的子项只留自然尺寸，超出 weightSum 的末块被裁

ID：`lesson-adad817f2c3c8f1eaa09` · 版本：1

[本主题](index.md)

## 何时使用

界面实现阶段，把 Android LinearLayout 的 layout_weight/weightSum 分配翻译成 ArkUI 尺寸时；规格提取阶段写权重布局时

## 适用情境

源布局声明 weightSum 且与子权重之和不等（如根 weightSum=10 而子权重 4/1/9，列 weightSum=6 而 8 个 wrap_content 子项各权重 1），或 wrap_content 子项带权重、自然尺寸各不相同。

## 原因

ArkUI layoutWeight 按权重和的比例分配全部空间，等于忽略 weightSum 与子项自然尺寸：源端被裁的末块、份额耗尽的子项与留白都会变形。

## 做法

1. 按 LinearLayout 算法计算：先测各子项自然尺寸，余量按权重依次分配（每次除以剩余 weightSum），weightSum 用尽后的子项只保留自然尺寸，总和超出可用尺寸的末块按剩余空间裁切；可按容器实测尺寸算出位置后绝对定位，或用占位补足 weightSum 余下的份额。
2. 带权重的 wrap_content 图片固有尺寸超过行能给的空间时，按父级上限夹紧盒子后等比缩小，不填经验值；写完抽 2–3 个位置（行中心、分隔线）与源端截图的 dp 对比。
3. 规格写权重布局时同时写 weightSum 与子权重之和，以及溢出、份额为 0 的子项，不只列各子项权重。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-4e7e0e12d7b6b08c08b0](../../../../store/cases/case-4e7e0e12d7b6b08c08b0/01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:4
  卡片版本：`01e35fad86da84ee72ab8dae4e42ffdfe63b5ab1b816e24b5614e9d185c42115`
