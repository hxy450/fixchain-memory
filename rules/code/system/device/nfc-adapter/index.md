# NfcAdapter 的可用性判断和贴卡入口

agent 会看到什么：读到源端 NfcAdapter.getDefaultAdapter 判空、isEnabled() 判开关、清单 intent-filter 带 android.nfc.action.TECH_DISCOVERED；交回的只有一个 isAvailable 布尔门、降级标志在每种缺失下都置位，或 EntryAbility 不读 want 里的 TagInfo

## 规矩

- rule-0804898ce3fb｜源端分不支持和 NFC 关闭两支时，目标服务层拆开判断，关闭态打开系统 NFC 设置页｜读到：源码 NfcAdapter 为 null 时提示不支持，isEnabled() 为 false 时 startActivity(Settings.ACTION_NFC_SETTINGS)；写错：目标只有一个 isAvailable() 布尔门：canIUse 失败、nfcController.isNfcOpen() 为 false 和异常都返回 false，ViewModel 一律置 UNSUPPORTED 并提示不支持，没有打开设置页的入口和关闭态文案
- rule-be070f564a77｜用 canIUse 等换掉能力探测时，只在源端设标志的那个分支设标志，其余缺失只返回 false｜读到：源端只在 NfcAdapter.getDefaultAdapter(...) 为 null 时设降级标志，其他不支持路径 return false；写错：目标在 canIUse('SystemCapability.Communication.NFC.Tag') 不成立或适配器缺失任一情况下都调用同一个降级标志的 setter 置 true，注释引用「统一收敛」的验收条目
- rule-09521abbb9f4｜有系统贴卡入口时，onCreate 和 onNewWant 里用 tag.getTagInfo 取标签｜读到：清单 intent-filter 带 android.nfc.action.TECH_DISCOVERED，被拉起的 Activity 是 singleTop，贴卡时以带 tag 的 intent 拉起或送达；写错：EntryAbility 的 onCreate 不读 want 里的 TagInfo，也没有 onNewWant；只在页面里做 tag.on / registerForegroundDispatch 前台注册
