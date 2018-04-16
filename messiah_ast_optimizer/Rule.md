#### Global
1) 只允许使用新式类


#### Component Optimizer
1）作为Component的Module定义的Global内容会被合并到Host
2）如果Component的Module的Globals和已合并的Component有重名的定义，除非是相同的Import或者是ImportFrom，否则合并将会调过并报警告信息
eg: Component A: from Model import Model
	Component B: import Model
	两个Component的Model含义不一样，则调过合并Component B

3) 如果Component存在Class Attr和FunctionDef重名, 调过合并并抛建议修改信息
4）若有除Class Attr、FunctionDef、Property以外的其他AstNode， 调过合并并抛建议修改信息
5）如果Component存在Meta，装饰器等，调过合并， 抛提示信息
6）Component里面定义的内容，除了函数外不允许存在同名， 否则抛错



需要重新整理合并Component
1) SoundManager的init_component参数个数为0
2) 各个Component有引用Globals AvatarMember
3)_host_fini没有参数
4) inquirePriceMoneyCb
5) 把合并的Globals改为import形式