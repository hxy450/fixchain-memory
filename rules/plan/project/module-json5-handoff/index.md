# module.json5 配置项的移交

agent 会看到什么：派工、移交、返回信封或切片账本涉及 module.json5 的 requestPermissions（INTERNET）、extensionAbilities 注册、shortcuts 入口配置，而这个文件不在本任务的写权内，或写法没核实就写成确定指令

## 规矩

- rule-941c6d22263a｜网络层任务的写权限不含 module.json5 时，返回信封要把网络权限列为跨文件改动草稿｜读到：派工把写权限限定在网络层目录；检查清单或代码模板注释写着「前置：必须在 module.json5 声明 INTERNET」；写错：返回信封的风险、登记项、跨文件改动里都没有 module.json5 的 ohos.permission.INTERNET，只在代码注释或自查清单里提到
- rule-940bd11aa17e｜移交和派工里的 module.json5 注册说明要与基类对应，未核实的字段标待核｜读到：扩展能力的源文件 extends AppServiceExtensionAbility，或编译时换过扩展基类；写错：handoff 或派工里写着 extensionAbilities 注册 type=service、backgroundModes 等字段，与基类不对应，或没核实就写成确定指令
- rule-ec5f9a96db91｜规格里带裁决的入口配置 AC 进切片账本时，列入 integration_points / wires 并指定写者｜读到：规格的验收条目或替代路径写明「入口配置由 module.json5 shortcuts 承担」，并标明是裁决；写错：切片账本的 integration_points / wires 里没有入口接线这一项，或列了却没指定写者
- rule-80cc5e357afc｜移交 module.json5 配置缺口时，按所用 skill 的检查清单抄全，含后台播放两项｜读到：所用 skill 的 module.json5 检查清单要求 backgroundModes: [audioPlayback] 和 ohos.permission.KEEP_BACKGROUND_RUNNING；派工的写盘边界不许改 module.json5；写错：交给收尾者的 module.json5 移交项（deferred-work）只列 skills 和运行时权限（如 ohos.permission.MICROPHONE），没有 backgroundModes: [audioPlayback] 和 ohos.permission.KEEP_BACKGROUND_RUNNING
