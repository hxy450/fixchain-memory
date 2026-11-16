# 按值表索引的 SeekBar 进度

agent 会看到什么：读到源端先建刻度值表，再 SeekBar.setMax(values.size() - 1)、setProgress(索引)，步进按索引 ± 1 移动；产物里 Slider 的 max、value 由谁赋值，步进函数改的是索引还是偏好值

## 规矩

- rule-2c3453d02bf7｜移植「建表+setMax+setProgress」的滑杆工具时，上限和初始进度一起写入状态并实际调用｜读到：源端滑杆工具先建刻度表，再 SeekBar.setMax(values.size() - 1)、setProgress(最近一档)，调用点在相机就绪回调里；写错：移植成只返回进度的函数，新增的上限状态初值 0 没有赋值者，Slider 的 max 恒为 0 或 Math.max(1, 0)
- rule-e70a886b8010｜声称与源端步进入口等价前先读源实现，曝光补偿按滑杆值表索引步进，不直接改偏好值｜读到：源端曝光补偿 SeekBar 的值表在 0 处重复多格，步进按 setProgress(索引 ± 1) 移动并跨过重复的零；写错：注释写「等价源端 changeExposure 一类方法」，代码却直接对曝光补偿偏好值 ±1
