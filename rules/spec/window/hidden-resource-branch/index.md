# 靠隐藏系统资源判断的源端分支

agent 会看到什么：源端用 Resources.getSystem().getIdentifier 读隐藏系统资源（如 config_navBarInteractionMode）决定行为，如非手势导航时 setNavigationBarColor；规格里以「无对等」删掉这段分支

## 规矩

- rule-baeef096f896｜源端分支依赖隐藏 API 或系统资源时，规格写可观察条件和效果，找目标等价信号，不删行为｜读到：源端按隐藏系统资源判断（如读 config_navBarInteractionMode 的 isUsingGestures），非手势导航时 setNavigationBarColor(…) 给导航栏着色；写错：规格以「检测用的隐藏资源无对等」为由把检测分支和着色整体删除，相关验收条目被标为 superseded
