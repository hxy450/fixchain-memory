# 编译报错后删改的调用和基类

agent 会看到什么：读到编译报错指向承载核心行为的调用或扩展基类（卡片页 .onAreaChange 报 can't support form application、@kit.AbilityKit 没有 ServiceExtensionAbility）；产物里为过编译删了调用或改了 extends，文件头和注释仍写着由它驱动或旧的注册 type，被它赋值的 @State 只剩声明

## 规矩

- rule-367c6dcdc5e4｜为过编译删掉承载核心行为的调用时，同步改掉声称它仍在的注释并回报退化｜读到：编译报错指向承载核心行为的调用，如卡片页的 .onAreaChange( 报 `can't support form application`；写错：调用删了，文件头或注释仍写着由 onAreaChange 之类驱动；被它赋值的 @State 变量只剩声明、再没有赋值
- rule-bf7330299daa｜改了扩展基类后，源文件头注释里的注册说明同步改成对应的 type｜读到：编译报 @kit.AbilityKit 没有 ServiceExtensionAbility（Did you mean AppServiceExtensionAbility），随后把类改为 extends AppServiceExtensionAbility；写错：源文件已 extends AppServiceExtensionAbility，头注释仍写着「extensionAbilities 注册（type=service, backgroundModes=[…]）」
