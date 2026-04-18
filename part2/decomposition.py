"""
Phan ra Cholesky cho ma tran doi xung xac dinh duong (SPD).

1) Dinh nghia
   Neu A la ma tran SPD, ton tai duy nhat ma tran tam giac duoi L co duong cheo duong
   sao cho:
	   A = L L^T

2) Dieu kien ap dung
   Ma tran dau vao phai la:
   - Vuong (n x n)
   - Doi xung (A = A^T)
   - Xac dinh duong (x^T A x > 0 voi moi x != 0)

3) Chi phi tinh toan
   Phan ra Cholesky can xap xi 1/2 so phep tinh so voi phan ra LU cho ma tran tong quat,
   vi khai thac tinh doi xung cua ma tran SPD. Day la uu diem lon trong bai toan so tri.

4) Cong thuc truy hoi (voi i > j)
   l_jj = sqrt( a_jj - sum_{k=1..j-1}(l_jk^2) )
   l_ij = ( a_ij - sum_{k=1..j-1}(l_ik l_jk) ) / l_jj

Tep nay gom:
- Ham cholesky_custom(A): tu cai dat Cholesky khong dung numpy.linalg.
- Bo unit test (>= 5 test cases), trong do dung NumPy de kiem chung ket qua.
"""

from __future__ import annotations

import math
import unittest

import numpy as np


def cholesky_custom(A: list[list[float]]) -> list[list[float]]:
	"""Tra ve ma tran tam giac duoi L sao cho A = L L^T neu A la SPD."""
	if not A or not isinstance(A, list):
		raise ValueError("Ma tran dau vao phai la ma tran vuong khong rong.")

	n = len(A)
	if any(not isinstance(row, list) or len(row) != n for row in A):
		raise ValueError("Ma tran dau vao phai la ma tran vuong.")

	matrix = [[float(A[i][j]) for j in range(n)] for i in range(n)]

	eps = 1e-12
	for i in range(n):
		for j in range(i + 1, n):
			if abs(matrix[i][j] - matrix[j][i]) > eps:
				raise ValueError("Ma tran phai doi xung.")

	L = [[0.0 for _ in range(n)] for _ in range(n)]

	for j in range(n):
		sum_diag = sum(L[j][k] * L[j][k] for k in range(j))
		diag_value = matrix[j][j] - sum_diag

		if diag_value <= eps:
			raise ValueError("Ma tran khong xac dinh duong.")

		L[j][j] = math.sqrt(diag_value)

		for i in range(j + 1, n):
			sum_off_diag = sum(L[i][k] * L[j][k] for k in range(j))
			L[i][j] = (matrix[i][j] - sum_off_diag) / L[j][j]

	return L


class TestCholeskyCustom(unittest.TestCase):
	def test_case_1_spd_3x3_demo_matrix(self) -> None:
		A = [
			[4.0, 12.0, -16.0],
			[12.0, 37.0, -43.0],
			[-16.0, -43.0, 98.0],
		]
		L = np.array(cholesky_custom(A), dtype=float)
		np_A = np.array(A, dtype=float)
		np_L = np.linalg.cholesky(np_A)

		self.assertTrue(np.allclose(L, np_L, atol=1e-10))
		self.assertTrue(np.allclose(L @ L.T, np_A, atol=1e-10))

	def test_case_2_spd_diagonal_matrix(self) -> None:
		A = [
			[9.0, 0.0, 0.0],
			[0.0, 16.0, 0.0],
			[0.0, 0.0, 25.0],
		]
		L = np.array(cholesky_custom(A), dtype=float)
		np_A = np.array(A, dtype=float)
		np_L = np.linalg.cholesky(np_A)

		self.assertTrue(np.allclose(L, np_L, atol=1e-10))
		self.assertTrue(np.allclose(L @ L.T, np_A, atol=1e-10))

	def test_case_3_spd_4x4(self) -> None:
		A = [
			[25.0, 15.0, -5.0, 10.0],
			[15.0, 18.0, 0.0, 6.0],
			[-5.0, 0.0, 11.0, 2.0],
			[10.0, 6.0, 2.0, 29.0],
		]
		L = np.array(cholesky_custom(A), dtype=float)
		np_A = np.array(A, dtype=float)
		np_L = np.linalg.cholesky(np_A)

		self.assertTrue(np.allclose(L, np_L, atol=1e-10))
		self.assertTrue(np.allclose(L @ L.T, np_A, atol=1e-10))

	def test_case_4_non_symmetric_matrix_raises(self) -> None:
		A = [
			[4.0, 1.0, 2.0],
			[0.0, 3.0, 1.0],
			[2.0, 1.0, 5.0],
		]
		with self.assertRaises(ValueError):
			cholesky_custom(A)

	def test_case_5_symmetric_not_positive_definite_raises(self) -> None:
		A = [
			[1.0, 2.0],
			[2.0, 1.0],
		]
		with self.assertRaises(ValueError):
			cholesky_custom(A)

		with self.assertRaises(np.linalg.LinAlgError):
			np.linalg.cholesky(np.array(A, dtype=float))

	def test_case_6_non_square_matrix_raises(self) -> None:
		A = [
			[1.0, 2.0, 3.0],
			[4.0, 5.0, 6.0],
		]
		with self.assertRaises(ValueError):
			cholesky_custom(A)


if __name__ == "__main__":
	unittest.main(verbosity=2)