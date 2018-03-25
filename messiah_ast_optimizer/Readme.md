1.Constant Inline: 常量内联
2.Small Function Inline: 小函数内联


# mark
1. 多文件联合的怎么搞？
2. 怎样加速， os.walk多进程扫描？


1.Component: 需要根据其他文件来合并Component Class, 因而其他文件必须先进行了其他step优化的。
			1）选择在visitor自动分析component的内容
			2）通过配置表人工配置

2.如果建立一个架构让跨表、依赖关系的更加便捷

3.多次执行分析当然没问题，但是这样效率会非常低下，现在已经进行了三次全局扫描


方案1：进行visitor的时候添加依赖关系，通过拓扑排序，最后再transfomer时候按照拓扑排序结果进行遍历
此时方案步骤：
1）tokenize 按照os.walk
2) visit 按照os.walk，添加依赖关系, visit结束后可以根据依赖关系对文件访问进行排序
3）transofrm阶段， 按照拓扑排序结果进行访问

思考：使用方案1Component是不是已经能够实现了？
1）Visitor能否更优化，现在是visit的时候就确定const内容，能否做到利用上一次的结果，比如const.A = 100 * 100, 现在是不会判定为const的，但是经过其他step优化会变成const.A = 10000,这时是可以进行优化的
2） 看下fatoptimizer是如何做到优化传递的



1. 实现multiprocessing或者multithreading的visitor和tokenizer，属性如何同步， 与现有框架冲突
2. 设计namespace框架
2. 设计添加文件依赖的框架
3. 执行transformer之前进行拓扑排序


fatoptimier namespace实现方案
1）fullvisit 重新设置命名空间
2）postvisit, previsit, midvisit



2018.3.19
合并Componennt：能合并则合并，不能则抛错不处理
hotfix加工具

1) pylint
2) astroid


# class Optimizer(object):
# 	def __init__(self):
# 		self.tokenize_data = {}
# 		self.visitor_data = {}


# class Tokenizer(object):
# 	def __init__(self):
# 		pass

# 	def enter(self):
# 		"""執行tokenize"""
# 		pass

# 	def exit(self):
# 		"""退出tokenize"""
# 		pass


# 問題在於@Optimize在Meta之後！！！
#  


1.改为使用astroid，确认两个问题
1）怎样组织visitor， transformer
2）import_module怎么指定