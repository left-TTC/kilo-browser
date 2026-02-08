import os
import shutil

# -----------------------------
# 配置
# -----------------------------
TARGET_DIR = r"/home/f/myproject/Brave/src/out/test"

# 保留文件和文件夹
KEEP_FILES = ["kilo.exe", "brave.exe", "icudtl.dat"]
KEEP_FOLDERS = ["resources", "locales", "WidevineCdm"]

# 可删除关键字 / 文件名
DELETE_KEYWORDS = [
    "build.ninja",
    ".runtime_deps",
    "generator.exe",
    "plugin.exe",
    "bench",
    "fuzzer",
    "exercise",
    "ghost_rules",
    "flatc.exe",
    "mksnapshot.exe",
    "protoc",
    "toolchain.ninja",
    "torque.exe",
    "v8_context_snapshot_generator.exe",
    "dbgcore.dll",
    "dbghelp.dll",
    "gpu_benchmark",
    "leveldb_db_bench",
    "devtools_protocol_encoding_json_fuzzer",
    "exercise_2_solution",
    "args.gn",
    "args_generated.gni",
    "gn_args_page_graph.json",
    "gn_logs.txt",
    "environment.x64",
    "environment.x86",
    "first run",
    "version",
]

# -----------------------------
# 遍历删除
# -----------------------------
deletable = []

for root, dirs, files in os.walk(TARGET_DIR, topdown=True):
    # 排除保留文件夹
    dirs[:] = [d for d in dirs if d not in KEEP_FOLDERS]

    # 处理目录
    for d in dirs:
        if any(kw.lower() in d.lower() for kw in DELETE_KEYWORDS):
            deletable.append(("dir", os.path.join(root, d)))

    # 处理文件
    for f in files:
        if f in KEEP_FILES:
            continue
        if any(kw.lower() in f.lower() for kw in DELETE_KEYWORDS):
            deletable.append(("file", os.path.join(root, f)))

# -----------------------------
# 删除操作
# -----------------------------
print("==== 将删除以下文件/文件夹 ====")
for typ, path in deletable:
    print(f"{typ}: {path}")

confirm = input("\n是否直接删除这些文件/文件夹？(y/n) ")
if confirm.lower() == "y":
    for typ, path in deletable:
        if not os.path.exists(path):
            print(f"[跳过] 不存在: {path}")
            continue
        try:
            if typ == "file":
                os.remove(path)
            else:
                shutil.rmtree(path)
            print(f"[已删除] {path}")
        except Exception as e:
            print(f"[删除失败] {path} -> {e}")

print("\n删除完成！")
