# LottieAnimationView 动画层

agent 会看到什么：读到布局里的 com.airbnb.lottie.LottieAnimationView、代码 setAnimation("json/...") 或按数据状态切动画；产物里只有一张静态 Image($r('app.media.…'))，没有 @ohos/lottie 依赖、迁过来的 json 文件和占位登记

## 规矩

- rule-2e80873209cb｜源布局有 LottieAnimationView 或按状态切动画时，目标接 @ohos/lottie 并迁动画文件｜读到：布局里有 `com.airbnb.lottie.LottieAnimationView`（常与静态 ImageView 同尺寸叠在一起），代码调用 setAnimation("json/...") 或按数据状态切换动画；写错：ArkTS 只写一张静态 Image($r('app.media.x')) 作为唯一的图，没有 Lottie 动画层、@ohos/lottie 依赖、迁过来的 json 文件，也没有占位登记
