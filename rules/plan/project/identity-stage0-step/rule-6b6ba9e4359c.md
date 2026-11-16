# Stage 0 的 brief 只记了版本号和 label 时，补记身份 skill 的调用和输出文件再判完成

审的是：计划与派工
触发（任一种）：
- 读到：stage 参考要求 Stage 0 调用 arkts-app-identity（scope=dev-identity）；写错的样子：Stage 0 的 brief 里身份一项只列 versionCode/versionName 和 module.json5 label，没有 skill 的调用记录和输出文件清单；续跑时凭 brief 存在就判定 app-identity 已经跑过
适用范围：Stage 0 收尾、断点续跑判断身份落地是否完成时
做法：
- brief 里记 arkts-app-identity 的实际调用和它写出的文件；按 skill 输出表逐个文件核对（含 startWindowIcon 指向的 startIcon.png 已换成安卓启动图标、EntryAbility_label 与 app_name 一致），不只 grep 版本号和 label
- brief 缺调用记录或缺输出文件时补跑该 skill，不凭 brief 文件存在推断已执行
来源：1 张卡，1 个应用
- case-1f6d95134bba8edf5ba6（jerboa）：做法第 1 步 ← 建议 2、建议 3；做法第 2 步 ← 建议 3
