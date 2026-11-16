# 系统省流量开关（Data Saver）和计费网络判定

agent 会看到什么：读到源端经 ConnectivityManager 按系统 Data Saver 开关（RESTRICT_BACKGROUND_STATUS_ENABLED）判定的档位；产物里改成按 NET_CAPABILITY_NOT_METERED、getNetCapabilities 判计费网络

## 规矩

- rule-64b7855d970b｜源端条件受系统开关限制而目标读不到时，按开关默认态退化，不改用计费网络判定｜读到：源端 Auto 档只按系统 Data Saver 开关判定（经 connectivityManager）；写错：目标把 Auto 改成「没有 NET_CAPABILITY_NOT_METERED 即计费网络 → 开启」
