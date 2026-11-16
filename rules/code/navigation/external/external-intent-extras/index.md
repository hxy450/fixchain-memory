# 外部应用拉起时 Intent extras 里的协议键

agent 会看到什么：读到源 Activity 在 onCreate 里从 getIntent() 读外部协议的 action 和 extras（IMAGE_CAPTURE、VIDEO_CAPTURE、CAMERA_FACING 一类），规格 AC 或映射列了键名、取值域和优先级；产物里 want.parameters 的解析代码多了源码没有的键、漏键，或类型、取值域和短路顺序不符

## 规矩

- rule-6291292c3852｜实现外部协议键前，grep 规格 AC 和源码对应行，逐键核对键名、类型、取值域与短路顺序｜读到：源 Activity 在 `onCreate` 里从 `getIntent()` 读外部协议 extras（如 `CAMERA_FACING`、`LENS_FACING_FRONT`、`LENS_FACING_BACK`、`USE_FRONT_CAMERA`），规格 AC 或实现映射列了键名、取值域和优先级；写错：want 解析代码里出现源码没有的键（凭记忆补的别名），或漏键、类型和取值域不符（任意 number 都按 `=== 1` 判），注释却写「原串保留」
