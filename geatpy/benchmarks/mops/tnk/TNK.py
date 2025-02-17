# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea


class TNK(ea.Problem):  # 继承Problem父类
    def __init__(self, M=None, Dim=None):  # M : 目标维数；Dim : 决策变量维数
        name = 'TNK'  # 初始化name（函数名称，可以随意设置）
        M = 2  # 初始化M（目标维数）
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 2  # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界
        ub = [np.pi] * Dim  # 决策变量上界
        lbin = [1, 0]  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)

    def evalVars(self, Vars):  # 目标函数
        x1 = Vars[:, [0]]
        x2 = Vars[:, [1]]
        # 采用可行性法则处理约束
        CV = np.hstack([-(x1 ** 2 + x2 ** 2 - 1 - 0.1 * np.cos(16 * np.arctan(x1 / x2))),
                            (x1 - 0.5) ** 2 + (x2 - 0.5) ** 2 - 0.5])

        ObjV = Vars.copy()
        return ObjV, CV
