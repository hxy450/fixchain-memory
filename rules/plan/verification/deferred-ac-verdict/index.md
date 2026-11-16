# 同会话已记为未接线或 deferred 的 AC 的验证判定

agent 会看到什么：同一会话里已记录某条 AC「未接线」或 deferred（如深色模式未接线）；环境降级时批量写的 impl-claims / verification 仍把它判 pass（静态代理检查），标侧文件不存在或 DarkColors 没有任何消费点

## 规矩

- rule-c38a4045551c｜验证时同会话已记为未接线或 deferred 的 AC 不判 pass，主题 AC 要查标侧文件和深色板消费点｜读到：同一会话里已记录「深色模式未接线」或把该 AC 记为 deferred；写错：环境降级时批量写的 impl-claims / verification 把这个 AC 判为 pass（静态代理检查），标侧文件不存在或 DarkColors 没有任何消费点
