# onStart / onResume 里每次重做的初始化

agent 会看到什么：读到 Activity 的 onStart() / onResume() 里每次重读 getIntent()、重建列表、校验目录或重设界面文字；产物里 NavDestination 把这段挂在一次性的 .onReady(...) 或 aboutToAppear 里，.onShown 只做别的事

## 规矩

- rule-bab1aa08f28c｜安卓 onStart 里的初始化，目标写进 onWillShow，回前台在 onShown 里补｜读到：Activity 的 onStart() / onResume() 里每次都重读 getIntent()、重建列表、校验目录或重设界面文字；写错：对应 NavDestination 把这段初始化挂在一次性的 .onReady(...) 或 aboutToAppear 里，.onShown 只做别的事；注释仍写着源自 onStart
