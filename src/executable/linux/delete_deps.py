import os
import shutil

# -----------------------------
# 配置
# -----------------------------
TARGET_DIR = r"/home/f/myproject/Brave/src/out/test"  # 要清理的目录
TEMP_BACKUP = os.path.join(TARGET_DIR, "_deps_backup")  # 临时隔离目录
RUN_BACKUP = True  # True 表示移动到备份目录，False 表示直接删除

os.makedirs(TEMP_BACKUP, exist_ok=True)

# -----------------------------
# 遍历目录
# -----------------------------
for root, dirs, files in os.walk(TARGET_DIR, topdown=True):
    # 排除隔离目录本身
    dirs[:] = [d for d in dirs if d != os.path.basename(TEMP_BACKUP)]

    for f in files:
        if f.endswith(".runtime_deps"):
            src_file = os.path.join(root, f)
            rel_file = os.path.relpath(src_file, TARGET_DIR)

            if RUN_BACKUP:
                dst_file = os.path.join(TEMP_BACKUP, rel_file)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.move(src_file, dst_file)
                print(f"[隔离] {rel_file}")
            else:
                os.remove(src_file)
                print(f"[删除] {rel_file}")

print("清理完成！")
if RUN_BACKUP:
    print(f"所有 .runtime_deps 文件已移动到: {TEMP_BACKUP}")
else:
    print("所有 .runtime_deps 文件已被删除")
