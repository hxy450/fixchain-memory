# 派工里的编译安排（禁止 worker 编译）

agent 会看到什么：派工说明写了禁止 worker 自行编译（「Do NOT run hvigor builds」「由主线程做最终构建」），却没要求对照导入名与导出名，也没安排收报告前的编译门

## 规矩

- rule-9c18d31d155d｜派工禁止 worker 编译时，要写明导入名与导出名的静态对照，并在收报告前跑编译门｜写错：派工写了禁止 worker 自行编译（如「Do NOT run hvigor builds」「由主线程做最终构建」），却没要求 worker 对照导入名与导出名，也没安排主线程在接受报告前跑一次编译门
