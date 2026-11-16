# 源端的整应用重启（System.exit、startActivity 后退出进程）

agent 会看到什么：读到源端方法体 System.exit(0)、注释「Performs a full app restart」，或恢复、导入的库实现里 startActivity 后 System.exit 重启应用；产物里对应处只有 terminateSelf()、只弹 showToast，没有 restartApp

## 规矩

- rule-228b2bff48af｜源端用 System.exit(0) 做整应用重启时，目标用 restartApp，失败再 terminateSelf｜读到：方法注释「Performs a full app restart」、方法体 System.exit(0)，调用点是语言切换、恢复或重置数据、通知点击一类；写错：目标重启方法体只有 context.terminateSelf()，注释写「忠实迁移 = 退出应用，不附加重启」一类
- rule-0a2eae3a4ee1｜源端恢复后重启应用时，目标端导入成功后也重启应用，不只弹 Toast｜读到：源端 import(ctx, uri, true) 的库实现在恢复后 startActivity + System.exit 重启应用；写错：目标端导入成功后只调 showToast(...)，没有重启应用
