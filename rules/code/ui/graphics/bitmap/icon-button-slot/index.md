# 固定承载区里的图标按钮

agent 会看到什么：读到工具栏、按钮的 ImageView / ImageButton 放在固定 android:layout_width 的承载区里，或写固定 dp 盒子加 android:scaleType="centerInside"；产物里槽位宽沿用旧值、图标尺寸和点击区写在同一个 Image 上、Image 设成盒子大小再 Contain，或照范式页逐字抄了宽高和 objectFit

## 规矩

- rule-60e727a4acd5｜工具栏点击槽宽取源布局承载区宽度，与图标尺寸分开核对｜读到：源工具栏布局里每个按钮的承载区有固定 android:layout_width（返回键与其余按钮可能不同），ImageView 在其中居中；写错：目标端槽位的 .width(…) 沿用旧代码的值，与源布局承载区宽度不符，或者没有和图标分开的槽位
- rule-1e339ebb1b84｜位图按钮不要在同一 Image 上先写图标尺寸再写槽位宽高，槽位放外层 Stack｜读到：安卓工具栏按钮是固定宽度承载区里居中显示的 ImageView；写错：同一个 Image 链上先写 .width(…).height(…).objectFit(ImageFit.Contain)，后面又接 .width(…).height(…) 当点击区
- rule-985ad4eaf1e1｜固定盒加 centerInside 的图标，外层留盒、内层 Image 设固有 dp，不用满盒 Contain｜读到：ImageButton / ImageView（含 AppCompatImageButton）写固定 dp 的 layout_width / layout_height 加 android:scaleType="centerInside"，图标只放在 drawable-xhdpi 等密度目录、固有 dp 小于盒子；映射参考写「centerInside → ImageFit.Contain」；写错：Image 自己设成盒子尺寸再写 .objectFit(ImageFit.Contain)，小图标被放大到满盒
- rule-7b46bf558416｜照已完成页面范式复用图标控件行时，按本页源 XML 重核 scaleType 和盒尺寸｜读到：派工写「可参考已完成的同域页面」，范式页里图标是盒尺寸 Image 加 objectFit(ImageFit.Contain)；写错：本页 Image 的宽高和 objectFit 与范式页逐字相同，没按本页源 XML 的 android:scaleType 和盒尺寸重核；或某页已修好图标尺寸，别的页面同一图标仍是旧写法
- rule-5ed63c70fb0f｜固定宽高的可点 ImageView 迁成同尺寸的点击容器，不缩成图标本身大小｜读到：源布局里返回键等 ImageView 写了固定的 android:layout_width / android:layout_height（dp）加 paddingVertical，图标画在这个点击区里；写错：鸿蒙端只按图标尺寸写 Image(...) 的 .width / .height 加上下 padding，没有和源端同宽高的点击容器
