# supportsRtl 声明和 RTL 语言资源

agent 会看到什么：读过的 AndroidManifest 写没写 android:supportsRtl、res 下有 values-fa / values-ar 等 RTL 语言目录、源码用 Canvas.drawText 画文字；交回的规格里布局方向契约、画布文字方向和 RTL 验收条目

## 规矩

- rule-4d2c014c37af｜未声明 supportsRtl 时，规格写明布局恒 LTR，有顺序语义的容器逐个设 Direction.Ltr｜读到：AndroidManifest.xml 的 `<application>` 没有 `android:supportsRtl`；写错：规格里没有布局方向契约，按钮条、靠起点对齐的容器没要求显式方向；或只写「Canvas 不镜像」就当 RTL 已处理
- rule-8f54e1875471｜源 Manifest 写 supportsRtl=true 时，规格把 RTL 镜像列为全局契约传给各页｜读到：AndroidManifest 的 <application> 写了 android:supportsRtl="true"，源码用 start / end 和 Icons.AutoMirrored；写错：页面规格没有 RTL 镜像契约，资源映射把 AutoMirrored 记成普通媒体资源
- rule-c8dc4452dd74｜规格把 Canvas.drawText 映射到 fillText 时，写出按首个强方向字符设 direction 的契约｜读到：源端用 `Canvas.drawText(..., paint)` 配默认 `new Paint()` 画文字，没做 bidi 或方向设置；资源里有 values-fa 等 RTL 语言；写错：规格映射写「drawText→fillText 1:1 移植」，或写「按原串绘制即 parity、不需特殊 RTL 处理」「Android drawText 同样不做 bidi」，没有段落方向契约
- rule-416b7592a245｜RTL 验收除 RTL 资源语言外，还要覆盖回落英文的 RTL 系统语言，查句末标点和按钮顺序｜读到：资源里有 values-fa 等 RTL 语言目录，manifest 未声明 `android:supportsRtl`；写错：RTL 验收条目只比 fa 截图「同为左对齐」，或以「全仓 grep bidi/rtl/mirror 零命中」判等价落地
- rule-ac26abd7e3bc｜源清单 supportsRtl=true 且有 RTL 语言资源时，ui-manifest 全局约定登记布局方向镜像｜读到：AndroidManifest.xml 的 application 标签有 android:supportsRtl="true"，res 下有 values-ar、values-he、values-fa 等 RTL 语言目录；写错：ui-manifest、feature-base 或页面规格的全局约定里没有布局方向镜像（RTL）要求，全文搜不到 RTL、supportsRtl、镜像
