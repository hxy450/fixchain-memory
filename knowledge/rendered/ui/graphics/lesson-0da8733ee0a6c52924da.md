# 根背景是按产品 flavor 覆盖的 layer-list 时按生效版本逐层落成组件；位图暂缺也保留 Image 引用并申报，不降成纯色底

## 何时使用

页面界面转换阶段，迁移根布局的 layer-list 背景 drawable（含产品 flavor 覆盖 main 的情形），尤其所需位图尚未进入目标 media 时

## 适用情境

源页面根背景是 layer-list（纯色底、全屏位图、定位的品牌图），main 与产品 flavor 的 sourceSet 各有一份，flavor 版覆盖 main；规格要求 Stack 加全屏 Image 背景；目标工程缺失的资源由后续批次统一补源，转换期不编译。

## 例外与边界

- 逐层落成组件时保持 layer-list 的层序：layer-list 按 item 顺序绘制、后面的 item 盖在上面，Stack 也是后声明的子组件盖在前面，所以 Stack 子组件按 item 原顺序排列，不要为了把背景放在一起而调换顺序；纯色底用 Stack 自身的 backgroundColor 时它始终在所有子组件之下

## 原因

只看 main 版或只保留第一层纯色，品牌图层整体丢失；把图层降成注释或“资产未迁移”说明后，补资源的环节只拷文件、不改页面，可见层一直没人接。

## 做法

1. 按构建配置选中的产品 flavor 解析背景 drawable，把每层落成组件：纯色底用 backgroundColor；gravity=fill（或 item 既没写 gravity 也没写 width/height）的位图用 100%×100% 的 Image 加 ImageFit.Fill（Image 不写 objectFit 时按 Cover 等比裁切）；带 gravity 与 top 偏移的品牌图按固有尺寸放 Image，用 padding 或 position 摆位（Stack 的 alignContent 默认 Alignment.Center，用 padding 按顶部偏移摆位时先把对齐设成顶部）。
2. 位图暂缺而编译在补资源后才跑时，照常写目标资源名的 $r 引用并在报告中申报缺口，或直接从源 sourceSet 拷贝；确需延后时用带负责方和可机读触发条件（如断言工程中存在该资源引用）的移交。
3. 补资源的步骤落盘后，检查代码槽是否已引用该资源；只有注释时把接线交给明确负责方。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔做法第 1 步〕Image 不写 objectFit 时按 ImageFit.Cover 显示：保持宽高比缩放，裁去超出部分，不是拉伸铺满
- 〔做法第 1 步〕ImageFit.Fill 不保持宽高比缩放，让图片填满显示边界
- 〔做法第 1 步〕安卓 gravity 的 fill（0x77）是 fill_horizontal（0x07）与 fill_vertical（0x70）的组合，横纵两个方向都铺满容器
- 〔做法第 1 步〕layer-list 的 item 没写 width/height 时，gravity 默认在两个方向取 fill_horizontal、fill_vertical；写了尺寸时默认 left、top；width、height 没写时取该层 drawable 的固有尺寸
- 〔做法第 1 步〕Stack 的 alignContent 在应用没有另设时为 Alignment.Center，子组件默认居中叠放
- 〔做法第 2 步〕resources 的 media 目录只放文件，图片支持 .jpg、.png、.gif、.svg、.webp、.bmp
