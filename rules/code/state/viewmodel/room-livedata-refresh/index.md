# Room LiveData 观察的表在目标存储里的刷新

agent 会看到什么：读到源端当前数据来自 Room @Dao 返回的 LiveData，ViewModel 的写方法只写库、靠 LiveData 重新发射；产物里目标存储的每个写方法有没有刷新内存里的 @Trace 当前值并广播

## 规矩

- rule-4dd3a0571bc2｜源端账号表经 Room LiveData 读出时，目标存储的每个写方法都刷新内存状态并广播｜读到：源端当前账号来自 Room @Dao 返回的 LiveData，ViewModel 的写方法（含验证状态）只写库、靠 LiveData 重新发射；写错：目标存储的某个写方法只写库、不刷新内存 @Trace 当前值，注释称「写库但不广播」或「非身份变更」
