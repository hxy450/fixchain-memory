# Cursor 按文本读回的数值列

agent 会看到什么：读到源端 cursor.getString(i) 读 REAL（浮点）列再交给 String 入口解析；产物里 relationalStore 的 ResultSet 同样用 rs.getString(idx) 读这一列

## 规矩

- rule-33473ff9bb79｜源端 Cursor.getString 读 REAL 列时，迁到 ResultSet 按 %g 复刻文本｜读到：源码用 `cursor.getString(i)` 读回 REAL（浮点）列，再交给 String 入口解析；写错：目标端 relationalStore 里同样用 `rs.getString(idx)` 读 REAL 列，得到全精度文本，和 Android 的文本不同
