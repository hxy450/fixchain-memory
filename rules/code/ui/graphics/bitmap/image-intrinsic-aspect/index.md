# 按素材固有比例定高的图片（ContentScale.FillWidth、无宽高约束的 img）

agent 会看到什么：读到 Compose Image / AsyncImage 写 contentScale = ContentScale.FillWidth，或网页模板里没有 width、height 约束的 IonImg / <img>；产物里 Image 用 objectFit(ImageFit.Fill / Contain / Cover) 加 layoutWeight 或固定高代替按素材比例算高

## 规矩

- rule-f77431aa449f｜ContentScale.FillWidth 不用 ImageFit.Fill，按图片比例算高并 clip｜读到：Compose Image / AsyncImage 写 contentScale = ContentScale.FillWidth，或组件的 contentScale 由调用方传入、调用处传 ContentScale.FillWidth；写错：目标 Image 写 .objectFit(ImageFit.Fill) 或 ImageFit.Cover 代替；或 ArkTS 组件只暴露 ImageFit 参数，调用处传 ImageFit.Fill
- rule-6d464464aa96｜源图片没有宽高约束时，读出素材像素比例，用满宽加 aspectRatio 定高｜读到：源 IonImg / <img> 没有 width、height 约束（满宽、按素材固有比例）；写错：目标写 Image(…).objectFit(ImageFit.Contain).layoutWeight(1)，图片在撑满的框里内缩；或按「截图」之类的推测定比例
