# preferences 用的 Context

agent 会看到什么：交回的修复把 preferences 的 context 从 getApplicationContext() 换成 UIAbilityContext（this.context），理由写「更可靠」，没核对两者的 preferencesDir

## 规矩

- rule-ec1623b8e3fa｜偏好存储换上下文前先核对两种 Context 的 preferencesDir，不以「可靠」为理由｜写错：修复把 preferences 的 context 从 getApplicationContext() 换成 UIAbilityContext（this.context），理由写「applicationContext 持久化不如 UIAbilityContext 可靠」
