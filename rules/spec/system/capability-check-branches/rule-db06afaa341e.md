# 替换能力探测机制时，规格只换判据，源端各返回路径的副作用逐条保留

审的是：规格
触发（任一种）：
- 读到：源端能力探测方法只在 NfcAdapter.getDefaultAdapter(...) 为 null 的分支设置降级标志，其他不支持路径（某芯片、某库缺失）只 return false，由启动流程弹不支持对话框；写错的样子：规格或验收条目写「不再区分…诱因，所有不支持场景统一收敛为…」，把只属于一个分支的副作用扩到全部不支持场景
适用范围：规格提取阶段，把源端设备能力探测换成目标端判据（如 syscap 检查）时
做法：
- 规格按源端返回路径逐条写：哪个条件下设标志、哪个条件下只返回 false 并由后续流程提示；目标判据（如 canIUse(syscap)、适配器是否存在）只替换各分支的判断条件，不合并分支结果
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- NfcAdapter.getDefaultAdapter(context) 在没有 NFC 适配器时返回 null：源端「无适配器」分支的判据（出处：android.nfc.NfcAdapter#getDefaultAdapter）
- canIUse(syscap: string): boolean：目标端按系统能力判断的判据（出处：鸿蒙 SDK 的 ets/api/@internal/full/global.d.ts，canIUse）
未核实：卡里的环境是 HarmonyOS SDK 6.1.1(24)，canIUse 按本机 API 23 的声明核实
来源：1 张卡，1 个应用
- case-e5655934c3f8870c44d9（MifareClassicTool）：做法第 1 步 ← 建议 3
