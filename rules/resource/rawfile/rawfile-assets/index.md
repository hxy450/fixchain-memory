# 源 assets 下的文件迁到 rawfile

agent 会看到什么：源工程 src/main/assets（含依赖模块）下有音频、预置数据 JSON 等，代码按文件名用 AssetManager / openFd 读；目标 resources/rawfile 下缺文件、getRawFd 的文件名对不上，或拷进去的数据没写覆盖范围

## 规矩

- rule-75c75affd86c｜源端从 assets 播放的音频文件，目标要逐个复制到 resources/rawfile，保持文件名｜读到：源工程 src/main/assets（含依赖模块的 assets）下放着按键 mp3，点击处理按文件名播放；写错：目标 resources/rawfile 下没有这些音频，或代码里 getRawFd('…') 的文件名在 rawfile 下找不到
- rule-d47ce77200a2｜把预置数据 JSON 拷进 rawfile 时，交回里写明覆盖范围并和运行期输入比对｜读到：源工程 `assets/` 下按日期等键查表的预置 JSON；写错：原样拷进 resources/rawfile/，交回只写行数和 SHA256 校验，没写覆盖的起止范围，也没和运行期输入域比对
- rule-2b726d120d4d｜本地 HTML 缺 viewport meta 时，在 rawfile 的 HTML 里补上它｜读到：`WebView` 加载 `file:///android_asset/` 下的 HTML，它的 `<head>` 里没有 `<meta name="viewport"`，源端也没调 `setUseWideViewPort(true)`；写错：rawfile 里那份 HTML 的 `<head>` 仍没有 viewport meta；或者 `Web` 上写了 `.metaViewport(false)` 想模拟按 WebView 宽度排版
