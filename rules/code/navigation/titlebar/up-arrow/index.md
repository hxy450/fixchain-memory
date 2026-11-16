# 标题栏的返回箭头

agent 会看到什么：源端 Manifest 的 android:parentActivityName、代码里的 setDisplayHomeAsUpEnabled 和窗口 ActionBar 主题；产物里自绘标题栏有没有返回箭头

## 规矩

- rule-8a4f95591a22｜主题带窗口 ActionBar、Manifest 有 parentActivityName 时，自绘标题条画 Up 箭头｜读到：Manifest 里 Activity 有 android:parentActivityName 或 android.support.PARENT_ACTIVITY meta-data，主题是带窗口 ActionBar 的 Theme.AppCompat（如 DarkActionBar），代码没调 setDisplayHomeAsUpEnabled，onOptionsItemSelected 处理 android.R.id.home；写错：自绘标题条里没有返回箭头，注释写「源端未调 setDisplayHomeAsUpEnabled，无返回箭头」，返回只靠系统返回键
- rule-6e632615d896｜源端无 parentActivityName 和 setDisplayHomeAsUpEnabled 时，不画返回箭头｜读到：Manifest 的 <activity> 没有 android:parentActivityName，Activity 代码里没有 setDisplayHomeAsUpEnabled(true) / getSupportActionBar()；写错：自绘标题栏开头画了返回箭头（ic_back 图标、showBack 选项，或注释写 up affordance）
- rule-171b80794910｜homeAsUp 返回箭头用 Image 加 matchTextDirection(true)，不换系统符号｜读到：源码 `setDisplayHomeAsUpEnabled(true)`，默认箭头 `abc_ic_ab_back_material` 带 `android:autoMirrored="true"`；写错：目标返回按钮写成 `SymbolGlyph($r('sys.symbol.chevron_left'))`，或 Image 没写 `.matchTextDirection(true)`
- rule-c2d90239d28f｜home 分支调 super.onBackPressed() 或 finish() 时，Up 单独实现，不并进返回键分支｜读到：onMenuItemSelected / onOptionsItemSelected 的 android.R.id.home 分支调 super.onBackPressed()、finish() 或直接跳转，而子类覆写的 onBackPressed 里另有分支（如先回退内部步骤）；写错：目标 Up 和系统返回共用一个处理函数（Up 也先走 onBackPressed 里的回退分支），注释写「home 与 onBackPressed 同分支」；或者用 NavDestination 系统标题栏的返回钮承接 Up
