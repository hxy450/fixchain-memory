# 布局方向镜像（RTL）的全局约定

agent 会看到什么：ui-manifest 全局约定里有布局方向镜像（RTL）要求，或源清单 android:supportsRtl="true"；写界面的 worker 的派工说明里没有布局方向镜像、start/end 边距这一条

## 规矩

- rule-5e180f948553｜全局约定登记了布局方向镜像时，每个 UI worker 的派工都带上这一条｜读到：ui-manifest 全局约定里有布局方向镜像（RTL）要求，或源清单 android:supportsRtl="true"；写错：写界面的 worker 的派工说明里没有布局方向镜像、start/end 边距这一条
