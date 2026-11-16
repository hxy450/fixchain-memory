# 滚动中的可见比例判断

agent 会看到什么：读到 Compose Modifier.onGloballyPositioned 里用 boundsInWindow() 在滚动中算可见高度和比例（如 visibleHeight > height * 0.5f）；产物里挂在 .onAreaChange 上、用 globalPosition 加屏幕高算相交的可见性判断

## 规矩

- rule-2987952070ae｜滚动中算可见比例时用 onVisibleAreaChange，不用 onAreaChange｜读到：Compose Modifier.onGloballyPositioned { it.boundsInWindow() … } 在滚动中算可见高度（如 visibleHeight > height * 0.5f）；写错：可见性挂在 .onAreaChange((old, new) => …) 上，用 globalPosition.y 加屏幕高算相交高度
