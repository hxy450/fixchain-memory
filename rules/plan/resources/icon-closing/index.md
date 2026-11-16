# 收口回报里的图标项

agent 会看到什么：资源迁移或收口回报写着 AppScope 的 app.json5 icon 仍是脚手架 $media:app_icon 并记为「非阻断」，或跑了会改写源码的 icon-sizing 自愈脚本却只报 findings 计数

## 规矩

- rule-79ae323b426b｜能靠复制闭合的 AppScope 图标项不记成「非阻断」附注移交验证，当场改好｜读到：资源迁移的回报把 AppScope 图标交给身份落地这一步，entry 侧已有可直接复制的前景、背景和 layered_image.json；写错：迁移报告或移交清单里写着 AppScope 的 app.json5 icon 仍是脚手架 $media:app_icon、AppScope media 没有图标文件，并记为「非阻断」附注留给验证阶段
- rule-e6ed8c076e27｜收口跑了会改写源码的自愈脚本后，回执要列出它的改动并做量级检查，不能只报 findings 计数｜读到：收口协议写明 pipeline 模式会自动运行 icon-sizing 图标尺寸自愈，它是唯一会改写源码的 detector，改动记录写在 icon-pipeline-iterN.json；写错：收口回执只报 findings 计数和结果文件路径，没有列出脚本改了哪些文件哪些行，也没有对新增尺寸做量级检查就继续派修复
