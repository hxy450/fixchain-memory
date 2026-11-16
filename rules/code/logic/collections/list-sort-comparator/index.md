# 列表排序的 Comparator 和排序偏好

agent 会看到什么：读到源端列表用自己的 Comparator 在 Collections.sort / List.sort 里排序、或排序时读 SharedPreferences 里的排序偏好，产物里是查询结果上的 .sort(比较函数) 和排序配置的读取

## 规矩

- rule-aa379c101f0c｜新列表数据路径要排序时，照源端该列表自己的 Comparator 写，不复用同文件别的列表的比较函数｜读到：源端这个列表有自己的 Comparator 实现（如待办列表：未完成在前、同状态按创建时间降序），在 Collections.sort 或 List.sort 里使用；写错：目标新增的查询直接照搬同文件里另一个列表的 .sort(比较函数)，排序键和方向与源端该列表的排序器不同
- rule-816575838a0c｜偏好类设置落地后，读它的列表查询要真有调用点，比较函数不能写死排序｜读到：源端列表排序时读取用户的排序偏好（经某个 Helper 的 getter 或 SharedPreferences.getString 取出）；写错：目标的排序配置键或加载函数在仓库、查询服务里没有调用点；列表的 .sort() 比较函数写死排序顺序
