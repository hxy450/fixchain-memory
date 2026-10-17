# data/preferences

偏好键值存储：装载时机与同步读写、批量提交原子性、读点缺省值与默认值落盘

[上一级](../index.md)

## 本级经验

- [偏好入口同步装载，读写走 Sync 接口](lesson-93b3eeff61598bc42172.lesson.md) · 阶段：spec/plan/execute · 信号：getSharedPreferences, PreferenceManager.getDefaultSharedPreferences, getPreferencesSync, getPreferences
- [同键多读点缺省不同时逐读点保留，不收敛为单一默认](lesson-11e4e15acdbadf579e07.lesson.md) · 阶段：spec/execute · 信号：getBoolean, getString, getXxx
- [批量 commit 改为先暂存校验再 putSync](lesson-24bc4929b771a9a33ef4.lesson.md) · 阶段：execute · 信号：SharedPreferences.Editor, editor.putX, putSync, flushSync
- [设置页出现时为缺键写 XML 默认值并落盘](lesson-4283cc343b875489b851.lesson.md) · 阶段：spec/execute · 信号：addPreferencesFromResource, PreferenceFragment, PreferenceActivity, PreferenceScreen
