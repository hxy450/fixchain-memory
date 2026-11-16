# 列表数据源、条目的键和更新后的刷新

agent 会看到什么：读到 Adapter 的 getItemCount、setList / submitList、remove + add + notifyItemChanged、onResume 或回调后改数据、分页追加和返回刷新；产物里 IDataSource 的成员、ForEach / Repeat 的键函数、传给 @Builder 的数据和整表回写

## 规矩

- rule-9ebd586bdafa｜列表以同 id 新实例替换条目时，Repeat/ForEach 的键要随实例变化，不能只含 id｜读到：安卓列表事件处理里 remove(pos) + add(pos, item) + notifyItemChanged(pos)，或整表重载后重新绑定行；写错：Repeat 的 .key(...) 或 ForEach 的 keyGenerator 只含 item.id（或再加选中位、列数等页面状态），数据数组却用 arr[pos] = item、splice(pos, 1, item) 或整表赋值换入同 id 的新实例
- rule-355b6f4417ff｜源端以同 id 新值重建列表再 setList 时，ForEach 的 key 要含所有可变展示字段｜读到：操作成功后重新请求列表并 adapter.setList(...)，新列表条目 id 不变而 count、title 等展示字段变了；写错：ForEach 的 keyGenerator 只用 index 和 item.id（加个别状态位）拼键，不含 count、title 等可变展示字段
- rule-93df7a810dcb｜会被异步更新的展示对象不作多参数 @Builder 的值参，改传整个 @ObservedV2 对象或拆子组件｜读到：源端卡片的数据在页面出现（onResume）或定位回调（onLocationChanged）完成后才更新；写错：普通 class 对象由 @Local 持有，经两个以上参数的 @Builder（如 this.行Builder(this.item, true)）按值渲染，数据更新后卡片不刷新
- rule-b3a7dd1e933a｜分页列表的返回刷新等批量异步查询，按列表代次放弃过期结果、只按 ID 修补当前列表｜读到：源端列表由分页回调追加、下拉时 `clear()` 后替换，`onResume` 不整表刷新；单项状态要逐条 await 本地数据库查询；写错：`onPageShow` 里新增的刷新先 `const current = this.list.slice()`，逐项 await 后 `this.list = current` 整体回写；同文件的分页加载已用请求序号丢弃过期回调，这个入口却没有
- rule-20a14e96b793｜实现 IDataSource 时计数成员写 totalCount()，不写 getTotalCount()｜读到：源端 RecyclerView.Adapter 的 getItemCount()；映射参考只写「RecyclerView.Adapter → LazyForEach + IDataSource」，没列成员；写错：实现 IDataSource 的类写了 getTotalCount()，调用点也用 getTotalCount()
- rule-bf5935ae5ed7｜分页追加依赖 ViewModel 返回的是当页还是累计时，写前重读提供方并按当前语义追加｜读到：编辑工具回执提示 `The file changed since your last read`，或提供方回调里 `result.list` 的赋值和注释（「当页数据，非全量累积列表」）与之前读到的不同；写错：页面上拉加载写成 `dataSource.append(result.list.slice(已有条数))`，注释称 `result.list` 是累计列表，而提供方当前回传的是当页数据
- rule-3cf4eff783c5｜LazyForEach 要整批换数据时保持数据源对象不变，用 onDataReloaded 通知，不重新赋值｜读到：源端用 setAdapter(...) 换一批数据（如排序后换适配器），或延迟后才填充列表数据；写错：目标写 this.数据源 = 新的 IDataSource 实例，整体替换 LazyForEach(this.数据源) 的数据源，排序后行不刷新；或 keyGenerator 只按 index 生成，换数据集后键重复
