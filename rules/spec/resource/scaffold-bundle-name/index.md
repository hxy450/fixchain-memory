# 脚手架身份的 bundleName

agent 会看到什么：目标 app.json5 还是 com.example.myapplication 脚手架身份，源 applicationId 在 com.example.* 下；决策台账里的身份技术项

## 规矩

- rule-d7bb21fb2857｜登记模板身份技术项时写明哪个阶段写 bundleName，源包名为 com.example.* 时提前登记例外｜读到：目标 app.json5 是脚手架身份（com.example.myapplication / example）；源 applicationId 位于 com.example.* 或组织段是 example；写错：决策台账的身份技术项只写「迁移真实身份」，没写由哪个阶段、以哪种 scope 写 bundleName/vendor；源包名在 com.example.* 下却没登记验证例外
