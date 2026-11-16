# 相机会话和录像输出的拆卸与释放

agent 会看到什么：读到源端在后台线程阻塞执行 Camera.stopPreview()、Camera.release()，或 MediaRecorder.release 之后 reconnect 相机；产物里 session.stop / release、cameraInput.close、各 output 的 release 有没有按顺序 await，拆卸 hook 是不是 () => void，重建会话前有没有 beginConfig + removeInput

## 规矩

- rule-31896aa1b3ca｜源端后台阻塞关相机时，目标释放返回 Promise，按输出、会话、输入逐步 await｜读到：源端在后台线程（AsyncTask 等）里阻塞执行 Camera.stopPreview() 和 Camera.release()，完成后才置为已关闭并回调或重开；规格写「异步关闭完成后回调，reopen 时重开」；写错：session.release()、cameraInput.close()、各 output 的 release() 只接 .catch( 不 await，释放方法签名是 void；或用 Promise.resolve().then(...) 包住 void 的释放调用冒充后台任务
- rule-cd84ac251f25｜录像输出的挂接和拆卸 hook 都返回 Promise，调用方先 await 拆卸再释放录制器｜写错：挂接 hook 是 async 并被 await，拆卸 hook 却定义成 () => void；拆卸插在 recorder.release() 之后，或拆卸里 session.stop()、output.release() 只发起不等待
- rule-2c57ce0bcbb6｜会话重建要复用同一 CameraInput 时，释放旧会话前先 beginConfig 再 removeInput｜写错：拆旧会话时直接 await session.stop() 再 await session.release()，没有先 session.beginConfig() + session.removeInput(cameraInput)，随后新会话又 addInput 同一个 cameraInput
