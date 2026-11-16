# 登记模板身份技术项时写明哪个阶段写 bundleName，源包名为 com.example.* 时提前登记例外

审的是：规格
触发（任一种）：
- 读到：目标 app.json5 是脚手架身份（com.example.myapplication / example）；源 applicationId 位于 com.example.* 或组织段是 example；写错的样子：决策台账的身份技术项只写「迁移真实身份」，没写由哪个阶段、以哪种 scope 写 bundleName/vendor；源包名在 com.example.* 下却没登记验证例外
适用范围：规格或决策阶段登记 App 身份迁移技术项时
做法：
- 技术项里写明哪个阶段、以哪种 scope 写 AppScope/app.json5 的 bundleName 和 vendor
- 源 applicationId 在 com.example.* 下或组织段为 example 时，同时登记验证例外（忠实迁移的身份按规则字面会 FAIL）
来源：1 张卡，1 个应用
- case-6c4ad933f56919279698（NoteKeeper）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 3、诊断
