# 构建结果为 FAILED 时，CHECK-1 只能记 FAIL 并列剩余错误，不记「仅警告」

审的是：计划与派工
触发（任一种）：
- 读到：构建输出 BUILD FAILED 或 COMPILE RESULT:FAIL；错误文件开头几行全是 WARN（如 @Entry + export 不推荐）；写错的样子：CHECK-1 写成「⚠️ 部分通过」「仅 ArkTS 语法警告」，并 mark-stage 进入下一阶段
适用范围：验收阶段记录编译检查 CHECK-1 的结论时
做法：
- 读完整 ERROR 列表：按 ERROR 过滤，或读 COMPILE RESULT 汇总行（如 ERROR:6 WARN:7），不只截前 N 行
- BUILD FAILED 或 COMPILE RESULT:FAIL 时 CHECK-1 记 FAIL 并列出剩余错误，继续按 hmos-fix-build-errors 循环修复，不 mark-stage
来源：1 张卡，1 个应用
- case-11c15d99c36e52d8aa59（星途清单）：做法第 1 步 ← 建议 3；做法第 2 步 ← 建议 4、诊断
