# 资源 HARD-GATE 和页面转换器的派出时机

agent 会看到什么：执行规程要求 Stage 0 资源 HARD-GATE 先跑，Stage 0 还在运行时就派出了页面转换器，派工里没写资源仍在迁移

## 规矩

- rule-bf821236956a｜资源 HARD-GATE 通过前不派页面转换器；必须并行时派工写明资源仍在迁移｜读到：执行规程要求 Stage 0 资源 HARD-GATE 先跑；写错：Stage 0 还在运行时就派出页面转换器，派工里没写资源仍在迁移、以 Stage 0 回报为准
