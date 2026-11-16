# 布局里的 start / end 方向和 RTL 镜像

agent 会看到什么：读到布局 XML 里同一控件或三方容器带 android:layout_gravity="bottom|end" 和 android:layout_marginEnd；产物里 Alignment.BottomEnd、HorizontalAlign.End 配 .margin({ right })，或容器内部子项整体镜像、整体不镜像

## 规矩

- rule-09c5465b6441｜同一元素用了会镜像的逻辑对齐时，边距也用 start/end，不和 margin({ right }) 混用｜读到：源布局 XML 里同一个控件同时有 android:layout_gravity="bottom|end" 和 android:layout_marginEnd；写错：目标外层用 Stack({ alignContent: Alignment.BottomEnd }) 或 HorizontalAlign.End，而同一元素的边距写成 .margin({ right: … })
- rule-8b6df57282fc｜第三方容器内部是否随 RTL 镜像，读它的 onLayout 定，不由外层 Start/End 推断｜读到：源布局里第三方自定义容器（如 getbase 的 FloatingActionsMenu）带 android:layout_gravity="bottom|end"、layout_marginEnd，内部子项由容器自己排；写错：目标端把容器内部的子项（按钮列、标签）也整体随方向镜像，或整体不镜像，代码和注释里没有依据容器的 onLayout
