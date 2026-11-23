# ContentScale.FillWidth 无 ImageFit 对应值：宽度铺满、高按图片比例、容器 clip，不用 Fill/Cover

## 何时使用

界面实现阶段，把 Compose Image/AsyncImage 的 contentScale 映射为 ArkUI Image 属性、且源端取值为 ContentScale.FillWidth 或由调用方传入时

## 适用情境

源端图片用 ContentScale.FillWidth（如模糊缩略图、横幅），或由调用方传入 contentScale；目标 ArkUI Image 只有 objectFit 的 Fill、Cover、Contain 等取值。

## 原因

FillWidth 按宽度等比缩放，高度溢出时居中裁切；Fill 会拉伸变形，Cover 按两轴取大可能裁掉左右。组件只暴露 objectFit 参数时，调用方传 FillWidth 的意图在目标组件里没有入口，只能被就近换成 Fill。

## 做法

1. 宽度铺满容器，高度取容器宽除以图片宽高比（onComplete 拿到图片宽高，onAreaChange 取容器宽），显式尺寸溢出部分由容器 clip 并居中。
2. Android 组件的 contentScale 由调用方传入时，目标组件也提供对应参数（如 fillWidth），不在组件内固定一种 objectFit。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕ImageFit.Fill 不保持宽高比，放大缩小到充满显示边界；ImageFit.Cover 保持宽高比缩放到两边都大于或等于显示边界，超出部分被裁；两者对齐方式都是水平居中
- 〔做法第 1 步〕Image 的 onComplete 回调里 width、height 是图片源的宽高，componentWidth、componentHeight 是组件宽高，单位都是 px
- 〔做法第 1 步〕onAreaChange 回调给出的 Area 里 width、height 的单位是 vp，和 onComplete 的 px 不是同一单位
- 〔做法第 1 步〕容器没有设置 clip 时，默认不裁剪子组件超出自身范围的部分；clip 设为 true 后超出部分不可见，也不再响应绑定的手势
