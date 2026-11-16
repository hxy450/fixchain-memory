# 基线截图没拍到本体的弹层

agent 会看到什么：读到 Android 基线截图没有拍到弹层展开后的本体，view.xml 是合成的、bounds 为空；视觉校验结论按源结构把这个弹层判为 PASS，弹层内卡片几何没有标为未核

## 规矩

- rule-ba3eb9a94b82｜视觉校验时基线截图没拍到弹层本体、view.xml 无 bounds，弹层内几何标未核，不判 PASS｜读到：Android 基线截图没有拍到弹层展开后的本体，view.xml 是合成的、bounds 为空；写错：校验结论按源结构把这个弹层判为 PASS，弹层内卡片几何没有标为未核
