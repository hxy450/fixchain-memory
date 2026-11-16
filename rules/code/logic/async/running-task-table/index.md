# 按键登记的在途任务表

agent 会看到什么：读到源端 JobService 的 onStartJob / onStopJob 和 jobs.remove(jobId)，或规格写同一 Job ID 先 cancel 旧 handle 再写入；产物里 Map<number, TaskHandle> 运行表在任务 finally 里无条件 running.delete(workId)

## 规矩

- rule-33be6e081e81｜同键覆盖前先取消旧任务时，清理运行表按句柄身份比对，不按键无条件删除｜读到：规格写同一 Job ID 连续触发时显式 cancel 旧 handle 再写入、不变式「同一 workId 最多一个 running 实例」；源端 JobService 用 jobs.remove(jobId)；写错：任务结束的 finally 里无条件 running.delete(workId)（运行表是 Map<number, TaskHandle>），被取消的旧任务晚到时把新 handle 删掉
