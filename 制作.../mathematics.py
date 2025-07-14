import math
import numpy as np
from fractions import Fraction
import sympy as sp
from sympy import symbols, solve, expand, factor, simplify, diff, integrate, limit, oo
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
import warnings
warnings.filterwarnings('ignore')

class MathSolver:
    def __init__(self):
        self.x, self.y, self.z = symbols('x y z')
        self.a, self.b, self.c = symbols('a b c')
        
    # ========== 基本計算 ==========
    def basic_arithmetic(self, expression):
        """基本的な四則演算"""
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except:
            return "計算エラー"
    
    def fraction_operations(self, frac1, frac2, operation):
        """分数の計算"""
        try:
            f1 = Fraction(frac1)
            f2 = Fraction(frac2)
            
            if operation == '+':
                result = f1 + f2
            elif operation == '-':
                result = f1 - f2
            elif operation == '*':
                result = f1 * f2
            elif operation == '/':
                result = f1 / f2
            else:
                return "演算子エラー（+, -, *, /のみ）"
            
            return f"{f1} {operation} {f2} = {result}"
        except:
            return "分数計算エラー"
    
    # ========== 代数 ==========
    def solve_linear_equation(self, equation):
        """一次方程式を解く"""
        x = symbols('x')
        try:
            eq = sp.sympify(equation)
            solution = solve(eq, x)
            return f"方程式 {equation} = 0 の解: x = {solution}"
        except:
            return "方程式の解析エラー"
    
    def solve_quadratic_equation(self, a, b, c):
        """二次方程式 ax² + bx + c = 0 を解く"""
        try:
            x = symbols('x')
            eq = a*x**2 + b*x + c
            solutions = solve(eq, x)
            
            discriminant = b**2 - 4*a*c
            result = f"二次方程式 {a}x² + {b}x + {c} = 0\n"
            result += f"判別式: D = {discriminant}\n"
            
            if discriminant > 0:
                result += f"異なる2つの実数解: x = {solutions}"
            elif discriminant == 0:
                result += f"重解: x = {solutions[0]}"
            else:
                result += f"複素数解: x = {solutions}"
            
            return result
        except:
            return "二次方程式の解析エラー"
    
    def solve_system_equations(self, eq1, eq2):
        """連立方程式を解く"""
        x, y = symbols('x y')
        try:
            equation1 = sp.sympify(eq1)
            equation2 = sp.sympify(eq2)
            solution = solve([equation1, equation2], [x, y])
            return f"連立方程式の解: {solution}"
        except:
            return "連立方程式の解析エラー"
    
    def expand_expression(self, expression):
        """式の展開"""
        try:
            expr = sp.sympify(expression)
            expanded = expand(expr)
            return f"展開: {expression} = {expanded}"
        except:
            return "展開エラー"
    
    def factor_expression(self, expression):
        """式の因数分解"""
        try:
            expr = sp.sympify(expression)
            factored = factor(expr)
            return f"因数分解: {expression} = {factored}"
        except:
            return "因数分解エラー"
    
    # ========== 幾何学 ==========
    def triangle_area(self, base, height):
        """三角形の面積"""
        try:
            area = 0.5 * base * height
            return f"三角形の面積: {area}"
        except:
            return "三角形面積計算エラー"
    
    def triangle_area_heron(self, a, b, c):
        """ヘロンの公式で三角形の面積"""
        try:
            s = (a + b + c) / 2
            area = math.sqrt(s * (s - a) * (s - b) * (s - c))
            return f"三角形の面積（ヘロンの公式）: {area:.4f}"
        except:
            return "ヘロンの公式計算エラー（三角形の条件を満たしていない可能性）"
    
    def circle_area_circumference(self, radius):
        """円の面積と円周"""
        try:
            area = math.pi * radius**2
            circumference = 2 * math.pi * radius
            return f"半径{radius}の円: 面積={area:.4f}, 円周={circumference:.4f}"
        except:
            return "円の計算エラー"
    
    def distance_two_points(self, x1, y1, x2, y2):
        """2点間の距離"""
        try:
            distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            return f"点({x1}, {y1})と点({x2}, {y2})の距離: {distance:.4f}"
        except:
            return "距離計算エラー"
    
    # ========== 統計・確率 ==========
    def statistics_basic(self, data):
        """基本統計量"""
        try:
            mean = sum(data) / len(data)
            sorted_data = sorted(data)
            n = len(data)
            median = sorted_data[n//2] if n % 2 == 1 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2
            
            mode_dict = {}
            for val in data:
                mode_dict[val] = mode_dict.get(val, 0) + 1
            mode = max(mode_dict, key=mode_dict.get)
            
            variance = sum((x - mean)**2 for x in data) / len(data)
            std_dev = math.sqrt(variance)
            
            return f"平均値: {mean:.4f}\n中央値: {median}\n最頻値: {mode}\n分散: {variance:.4f}\n標準偏差: {std_dev:.4f}"
        except:
            return "統計計算エラー"
    
    def combinations(self, n, r):
        """組み合わせ nCr"""
        try:
            if r > n or r < 0:
                return "組み合わせの条件エラー（0 ≤ r ≤ n）"
            result = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
            return f"{n}C{r} = {result}"
        except:
            return "組み合わせ計算エラー"
    
    def permutations(self, n, r):
        """順列 nPr"""
        try:
            if r > n or r < 0:
                return "順列の条件エラー（0 ≤ r ≤ n）"
            result = math.factorial(n) // math.factorial(n - r)
            return f"{n}P{r} = {result}"
        except:
            return "順列計算エラー"
    
    # ========== 三角関数 ==========
    def trigonometric_values(self, angle_degrees):
        """三角関数の値"""
        try:
            angle_rad = math.radians(angle_degrees)
            sin_val = math.sin(angle_rad)
            cos_val = math.cos(angle_rad)
            tan_val = math.tan(angle_rad) if abs(math.cos(angle_rad)) > 1e-10 else "未定義"
            
            return f"{angle_degrees}°の三角関数値:\nsin = {sin_val:.4f}\ncos = {cos_val:.4f}\ntan = {tan_val if tan_val == '未定義' else f'{tan_val:.4f}'}"
        except:
            return "三角関数計算エラー"

def print_menu():
    """メニューを表示"""
    print("\n" + "="*50)
    print("         数学計算機メニュー")
    print("="*50)
    print("1. 基本計算")
    print("2. 分数計算")
    print("3. 一次方程式")
    print("4. 二次方程式")
    print("5. 連立方程式")
    print("6. 式の展開")
    print("7. 因数分解")
    print("8. 三角形の面積")
    print("9. 三角形の面積（ヘロンの公式）")
    print("10. 円の面積・円周")
    print("11. 2点間の距離")
    print("12. 統計量計算")
    print("13. 組み合わせ")
    print("14. 順列")
    print("15. 三角関数")
    print("0. 終了")
    print("="*50)

def get_input(prompt, data_type=str):
    """入力を取得して適切な型に変換"""
    while True:
        try:
            if data_type == list:
                user_input = input(prompt)
                return [float(x.strip()) for x in user_input.split(',')]
            elif data_type == float:
                return float(input(prompt))
            elif data_type == int:
                return int(input(prompt))
            else:
                return input(prompt)
        except ValueError:
            print("入力形式が正しくありません。もう一度入力してください。")

def main():
    solver = MathSolver()
    
    print("数学計算機へようこそ！")
    print("様々な数学問題を解くことができます。")
    
    while True:
        print_menu()
        choice = input("選択してください（0-15）: ").strip()
        
        if choice == '0':
            print("計算機を終了します。お疲れ様でした！")
            break
        
        elif choice == '1':
            expression = input("計算式を入力してください（例：2+3*4）: ")
            print(solver.basic_arithmetic(expression))
        
        elif choice == '2':
            frac1 = input("1つ目の分数を入力してください（例：1/2）: ")
            frac2 = input("2つ目の分数を入力してください（例：2/3）: ")
            operation = input("演算子を入力してください（+, -, *, /）: ")
            print(solver.fraction_operations(frac1, frac2, operation))
        
        elif choice == '3':
            equation = input("一次方程式を入力してください（例：2*x+3）: ")
            print(solver.solve_linear_equation(equation))
        
        elif choice == '4':
            print("二次方程式 ax² + bx + c = 0 の係数を入力してください")
            a = get_input("a = ", float)
            b = get_input("b = ", float)
            c = get_input("c = ", float)
            print(solver.solve_quadratic_equation(a, b, c))
        
        elif choice == '5':
            print("連立方程式を入力してください")
            eq1 = input("1つ目の式（例：2*x+3*y-7）: ")
            eq2 = input("2つ目の式（例：x-2*y+1）: ")
            print(solver.solve_system_equations(eq1, eq2))
        
        elif choice == '6':
            expression = input("展開する式を入力してください（例：(x+2)*(x-3)）: ")
            print(solver.expand_expression(expression))
        
        elif choice == '7':
            expression = input("因数分解する式を入力してください（例：x**2-4）: ")
            print(solver.factor_expression(expression))
        
        elif choice == '8':
            base = get_input("底辺: ", float)
            height = get_input("高さ: ", float)
            print(solver.triangle_area(base, height))
        
        elif choice == '9':
            print("三角形の3辺の長さを入力してください")
            a = get_input("辺a: ", float)
            b = get_input("辺b: ", float)
            c = get_input("辺c: ", float)
            print(solver.triangle_area_heron(a, b, c))
        
        elif choice == '10':
            radius = get_input("半径: ", float)
            print(solver.circle_area_circumference(radius))
        
        elif choice == '11':
            print("2点の座標を入力してください")
            x1 = get_input("1点目のx座標: ", float)
            y1 = get_input("1点目のy座標: ", float)
            x2 = get_input("2点目のx座標: ", float)
            y2 = get_input("2点目のy座標: ", float)
            print(solver.distance_two_points(x1, y1, x2, y2))
        
        elif choice == '12':
            print("データを入力してください（カンマ区切り）")
            print("例: 85,92,78,96,87")
            data = get_input("データ: ", list)
            print(solver.statistics_basic(data))
        
        elif choice == '13':
            n = get_input("n: ", int)
            r = get_input("r: ", int)
            print(solver.combinations(n, r))
        
        elif choice == '14':
            n = get_input("n: ", int)
            r = get_input("r: ", int)
            print(solver.permutations(n, r))
        
        elif choice == '15':
            angle = get_input("角度（度）: ", float)
            print(solver.trigonometric_values(angle))
        
        else:
            print("無効な選択です。0-15の数字を入力してください。")
        
        # 次の操作への案内
        input("\nEnterキーを押して続行...")

if __name__ == "__main__":
    main()