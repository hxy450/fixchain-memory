# Vibrator 振动和提示音

agent 会看到什么：读过的源码里调 Vibrator 的 cancel / vibrate、用 MediaPlayer 播提示音或 performHapticFeedback；交回的代码里 vibrator.startVibration / stopVibration 有没有写、先后是否串行

## 规矩

- rule-cfcd5d42331f｜源端计时器步骤切换按偏好发声振动时，目标步进分支读偏好并播 rawfile 提示音、调振动｜读到：源端计时器在非静默步骤切换时按偏好用 `MediaPlayer` 播本地提示音、调 `Vibrator` 振动封装，长按跳步做重触觉；设置页有提示音、振动两个开关；写错：目标的步进函数只改索引、清进度、停表，不读提示音和振动偏好，不播 rawfile 提示音、不调 vibrator.startVibration；占位的 `FWD-REF` 标记被删掉却没写触觉
- rule-ccf26463e052｜源端同步先 cancel 再 vibrate 时，网关用 Promise 队列串行发出停止和振动｜读到：源端同一方法里先同步调用 `Vibrator.cancel()` 再调用 `vibrate(long[] pattern, int repeat)`（或别的 stop 后 start、先释放再创建），后一调用依赖前一调用已生效；写错：目标网关的 void 方法里 `vibrator.stopVibration()` 和 `vibrator.startVibration(...)` 各自发出、只挂 `.catch`，后一调用不等前一调用完成；只核了调用点顺序和源码一致
