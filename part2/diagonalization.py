# """
# Matrix diagonalization: A = P D P^{-1}

# Definition:
# - A square matrix A is diagonalizable if there exists an invertible matrix P and a
#   diagonal matrix D such that A = P D P^{-1}.
# - The diagonal entries of D are eigenvalues of A, and columns of P are
#   corresponding eigenvectors.

# Important application:
# - Matrix power can be computed by A^k = P D^k P^{-1}.
# - This process significantly reduces the computational cost of matrix exponentiation
#     from O(n^3 log k) down to O(n^2).

# Why numerical algorithms (NumPy) are used:
# - In general, finding eigenvalues requires solving det(A - lambda I) = 0, a degree-n
#   polynomial.
# - By Abel-Ruffini theorem, no general radical formula exists for degree n >= 5.
# - Numerical methods (e.g., QR-based algorithms behind numpy.linalg.eig) provide
#   stable approximations for practical matrix sizes.
# """

# from __future__ import annotations

# import numpy as np
# from part1.inverse import inverse


# def diagonalize_matrix(A, cond_threshold: float = 1e8):
#     """Diagonalize a square matrix A and return (P, D, P_inv).

#     Args:
#         A: Input square matrix-like object.
#         cond_threshold: Maximum accepted condition number of P.

#     Raises:
#         ValueError: If A is not square or numerically not diagonalizable.
#     """
#     A = np.array(A, dtype=float)

#     if A.ndim != 2 or A.shape[0] != A.shape[1]:
#         raise ValueError("Input matrix A must be square.")

#     eigenvalues, eigenvectors = np.linalg.eig(A)
#     P = eigenvectors
#     D = np.diag(eigenvalues)

#     cond_p = np.linalg.cond(P)
#     if (not np.isfinite(cond_p)) or cond_p > cond_threshold:
#         raise ValueError(
#             f"Matrix is not diagonalizable or numerically unstable (cond(P)={cond_p:.3e})."
#         )

#     P_inv = inverse(P)
#     return P, D, P_inv


# def verify_diagonalization(A, P, D, P_inv, atol: float = 1e-5, rtol: float = 1e-5):
#     """Verify A ~= P D P^{-1}. Return (ok, max_abs_error)."""
#     A = np.array(A, dtype=float)
#     A_hat = P @ D @ P_inv
#     max_abs_error = float(np.max(np.abs(A - A_hat)))
#     ok = bool(np.allclose(A, A_hat, atol=atol, rtol=rtol))
#     return ok, max_abs_error


# def matrix_power_via_diagonalization(A, k: int, cond_threshold: float = 1e8):
#     """Compute A^k using diagonalization when stable."""
#     if k < 0:
#         raise ValueError("k must be a non-negative integer.")

#     P, D, P_inv = diagonalize_matrix(A, cond_threshold=cond_threshold)
#     Dk = np.diag(np.diag(D) ** k)
#     return P @ Dk @ P_inv


# """
# Cheo hoa ma tran: A = P D P^{-1}

# Dinh nghia:
# - Mot ma tran vuong A co the cheo hoa neu ton tai ma tran kha nghich P va 
#   ma tran duong cheo D sao cho A = P D P^{-1}.
# - Cac phan tu tren duong cheo cua D la cac gia tri rieng cua A, va cac cot 
#   cua P la cac vector rieng tuong ung.

# Ung dung quan trong:
# - Luy thua ma tran co the duoc tinh bang A^k = P D^k P^{-1}.
# - Qua trinh nay giup giam chi phi tinh toan cua viec tinh luy thua ma tran 
#   tu O(n^3 log k) xuong con O(n^2).

# Tai sao phai su dung thuat toan so tri (NumPy) de tim gia tri rieng:
# - Nhin chung, viec tim gia tri rieng bang giai tich doi hoi phai giai phuong trinh 
#   dac trung det(A - lambda I) = 0, day la mot da thuc bac n.
# - Theo dinh ly bat kha thi Abel-Ruffini, khong ton tai cong thuc nghiem dai so 
#   tong quat (can thuc) cho da thuc bac n >= 5.
# - Do do, chung ta bat buoc phai dua vao cac phuong phap lap so tri (nhu thuat 
#   toan QR duoc cai dat trong `numpy.linalg.eig`) de xap xi on dinh cac gia 
#   tri rieng va vector rieng.
# """

# from __future__ import annotations

# import numpy as np
# from part1.inverse import inverse


# def diagonalize_matrix(A, cond_threshold: float = 1e8):
#     """Cheo hoa ma tran vuong A va tra ve (P, D, P_inv).

#     Args:
#         A: Ma tran vuong dau vao.
#         cond_threshold: Nguong chap nhan toi da cho so dieu kien cua P.

#     Raises:
#         ValueError: Neu A khong phai ma tran vuong hoac khong the cheo hoa ve mat so tri.
#     """
#     A = np.array(A, dtype=float)

#     if A.ndim != 2 or A.shape[0] != A.shape[1]:
#         raise ValueError("Input matrix A must be square.")

#     eigenvalues, eigenvectors = np.linalg.eig(A)
#     P = eigenvectors
#     D = np.diag(eigenvalues)

#     cond_p = np.linalg.cond(P)
#     if (not np.isfinite(cond_p)) or cond_p > cond_threshold:
#         raise ValueError(
#             f"Matrix is not diagonalizable or numerically unstable (cond(P)={cond_p:.3e})."
#         )

#     # Su dung ham inverse tu cai dat tu Phan 1 theo dung quy dinh
#     P_inv = inverse(P)
#     return P, D, P_inv


# def verify_diagonalization(A, P, D, P_inv, atol: float = 1e-5, rtol: float = 1e-5):
#     """Kiem chung A ~= P D P^{-1}. Tra ve (ok, max_abs_error)."""
#     A = np.array(A, dtype=float)
#     A_hat = P @ D @ P_inv
#     max_abs_error = float(np.max(np.abs(A - A_hat)))
#     ok = bool(np.allclose(A, A_hat, atol=atol, rtol=rtol))
#     return ok, max_abs_error


# def matrix_power_via_diagonalization(A, k: int, cond_threshold: float = 1e8):
#     """Tinh A^k thong qua cheo hoa khi ma tran on dinh."""
#     if k < 0:
#         raise ValueError("k must be a non-negative integer.")

#     P, D, P_inv = diagonalize_matrix(A, cond_threshold=cond_threshold)
#     Dk = np.diag(np.diag(D) ** k)
#     return P @ Dk @ P_inv


# def run_test_suite():
#     """Chay 5 test cases (3 case chuan + 2 case bao loi)."""
#     test_cases = [
#         {
#             "name": "TC1 - Ma tran A khuyen dung (3x3 SPD)",
#             "A": np.array([
#                 [4.0, 12.0, -16.0],
#                 [12.0, 37.0, -43.0],
#                 [-16.0, -43.0, 98.0]
#             ]),
#             "expect_error": False,
#         },
#         {
#             "name": "TC2 - Ma tran duong cheo",
#             "A": np.array([[5.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, 7.0]]),
#             "expect_error": False,
#         },
#         {
#             "name": "TC3 - Ma tran 2x2 thong thuong",
#             "A": np.array([[4.0, 1.0], [2.0, 3.0]]),
#             "expect_error": False,
#         },
#         {
#             "name": "TC4 - Ma tran suy bien (Jordan block - khong the cheo hoa)",
#             "A": np.array([[1.0, 1.0], [0.0, 1.0]]),
#             "expect_error": True,
#         },
#         {
#             "name": "TC5 - Ma tran khong vuong",
#             "A": np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]),
#             "expect_error": True,
#         },
#     ]

#     passed = 0

#     for idx, case in enumerate(test_cases, start=1):
#         print("=" * 72)
#         print(f"{idx}. {case['name']}")
#         print("A =")
#         print(case["A"])

#         try:
#             P, D, P_inv = diagonalize_matrix(case["A"], cond_threshold=1e8)

#             if case["expect_error"]:
#                 print("FAIL: Expected an error, but diagonalization succeeded.")
#                 continue

#             ok, max_err = verify_diagonalization(case["A"], P, D, P_inv)
            
#             # Tinh toan va in truc tiep ma tran phuc hoi de chung minh
#             A_reconstructed = P @ D @ P_inv
            
#             print("\nMa tran P =")
#             print(P)
#             print("\nMa tran D =")
#             print(D)
#             print("\nMa tran P_inv =")
#             print(P_inv)
#             print("\nPhuc hoi ma tran (P @ D @ P_inv) =")
#             print(A_reconstructed)
            
#             print(f"\nallclose(A, P @ D @ P_inv) = {ok}")
#             print(f"max_abs_error = {max_err:.3e}")

#             if ok:
#                 print("PASS")
#                 passed += 1
#             else:
#                 print("FAIL: Reconstruction check did not pass tolerance.")

#         except ValueError as exc:
#             if case["expect_error"]:
#                 print(f"PASS: Caught expected ValueError -> {exc}")
#                 passed += 1
#             else:
#                 print(f"FAIL: Unexpected ValueError -> {exc}")

#     print("=" * 72)
#     print(f"Summary: {passed}/{len(test_cases)} test cases passed.")


# def demo_matrix_power():
#     """Demo nho cho viec tinh A^k = P D^k P^{-1}."""
#     # Su dung dung ma tran 3x3 khuyen dung theo yeu cau cua do an
#     A = np.array([
#         [4.0, 12.0, -16.0],
#         [12.0, 37.0, -43.0],
#         [-16.0, -43.0, 98.0]
#     ])
#     k = 3

#     A_k_diag = matrix_power_via_diagonalization(A, k)
#     A_k_np = np.linalg.matrix_power(A, k)

#     print("=" * 72)
#     print("Demo Matrix Power")
#     print(f"k = {k}")
#     print("\nA^k (thong qua cheo hoa) =")
#     print(A_k_diag)
#     print("\nA^k (thong qua numpy.matrix_power de kiem chung) =")
#     print(A_k_np)
#     print("\nKiem chung allclose =", np.allclose(A_k_diag, A_k_np, atol=1e-5, rtol=1e-5))


# if __name__ == "__main__":
#     run_test_suite()
#     print()
#     demo_matrix_power()


"""
Cheo hoa ma tran: A = P D P^{-1}

Dinh nghia:
- Mot ma tran vuong A co the cheo hoa neu ton tai ma tran kha nghich P va 
  ma tran duong cheo D sao cho A = P D P^{-1}.
- Cac phan tu tren duong cheo cua D la cac gia tri rieng cua A, va cac cot 
  cua P la cac vector rieng tuong ung.

Ung dung quan trong:
- Luy thua ma tran co the duoc tinh bang A^k = P D^k P^{-1}.
- Qua trinh nay giup giam chi phi tinh toan cua viec tinh luy thua ma tran 
  tu O(n^3 log k) xuong con O(n^2).

Tai sao phai su dung thuat toan so tri (NumPy) de tim gia tri rieng:
- Nhin chung, viec tim gia tri rieng bang giai tich doi hoi phai giai phuong trinh 
  dac trung det(A - lambda I) = 0, day la mot da thuc bac n.
- Theo dinh ly bat kha thi Abel-Ruffini, khong ton tai cong thuc nghiem dai so 
  tong quat (can thuc) cho da thuc bac n >= 5.
- Do do, chung ta bat buoc phai dua vao cac phuong phap lap so tri (nhu thuat 
  toan QR duoc cai dat trong `numpy.linalg.eig`) de xap xi on dinh cac gia 
  tri rieng va vector rieng.
"""

from __future__ import annotations

import numpy as np
import sys
import os
import unittest

# --- FIX LOI IMPORT ---
# Lay duong dan cua thu muc cha (task2) va them vao he thong
# giup Python tim thay module 'part1' du ban dang chay file o bat ky thu muc nao
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from part1.inverse import inverse


def diagonalize_matrix(A, cond_threshold: float = 1e8):
    """Cheo hoa ma tran vuong A va tra ve (P, D, P_inv).

    Args:
        A: Ma tran vuong dau vao.
        cond_threshold: Nguong chap nhan toi da cho so dieu kien cua P.

    Raises:
        ValueError: Neu A khong phai ma tran vuong hoac khong the cheo hoa ve mat so tri.
    """
    A = np.array(A, dtype=float)

    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("Input matrix A must be square.")

    eigenvalues, eigenvectors = np.linalg.eig(A)
    P = eigenvectors
    D = np.diag(eigenvalues)

    cond_p = np.linalg.cond(P)
    if (not np.isfinite(cond_p)) or cond_p > cond_threshold:
        raise ValueError(
            f"Matrix is not diagonalizable or numerically unstable (cond(P)={cond_p:.3e})."
        )

    # Su dung ham inverse tu cai dat tu Phan 1 theo dung quy dinh
    P_inv = inverse(P)
    return P, D, P_inv


def verify_diagonalization(A, P, D, P_inv, atol: float = 1e-5, rtol: float = 1e-5):
    """Kiem chung A ~= P D P^{-1}. Tra ve (ok, max_abs_error)."""
    A = np.array(A, dtype=float)
    A_hat = P @ D @ P_inv
    max_abs_error = float(np.max(np.abs(A - A_hat)))
    ok = bool(np.allclose(A, A_hat, atol=atol, rtol=rtol))
    return ok, max_abs_error


def matrix_power_via_diagonalization(A, k: int, cond_threshold: float = 1e8):
    """Tinh A^k thong qua cheo hoa khi ma tran on dinh."""
    if k < 0:
        raise ValueError("k must be a non-negative integer.")

    P, D, P_inv = diagonalize_matrix(A, cond_threshold=cond_threshold)
    Dk = np.diag(np.diag(D) ** k)
    return P @ Dk @ P_inv


# =====================================================================
# PHAN UNIT TEST CHO HAM DIAGONALIZE_MATRIX & VERIFY_DIAGONALIZATION
# =====================================================================
class TestDiagonalization(unittest.TestCase):

    def print_report(self, tc_name, A, P=None, D=None, P_inv=None, A_hat=None, max_err=None, expected_err=None):
        """Ham ho tro in bao cao test case dep mat tren console."""
        print("\n" + "="*75)
        print(f"[TEST CASE DIAGONALIZATION] {tc_name}")
        print("="*75)
        
        print("[1. DAU VAO (INPUT)]")
        print("Ma tran A:")
        print(A)
        
        if expected_err:
            print("\n[2. KET QUA MONG DOI (EXPECTED OUTPUT)]")
            print(f"Ma tran loi/suy bien. He thong phai bat duoc loi: {expected_err}")
            return

        print("\n[2. KET QUA TINH TOAN (OUTPUT)]")
        print("-> Ma tran D (Cac gia tri rieng nam tren duong cheo):")
        print(np.round(D, 4))
        print("\n-> Ma tran P (Cac vector rieng tuong ung tao thanh cot):")
        print(np.round(P, 4))
        print("\n-> Ma tran P_inv (Nghich dao cua P, tinh bang Gauss-Jordan):")
        print(np.round(P_inv, 4))
        
        print("\n[3. KIEM CHUNG (VERIFICATION)]")
        print("-> Phuc hoi ma tran A_hat = P @ D @ P_inv:")
        print(np.round(A_hat, 4))
        print(f"\n-> Danh gia sai so (Max Absolute Error): {max_err:.3e}")
        if max_err < 1e-5:
            print("-> KET LUAN: Thanh cong! Ma tran phuc hoi khop voi ma tran A ban dau.")
        else:
            print("-> KET LUAN: That bai! Sai so qua lon.")

    def test_tc1_ma_tran_khuyen_dung_spd(self):
        name = "TC1 - Ma tran A khuyen dung (3x3 Symmetric Positive Definite)"
        A = np.array([
            [4.0, 12.0, -16.0],
            [12.0, 37.0, -43.0],
            [-16.0, -43.0, 98.0]
        ])
        P, D, P_inv = diagonalize_matrix(A)
        ok, max_err = verify_diagonalization(A, P, D, P_inv)
        A_reconstructed = P @ D @ P_inv
        
        self.print_report(name, A, P, D, P_inv, A_reconstructed, max_err)
        self.assertTrue(ok, f"{name} failed! Sai so: {max_err}")

    def test_tc2_ma_tran_duong_cheo(self):
        name = "TC2 - Ma tran duong cheo (Diagonal Matrix)"
        A = np.array([[5.0, 0.0, 0.0], [0.0, -2.0, 0.0], [0.0, 0.0, 7.0]])
        P, D, P_inv = diagonalize_matrix(A)
        ok, max_err = verify_diagonalization(A, P, D, P_inv)
        A_reconstructed = P @ D @ P_inv
        
        self.print_report(name, A, P, D, P_inv, A_reconstructed, max_err)
        self.assertTrue(ok, f"{name} failed! Sai so: {max_err}")

    def test_tc3_ma_tran_thong_thuong_2x2(self):
        name = "TC3 - Ma tran 2x2 thong thuong (Distinct Eigenvalues)"
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        P, D, P_inv = diagonalize_matrix(A)
        ok, max_err = verify_diagonalization(A, P, D, P_inv)
        A_reconstructed = P @ D @ P_inv
        
        self.print_report(name, A, P, D, P_inv, A_reconstructed, max_err)
        self.assertTrue(ok, f"{name} failed! Sai so: {max_err}")

    def test_tc4_ma_tran_suy_bien(self):
        name = "TC4 - Ma tran suy bien (Jordan Block - Khong the cheo hoa)"
        A = np.array([[1.0, 1.0], [0.0, 1.0]])
        
        self.print_report(name, A, expected_err="ValueError (Numerically unstable)")
        
        with self.assertRaises(ValueError) as context:
            diagonalize_matrix(A)
        print(f"-> THUC TE: He thong da bat loi thanh cong: {context.exception}")

    def test_tc5_ma_tran_khong_vuong(self):
        name = "TC5 - Ma tran khong vuong (Non-square matrix)"
        A = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        
        self.print_report(name, A, expected_err="ValueError (Input must be square)")
        
        with self.assertRaises(ValueError) as context:
            diagonalize_matrix(A)
        print(f"-> THUC TE: He thong da bat loi thanh cong: {context.exception}")


# =====================================================================
# PHAN UNIT TEST CHO HAM MATRIX_POWER_VIA_DIAGONALIZATION
# =====================================================================
class TestMatrixPower(unittest.TestCase):
    
    def test_tc1_luy_thua_ma_tran_spd(self):
        print("\n" + "="*75)
        print("[TEST CASE POWER 1] Luy thua ma tran SPD (k=3)")
        A = np.array([
            [4.0, 12.0, -16.0],
            [12.0, 37.0, -43.0],
            [-16.0, -43.0, 98.0]
        ])
        k = 3
        A_k = matrix_power_via_diagonalization(A, k)
        A_k_numpy = np.linalg.matrix_power(A, k)
        
        ok = np.allclose(A_k, A_k_numpy, atol=1e-5, rtol=1e-5)
        print("-> Ket qua A^3 (thong qua cheo hoa):\n", np.round(A_k, 4))
        print("-> Kiem chung voi numpy.matrix_power: ", ok)
        self.assertTrue(ok, "Tinh luy thua ma tran SPD sai.")

    def test_tc2_luy_thua_ma_tran_duong_cheo(self):
        print("\n" + "="*75)
        print("[TEST CASE POWER 2] Luy thua ma tran duong cheo (k=5)")
        A = np.array([[2.0, 0.0], [0.0, 3.0]])
        k = 5
        A_k = matrix_power_via_diagonalization(A, k)
        A_k_numpy = np.linalg.matrix_power(A, k)
        
        ok = np.allclose(A_k, A_k_numpy, atol=1e-5, rtol=1e-5)
        print("-> Ket qua A^5 (thong qua cheo hoa):\n", np.round(A_k, 4))
        print("-> Kiem chung voi numpy.matrix_power: ", ok)
        self.assertTrue(ok, "Tinh luy thua ma tran duong cheo sai.")

    def test_tc3_luy_thua_bac_khong(self):
        print("\n" + "="*75)
        print("[TEST CASE POWER 3] Edge Case: Luy thua bac k=0 (Phai ra ma tran don vi I)")
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        k = 0
        A_k = matrix_power_via_diagonalization(A, k)
        I = np.eye(2)
        
        ok = np.allclose(A_k, I, atol=1e-5, rtol=1e-5)
        print("-> Ket qua khi k=0:\n", np.round(A_k, 4))
        print("-> Kiem chung voi ma tran don vi I: ", ok)
        self.assertTrue(ok, "Luy thua bac 0 phai ra ma tran don vi.")

    def test_tc4_loi_luy_thua_am(self):
        print("\n" + "="*75)
        print("[TEST CASE POWER 4] Edge Case: Bat loi luy thua am (k < 0)")
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        k = -2
        
        with self.assertRaises(ValueError) as context:
            matrix_power_via_diagonalization(A, k)
        print(f"-> Bat loi thanh cong luy thua am: {context.exception}")

    def test_tc5_loi_ma_tran_khong_cheo_hoa_duoc(self):
        print("\n" + "="*75)
        print("[TEST CASE POWER 5] Edge Case: Tinh luy thua tren ma tran suy bien")
        A = np.array([[1.0, 1.0], [0.0, 1.0]]) # Jordan block
        k = 2
        
        with self.assertRaises(ValueError) as context:
            matrix_power_via_diagonalization(A, k)
        print(f"-> Bat loi thanh cong ma tran khong the cheo hoa: {context.exception}")


def demo_matrix_power():
    """Demo nho cho viec tinh A^k = P D^k P^{-1}."""
    A = np.array([
        [4.0, 12.0, -16.0],
        [12.0, 37.0, -43.0],
        [-16.0, -43.0, 98.0]
    ])
    k = 3

    A_k_diag = matrix_power_via_diagonalization(A, k)
    A_k_np = np.linalg.matrix_power(A, k)

    print("\n" + "=" * 75)
    print("DEMO MATRIX POWER (Nghiem thu chuc nang ung dung)")
    print("=" * 75)
    print(f"Tinh ma tran A^k voi k = {k}")
    print("\nA^k (thong qua cheo hoa) =")
    print(np.round(A_k_diag, 4))
    print("\nA^k (thong qua numpy.matrix_power de kiem chung) =")
    print(np.round(A_k_np, 4))
    print("\n-> Kiem chung muc do khop (allclose) =", np.allclose(A_k_diag, A_k_np, atol=1e-5, rtol=1e-5))
    print("=" * 75)


if __name__ == "__main__":
    print("BAT DAU CHAY UNIT TEST...")
    # exit=False de sau khi chay test xong, chuong trinh tiep tuc xuong chay phan demo
    unittest.main(argv=[''], exit=False)
    
    # Chay demo luy thua ma tran cuoi cung de nghiem thu truc quan
    demo_matrix_power()