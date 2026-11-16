# 安卓免权限的系统服务映射后的权限契约

agent 会看到什么：读到源端用 ClipboardManager、NfcAdapter 这类无需运行时权限的系统服务；规格或功能基线写「requestPermissions 为空」「免权限」，没逐个查已映射接口的 @permission

## 规矩

- rule-a71425b92317｜写权限契约前按每个已映射的系统 API 查 @permission，不因安卓免权限就写空｜读到：源端用 ClipboardManager 读剪贴板、NfcAdapter 读标签等无需运行时权限的系统服务；写错：规格或功能基线写「requestPermissions 为空」「…免权限」，没逐个查已映射接口的 @permission（如 pasteboard 的 getData 需要 ohos.permission.READ_PASTEBOARD）
- rule-ada79409a95e｜规格权限节对跨栈映射里每个目标 API 反查 @permission，不只从源 Manifest 推｜读到：源能力在安卓上无需权限，源 Manifest 只有少量或未用的权限；跨栈映射写了 FLAG_SECURE → setWindowPrivacyMode；写错：权限节、决策台账写「目标不声明任何权限」，或静态验收写「module.json5 无 requestPermissions 条目」，没核各目标 API 的 @permission
