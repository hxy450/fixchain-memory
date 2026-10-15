# app/settings

设置项迁移：偏好键与默认值之外，每个开关的运行期消费方与应用入口；设置保存的副作用（远端、本地缓存、刷新事件）与切换即持久化界面状态的恢复，应用内语言切换的即时生效

[上一级](../index.md)

## 本级经验

- [源端 SharedPreferences.Editor 累积 put 后一次 commit 的流程（恢复、导入），目标先暂存、全部校验通过后再 put 并 flush：preferences.putSync 立即改共享实例，中途失败不能留下部分写入](lesson-24bc4929b771a9a33ef4.lesson.md)
  - 时机：数据层实现阶段，迁移 Editor 批量写入后 commit/apply 的恢复或导入流程时
  - 情境：源端遍历输入逐键 editor.putX，遇到未知键或格式错误时抛出，末尾才 commit；目标准备逐键 putSync 到共享 preferences 实例。
- [设置页由 addPreferencesFromResource/PreferenceFragment 挂载时，缺持久值的偏好会写入 android:defaultValue：目标在设置页出现时按 XML 顺序为缺键补写默认值并落盘，不只在读取时回退默认](lesson-4283cc343b875489b851.lesson.md)
  - 时机：规格提取与设置页实现阶段，迁移带 android:defaultValue 的 PreferenceScreen XML 时
  - 情境：源设置页由 PreferenceFragment/PreferenceActivity 以 XML 挂载偏好，各项有 defaultValue；目标偏好服务只在读取时回退默认值；偏好文件内容会被备份等流程读取。
- [迁移设置开关、设置保存与持久化的界面状态时为每项落实运行期消费方：只调持久化 setter、只写远端设置不算完成](lesson-4d0f0176b3d09c33f1eb.lesson.md)
  - 时机：功能接线阶段实现设置页开关与偏好仓库，或页面转换遇到按偏好切换的渲染与行为分支时；迁移设置页的保存逻辑，或切换即持久化的界面状态（如首页视图位置）时
  - 情境：源端设置用 DataStore/SharedPreferences 持久化，并被主题、计时器、反馈等运行期代码实时读取；目标端的设置页、偏好仓库、主题状态和消费页面由不同任务编写，靠占位登记传递“持久化并立即生效”的契约。也包括源端设置保存除远端同步外还更新本地配置缓存并发刷新事件（如排序设置保存后各列表按新配置排序），目标只写远端设置；以及源端切换视图即写偏好、启动时读取恢复，目标只改内存状态。也包括应用内语言选择只调用持久化的偏好语言接口，而规格要求保存后立即切换。
