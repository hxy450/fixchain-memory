# DAO 读写里的加解密钩子

agent 会看到什么：读到安卓 DAO 的读写方法里无条件 encrypt(...) / decrypt(...)，或备份导出导入对 DAO 记录再加解密；产物里 DAO 的加解密钩子 setter（默认恒等或空实现）注入在业务单例 getInstance() 里还是 EntryAbility.onCreate，导出导入任务开始前有没有确保钩子已注入

## 规矩

- rule-5b39685241f2｜数据层钩子替代源端无条件加解密时，注入放进 EntryAbility.onCreate，不挂单例 getInstance｜读到：安卓 DAO 的读写方法里无条件直接调用加解密（写入时 encrypt(...)、读出时 decrypt(...)），源端没有「未注入」状态；目标 DAO 由基座留了钩子 setter，默认值是恒等/空实现；写错：钩子的 setter 注入写在某个业务单例 getInstance() 的首次构造分支里，EntryAbility.onCreate 里没有这次注入
- rule-8be8997c11c9｜钩子默认是恒等实现时，依赖 DAO 加解密的备份导出导入任务开始前先确保钩子已注入｜读到：源端导出时对 DAO 读出的明文记录再 encrypt(...)、导入时先 decrypt(...) 再交给 DAO 写回；目标 DAO 的钩子默认值是恒等/空实现；写错：目标端导出/导入任务直接调 DAO 的读写方法，开始前没有确保钩子已注入（没有先行调用注入入口，也没有在未注入时 `throw`）
