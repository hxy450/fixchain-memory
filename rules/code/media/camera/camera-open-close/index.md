# 相机的打开、关闭和重开

agent 会看到什么：读到源端相机在 onResume 打开、onPause 关闭，关闭进行中只置 reopen 标志、onDestroy 限时等关闭任务完成；产物里 CameraInput.open / close 的调用、关闭进行中收到的打开请求、aboutToDisappear 里的释放路径

## 规矩

- rule-030f735dd431｜相机关闭中收到打开请求记为待重开，销毁和 aboutToDisappear 走同一条有序关闭路径｜读到：源端关闭进行中 onResume 只置 reopen、关闭完成后再打开；Activity.onDestroy 最多等关闭任务 3000ms；写错：关闭进行中收到的打开相机调用只记日志就返回；aboutToDisappear 里直接调同步的 onDestroy() 强释放，或在已触发销毁序列后又调一次
