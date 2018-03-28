一、设计原则
1.不保证所有都会做，但是保证做的都是正确的
2.scope_lookup必要正确


Walker流程：后序遍历
1）visit children
2) previsitSelf 这个阶段已经visit完孩子，在这个阶段确认node scope等内容, freevars
3）visitSelf， 这个阶段node可能改变
4）postvisitSelf 主要add name, 常量自动计算, isconstant