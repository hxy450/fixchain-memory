# Stack 中内容尺寸的子项按 alignContent 定位：源端纵向居中的文字用满高容器居中，Text.align 不改变它在父容器中的位置

ID：`lesson-92aee54a305ea0bde363` · 版本：1

[本主题](index.md)

## 何时使用

界面转换与巡检修复阶段，把 Compose 自定义 Layout 或 Box 中的文字改写为 ArkUI Stack 子节点并确定纵向位置时；修复或编译清理删除 height('100%')、.align() 等居中手段时

## 适用情境

源端自定义 Layout 用 placeRelative(x, (maxHeight - height) / 2) 把定宽文字纵向居中，或 Box 中文字按居中对齐放置；目标用 Stack({ alignContent: Alignment.TopStart }) 同时容纳文字与图片等对齐需求不同的子项。

## 原因

Stack 按 alignContent 放置未撑满的子节点；Text 的 .align() 只对齐文字在自身框内的位置，内容高的 Text 在 TopStart 的 Stack 里仍落在左上角，ArkUI Alignment 也没有 Compose 的 CenterStart。来源中巡检修复者为裁剪图片把 Row 改成 TopStart 的 Stack，删去 Text 的满高后改写 .align(Alignment.CenterStart) 并自称已居中；编译修复把它改成 Alignment.Start，随后又被删除，分类卡文字一直贴左上。

## 做法

1. 同一 Stack 中各子项对齐需求不同时，给文字包一个满高容器：Column().width(源端比例).height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Start)，或给子项按源公式单独 position/offset。
2. 删除 height('100%')、.align() 等手段前，确认替代约束仍实现原来的纵向位置；枚举名以 ArkUI SDK 为准，不照搬 Compose 的 Alignment 名称。

## 来源（按需复核）

- case-f749e3c70af1100c90d9 · 结论：recommendation:3, recommendation:4
  卡片版本：`4ab915d657b4b5d97eff00e45065e33757429c6731b5d26a5663f04484f0cf58`
