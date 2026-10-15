# app/base-page

Android 业务基类（BaseActivity、BaseBusinessActivity）横切行为迁到组合式 BasePage：生命周期埋点与返回归因、触摸分发与点外收键盘的逐方法映射与逐页接线

[上一级](../index.md)

## 本级经验

- [源页面继承带生命周期副作用的业务基类、目标改用组合式 BasePage 时，逐方法列出副作用及守卫条件再逐页落地](lesson-2fcb6612ee4106b34e17.lesson.md)
  - 时机：公共基座实现与页面转换阶段，把 BaseActivity/BaseBusinessActivity 等业务基类的 onCreate、onDestroy、onBackPressed、dispatchTouchEvent 行为迁到 ArkUI 页面时
  - 情境：Android 页面统一继承业务基类，由基类自动完成页面展示/退出埋点（停留时长、返回键归因）、触摸计数、点外收键盘、进入淡入、前台能力开关等；ArkUI @ComponentV2 struct 不能继承，目标改用需逐页调用的组合式 BasePage 或工具类，页面还可能先于公共基座生成；负责基座或服务的任务可能不能改页面，规格指向的基类等价物（Mixin）也可能并不存在。也包括基类副作用写在 findViewById(R.id.x) != null、instanceof、标志位等守卫之内，并非每个子类都满足。
  - 例外：基类在 onResume/onPause 开关的是 NFC 前台派发这类按 UIAbility 注册的能力：按能力级注册加可见页登记处理，不逐页开关整个能力
