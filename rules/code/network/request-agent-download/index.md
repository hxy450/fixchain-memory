# request.agent 的下载任务

agent 会看到什么：读到源端用 OkHttp 或 getInputStream 把文件下到缓存目录，或参考模板按 request.agent.create → on('completed') → start() 落码；产物里有没有调 task.start()，完成和失败回调怎么接

## 规矩

- rule-6706332be130｜request.agent 下载在 create 和注册回调之后要调 task.start()｜读到：源端用 OkHttp 或 getInputStream 下载到缓存；参考模板按 request.agent.create → on('completed') → await task.start() 落码；写错：代码里有 request.agent.create(...) 和 task.on('completed' / 'failed', ...)，却没有 task.start()；后续保存、分享、复制一直等不到完成
