# extensionAbilities 条目的 type

agent 会看到什么：目标源文件 extends 某个 ExtensionAbility 子类（AppServiceExtensionAbility、WorkSchedulerExtensionAbility 等），module.json5 的 extensionAbilities 里对应条目写的 type

## 规矩

- rule-0c82f088feef｜扩展条目的 type 要与基类对应，AppServiceExtensionAbility 写 appService｜读到：目标源文件 extends AppServiceExtensionAbility（或 WorkSchedulerExtensionAbility）；写错：module.json5 的 extensionAbilities 里该条目写 "type": "service"（或别的与基类不对应的 type）
