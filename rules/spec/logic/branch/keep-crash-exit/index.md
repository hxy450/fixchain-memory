# 照源保留的崩溃退出

agent 会看到什么：源端有会抛未捕获异常的路径（整数除零、数组负下标）且没有 setDefaultUncaughtExceptionHandler；规格里「照源复刻崩溃」的条目和 errorManager.on('error') 既定项并存

## 规矩

- rule-cfaaafea3373｜规格照源保留崩溃退出时，不把入口补 errorManager.on('error') 写成既定项｜读到：安卓源有会抛未捕获异常的路径（整数除零、数组负下标），且没有全局未捕获异常处理（没有 Thread.setDefaultUncaughtExceptionHandler）；写错：规格里一边有「throw…使应用崩溃（照源复刻）」的验收项或台账条目，一边写「全局异常观察｜源无对应代码｜EntryAbility.onCreate 补 errorManager.on('error')（工程健壮性既定项）」
