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
1) Component分析单个模块


#### Constant Optimizer


#### Inline Optimzer
1）装饰器inline
2）Buffs、Pskills的get function Inline
3) 能否利用MonkeyType的功能来进行inline



1) Tick合并
2） 小函数Inline