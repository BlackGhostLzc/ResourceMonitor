from tabulate import tabulate

# 数据
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "New York"],
    ["Bob", 24, "Los Angeles"],
    ["Charlie", 29, "Chicago"]
]

# 打印表格
print(tabulate(data, headers="firstrow", tablefmt="grid"))

