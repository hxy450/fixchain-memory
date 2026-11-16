# DisplayMetrics 屏幕宽高参与的几何

agent 会看到什么：源端用 getDisplayMetrics().widthPixels / heightPixels 算格径、留白、行数的公式（常在 FLAG_FULLSCREEN、targetSdk 低的 Activity 里），对应目标取尺寸的写法（getDefaultDisplaySync、windowRect、getWindowAvoidArea）

## 规矩

- rule-43b85070cc90｜源端公式用 DisplayMetrics 宽高时，目标按避让区算出的内容区取值，不用整屏尺寸｜读到：源端布局公式里用 DisplayMetrics 的宽高（如高度的几分之一作留白），Activity 是 FLAG_FULLSCREEN 全屏、targetSdk 较低；写错：目标用 display.getDefaultDisplaySync() 的整屏宽高代替 DisplayMetrics；页面内容没放进按内容区定宽高与偏移的容器
