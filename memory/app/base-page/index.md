# app/base-page

Android 业务基类（BaseActivity、BaseBusinessActivity）横切行为迁到组合式 BasePage：生命周期埋点与返回归因、触摸分发与点外收键盘的逐方法映射与逐页接线

[上一级](../index.md)

## 本级经验

- [Android 业务基类的横切行为逐方法映射到组合式 BasePage：副作用受守卫（findViewById 判空、instanceof、标志位）时，先按每个子类布局（含横竖屏变体）核对守卫是否成立，成立的页才逐页落地生命周期调用](lesson-2fcb6612ee4106b34e17.lesson.md)
  - 时机：公共基座实现与页面转换阶段，把 BaseActivity/BaseBusinessActivity 等业务基类的 onCreate、onDestroy、onBackPressed、dispatchTouchEvent 行为迁到 ArkUI 页面时
  - 情境：Android 页面统一继承业务基类，由基类自动完成页面展示/退出埋点（停留时长、返回键归因）、触摸计数、点外收键盘、进入淡入等；ArkUI @ComponentV2 struct 不能继承，目标改用需逐页调用的组合式 BasePage 或工具类，页面还可能先于公共基座生成。也包括基类在 onResume/onPause 开关前台能力（如 NFC 前台派发）、onNewIntent 统一处理并在不支持时跳转；服务切片不能改页面，规格指向的基类等价物（Mixin）并不存在。也包括基类副作用写在 findViewById(R.id.x) != null 等守卫之内，并非每个子类布局都含该 id。
