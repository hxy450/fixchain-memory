# 指向应用自身的包名（getPackageName、APPLICATION_ID）

agent 会看到什么：读到源端用 getPackageName()、BuildConfig.APPLICATION_ID 或 Intent 的 setPackage / ComponentName 指向应用自身；产物里 Want 的 bundleName 写成 'com.example.…' 字面量，或另起、跨文件复制包名常量

## 规矩

- rule-78e13d8197fb｜代码里要包名时用 context.abilityInfo.bundleName，不写字面量常量｜读到：源端用 getPackageName()、BuildConfig.APPLICATION_ID 或 Intent 的 setPackage / ComponentName 指向应用自身；写错：Want 里写 bundleName: 'com.example.…' 这类字面量，或另起常量（如 HOST_BUNDLE_NAME）保存包名、跨文件复制别人的常量
