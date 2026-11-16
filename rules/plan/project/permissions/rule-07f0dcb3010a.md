# 派工接入 OAID 采集时，把 module.json5 和字符串资源一起划进写域

审的是：计划与派工
触发（任一种）：
- 读到：任务要接入 identifier.getOAID（需要 APP_TRACKING_CONSENT 权限）；写错的样子：派工说明的写域只列服务代码文件，没有 module.json5 和 base / en_US 的 string.json，权限声明只能被记成缺口
适用范围：给接入 OAID 采集的任务写派工说明时
做法：
- 写域里同时列服务代码、module.json5（requestPermissions）和 base、en_US 的 string.json（权限理由），让权限声明、理由文案和申请代码同批完成
来源：1 张卡，1 个应用
- case-5c6be3ec08184086fd79（DeepAI全能PPT）：做法第 1 步 ← 建议 2
