# module.json5 的 querySchemes

agent 会看到什么：源端用 Intent 拉起外部应用（geo:、mailto:、tel: 等 URI）并在拉起前查可用性，目标代码调了 bundleManager.canOpenLink；entry 模块 module.json5 的 module.querySchemes 里有没有登记这些 scheme

## 规矩

- rule-c020f2d111e1｜代码用 canOpenLink 探测某个 scheme 时，在 querySchemes 里登记它｜读到：源端用 Intent 拉起外部应用（geo:、mailto:、tel: 等 URI），拉起前查可用性；写错：代码里调了 bundleManager.canOpenLink，entry 模块 module.json5 的 module.querySchemes 没有对应 scheme
