# 源端能力探测的分支和不支持、外跳路径

agent 会看到什么：读到源端入口先判 NfcAdapter.getDefaultAdapter() 为 null、再判 isEnabled()、不支持时弹对话框、按钮发 market:// 或 Settings.ACTION_NFC_SETTINGS 的 Intent 并带失败回退；规格把这些分支收成一个 isAvailable()、统一收敛为说明文本，或把一个分支的副作用扩到全部

## 规矩

- rule-9351b433d1b8｜源码能力检查分不支持、开关关闭、可用时，规格的接口、状态和验收逐个列出｜读到：源码入口先判 NfcAdapter.getDefaultAdapter() 为 null 提示不支持，再判 isEnabled() 为 false 时 startActivity(Settings.ACTION_NFC_SETTINGS)，否则进入功能页；写错：规格的服务接口只有一个 isAvailable()，状态枚举没有关闭态（disabled），验收条款只写「不支持时提示且不导航」，没有「NFC 关闭→打开系统 NFC 设置页」
- rule-db06afaa341e｜替换能力探测机制时，规格只换判据，源端各返回路径的副作用逐条保留｜读到：源端能力探测方法只在 NfcAdapter.getDefaultAdapter(...) 为 null 的分支设置降级标志，其他不支持路径（某芯片、某库缺失）只 return false，由启动流程弹不支持对话框；写错：规格或验收条目写「不再区分…诱因，所有不支持场景统一收敛为…」，把只属于一个分支的副作用扩到全部不支持场景
- rule-c5471ffb8c6a｜平台做不到的只收敛那一步，源端外跳按钮和失败回退链在规格里照原样保留｜读到：源端对话框按钮发 market://details?id=… 的 Intent、ActivityNotFoundException 时转 https 网页，startActivity(new Intent(Settings.ACTION_NFC_SETTINGS))，或拉起其他应用；同一流程里另有查询他包安装、运行状态的判断；写错：规格的平台差异决策把整条分支改成「说明文本」「设置主页或引导文案」，删掉商店跳转、拉起他应用或设置深链按钮，并作废对应的验收条目
