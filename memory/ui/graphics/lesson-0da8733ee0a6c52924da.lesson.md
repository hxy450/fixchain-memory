# 根背景是按产品 flavor 覆盖的 layer-list 时按生效版本逐层落成组件；位图暂缺也保留 Image 引用并申报，不降成纯色底

ID：`lesson-0da8733ee0a6c52924da` · 版本：1

[本主题](index.md)

## 何时使用

页面界面转换阶段，迁移根布局的背景 drawable，尤其所需位图尚未进入目标 media 时

## 适用情境

源页面根背景是 layer-list（纯色底、全屏位图、定位的品牌图），main 与产品 flavor 的 sourceSet 各有一份，flavor 版覆盖 main；规格要求 Stack 加全屏 Image 背景；目标工程缺失的资源由后续批次统一补源，转换期不编译。

## 原因

只看 main 版或只保留第一层纯色，品牌图层整体丢失；把图层降成注释或“资产未迁移”说明后，补资源的环节只拷文件、不改页面，可见层一直没人接。

## 做法

1. 按构建配置选中的产品 flavor 解析背景 drawable，把每层落成组件：纯色底用 backgroundColor；gravity=fill 的位图用 100%×100% 的 Image 加 ImageFit.Fill；带 gravity 与 top 偏移的品牌图按固有尺寸放 Image，用 padding 或 position 摆位。
2. 位图暂缺而编译在补资源后才跑时，照常写目标资源名的 $r 引用并在报告中申报缺口，或直接从源 sourceSet 拷贝；确需延后时用带负责方和可机读触发条件（如断言工程中存在该资源引用）的移交。
3. 补资源的步骤落盘后，检查代码槽是否已引用该资源；只有注释时把接线交给明确负责方。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-bcb4b234c7b3327e2100](../../../store/cases/case-bcb4b234c7b3327e2100/48e25a7d2498dc3fb69ab265d6940adf5a422adf40cd38f8f7a8ffade949a244.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3, recommendation:4
  卡片版本：`48e25a7d2498dc3fb69ab265d6940adf5a422adf40cd38f8f7a8ffade949a244`
