# 原始文件（rawfile）

源工程 src/main/assets 下有音频、预置数据等文件，代码用 AssetManager、openFd 按文件名读；目标端有 resources/rawfile 和 getRawFd 时

## 触发族

- [源 assets 下的文件迁到 rawfile](rawfile-assets/index.md)（3 条）：源工程 src/main/assets（含依赖模块）下有音频、预置数据 JSON 等，代码按文件名用 AssetManager / openFd 读；目标 resources/rawfile 下缺文件、getRawFd 的文件名对不上，或拷进去的数据没写覆盖范围
