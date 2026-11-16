# 转换器造成的共享资源缺陷

agent 会看到什么：页面 worker 判定共享资源错在转换器（如 converter used dp size as viewBox），回执只写「修复 N 处 SVG viewBox 错配」，编排记录里记成顺手修复，没有全量审计

## 规矩

- rule-3e40bd03a346｜worker 发现共享资源是转换器的同类缺陷时，回执写系统性根因和范围，编排者安排全量审计｜读到：页面 worker 判定共享资源错在转换器（如「converter used dp size as viewBox instead of viewport」）；写错：回执只写「修复 N 处 SVG viewBox 错配」，没写转换器的系统性根因和疑似范围；编排记录里记成顺手修复，没有全量审计或重跑脚本的任务
