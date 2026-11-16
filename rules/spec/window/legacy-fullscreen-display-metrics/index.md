# 低 targetSdk 全屏窗口下以 DisplayMetrics 为基准的几何

agent 会看到什么：源自绘 View 用 getDisplayMetrics() 的 widthPixels / heightPixels 作几何基准，Activity 是 FLAG_FULLSCREEN，Manifest 的 targetSdkVersion 低、没声明 windowLayoutInDisplayCutoutMode / maxAspectRatio，规格里按整屏或「全屏减底部避让」取值

## 规矩

- rule-be4445a10646｜源 targetSdk 低的全屏窗口，规格写明挖孔边留黑和按 1.86 截长边后的内容区｜读到：源自绘 View 用 getDisplayMetrics() 的 widthPixels / heightPixels（或 Display.getSize）作几何基准，Activity 只设 FEATURE_NO_TITLE + FLAG_FULLSCREEN，targetSdkVersion 低；写错：规格或台账把几何基准写成「全屏窗口 px 尺寸 − 底部系统避让区高度」，只把导航栏当成两端的差别
- rule-663ced688c7b｜基准高经整数截断决定格数行数时，AC 写参照机尺寸下两端一致的派生整数｜读到：源公式把基准宽高整数截断成格径、底栏、起始空行等（如 (int)(y·40%/格径)）；写错：AC 只断言基准公式或「非全窗高」，没写参照机尺寸下派生出的格径、行数等整数，也没写参照机实测的应用窗口尺寸
