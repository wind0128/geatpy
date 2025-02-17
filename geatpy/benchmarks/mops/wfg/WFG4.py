# -*- coding: utf-8 -*-
import numpy as np
import geatpy as ea


class WFG4(ea.Problem):  # 继承Problem父类
    def __init__(self, M=3, Dim=None):  # M : 目标维数；Dim : 决策变量维数
        name = 'WFG4'  # 初始化name（函数名称，可以随意设置）
        maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        if Dim is None:
            Dim = M + 9  # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0] * Dim  # 决策变量下界
        ub = list(range(2, 2 * Dim + 1, 2))  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim  # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 目标函数中用到的一些参数设置
        self.K = self.M - 1
        self.L = self.Dim - self.K
        self.S = np.array([list(range(2, 2 * self.M + 1, 2))])
        self.D = 1
        self.A = np.ones((1, self.M - 1))

    def evalVars(self, Vars):  # 目标函数
        N, Lind = Vars.shape
        M = self.M
        K = self.K
        L = self.L
        S = self.S
        D = self.D
        A = np.tile(self.A, (N, 1))
        Z = Vars / np.array([range(2, Lind * 2 + 1, 2)])
        t1 = s_multi(Z, 30, 10, 0.35)
        t2 = np.zeros((N, int(K + L / 2)))
        t2[:, :K] = t1[:, :K]
        t2[:, K: int(K + L / 2)] = (t1[:, K:: 2] + t1[:, K + 1:: 2] + 2 * np.abs(t1[:, K:: 2] - t1[:, K + 1:: 2])) / 3
        t2 = np.ones((N, M))
        K_divide_M_sub_1 = int(K / (M - 1))
        for i in range(1, M):
            t2[:, i - 1] = r_sum(t1[:, list(range((i - 1) * K_divide_M_sub_1, i * K_divide_M_sub_1))],
                                 np.ones((1, K_divide_M_sub_1)))
        t2[:, M - 1] = r_sum(t1[:, K: K + L], np.ones((1, L)))
        x = np.zeros((N, M))
        for i in range(1, M):
            x[:, [i - 1]] = np.max([t2[:, [M - 1]], A[:, [i - 1]]], 0) * (t2[:, [i - 1]] - 0.5) + 0.5
        x[:, [M - 1]] = t2[:, [M - 1]]
        h = concave(x)
        f = D * x[:, [M - 1]] + S * h
        return f

    def calReferObjV(self):  # 设定目标数参考值（本问题目标函数参考值设定为理论最优值，即“真实帕累托前沿点”）
        N = 10000  # 设置所要生成的全局最优解的个数
        Point, num = ea.crtup(self.M, N)  # 生成N个在各目标的单位维度上均匀分布的参考点
        Point = Point / np.sqrt(np.sum(Point ** 2, 1, keepdims=True))
        referenceObjV = np.array([list(range(2, 2 * self.M + 1, 2))]) * Point
        return referenceObjV


def s_multi(x, A, B, C):
    return (1 + np.cos((4 * A + 2) * np.pi * (0.5 - np.abs(x - C) / 2 / (np.floor(C - x) + C))) + 4 * B * (
            np.abs(x - C) / 2 / (np.floor(C - x) + C)) ** 2) / (B + 2)


def concave(x):
    return np.fliplr(np.cumprod(np.hstack([np.ones((x.shape[0], 1)), np.sin(x[:, :-1] * np.pi / 2)]), 1)) * np.hstack(
        [np.ones((x.shape[0], 1)), np.cos(x[:, list(range(x.shape[1] - 1 - 1, -1, -1))] * np.pi / 2)])


def r_sum(x, w):
    Output = np.sum(x * w, 1) / np.sum(w)
    return Output
