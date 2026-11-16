# Coil 有占位、错误图和 crossfade 时，Image 写 alt 加 contentTransition

审的是：代码
触发（任一种）：
- 读到：默认 ImageLoader.Builder 或 ImageRequest.Builder 上有 .placeholder(...)、.error(...)、.crossfade(true)；写错的样子：目标 Image 只写 .alt(错误图)，加载中没有占位；或把 crossfade 说成 Image 的默认过渡，没写 .contentTransition(...)
适用范围：Coil 加载的图片迁成 ArkUI Image 时；ImageAlt 出自声明 @since 22，contentTransition 出自声明 @since 21
做法：
- 写成 Image(src).alt({ placeholder: <源端 placeholder 的资源>, error: <源端 error 的资源> })
- 源端 crossfade(true) 写成 .contentTransition(ContentTransitionEffect.OPACITY)
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- alt(src: ResourceStr | PixelMap | ImageAlt): ImageAttribute：加载中的占位；参数类型是 AnimatedDrawableDescriptor 时不生效（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.alt）
- interface ImageAlt { placeholder?: ResourceStr | PixelMap; error?: ResourceStr | PixelMap }：placeholder 是加载中占位，error 是加载失败时的图（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAlt）
- contentTransition(transition: ContentTransitionEffect): ImageAttribute：图片内容变化时的动画（出处：鸿蒙 SDK 的 ets/component/image.d.ts，ImageAttribute.contentTransition）
- ContentTransitionEffect.OPACITY（另有 IDENTITY 无动画）：内容变化时淡入淡出，对应 crossfade（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ContentTransitionEffect.OPACITY）
针对本应用要查的：
- 源端 placeholder 和 error 用的资源：源工程里默认 ImageLoader.Builder（Application 的 newImageLoader）和各处 ImageRequest.Builder 的 placeholder(...)、error(...)；读出资源名，换成目标工程里对应的 $r('app.media.…') 资源
未核实：卡里的上机行为出自 HarmonyOS 6.1.1(24)，本机按 API 23 的声明核实
来源：1 张卡，1 个应用
- case-af4252d474c172e093fc（jerboa）：做法第 1 步 ← 诊断；做法第 2 步 ← 诊断
