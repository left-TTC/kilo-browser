import os
import shutil

# -----------------------------
# 配置
# -----------------------------
SOURCE_DIR = "/home/f/myproject/Brave/src/out/test1"  # 来源目录
PKG_DIR = "/home/f/myproject/web3DomainProject/kilo/executable/linux/pgk/kilo-deb"         # 打包目录

BIN_FILES = ["kilo"]  # 可执行文件
LIB_FILES = [
    "libEGL.so", "libGLESv2.so", "libqt5_shim.so", "libqt6_shim.so",
    "libVkICD_mock_icd.so", "libVkLayer_khronos_validation.so",
    "libvk_swiftshader.so", "libvulkan.so.1", "chrome_sandbox"
]
SHARE_FILES = [
    "angledata",
    "brave_100_percent.pak", "brave_100_percent.pak.info",
    "brave_200_percent.pak", "brave_200_percent.pak.info",
    "brave_resources.pak", "brave_resources.pak.info",
    "chrome_100_percent.pak", "chrome_100_percent.pak.info",
    "chrome_200_percent.pak", "chrome_200_percent.pak.info",
    "chrome_crashpad_handler", "chrome-wrapper",
    "headless_command_resources.pak", "headless_command_resources.pak.info",
    "resources.pak", "resources.pak.info",
    "snapshot_blob.bin", "v8_context_snapshot.bin",
    "icudtl.dat", "vk_swiftshader_icd.json",
    "locales"  # 文件夹
]
TOOLS_FILES = [
    "make_top_domain_list_variables", "mksnapshot", "protoc", "protoc-gen-js",
    "proto_extras_plugin", "protozero_plugin", "extensions", "root_store_tool",
    "xdg-mime", "xdg-settings"
]

# -----------------------------
# 创建目标目录
# -----------------------------
BIN_DIR = os.path.join(PKG_DIR, "usr/bin")
LIB_DIR = os.path.join(PKG_DIR, "usr/lib/kilo")
SHARE_DIR = os.path.join(PKG_DIR, "usr/share/kilo")
TOOLS_DIR = os.path.join(PKG_DIR, "usr/lib/kilo/tools")

os.makedirs(BIN_DIR, exist_ok=True)
os.makedirs(LIB_DIR, exist_ok=True)
os.makedirs(SHARE_DIR, exist_ok=True)
os.makedirs(TOOLS_DIR, exist_ok=True)

# -----------------------------
# 拷贝文件函数
# -----------------------------
def copy_file(name, src_dir, dst_dir):
    src_path = os.path.join(src_dir, name)
    dst_path = os.path.join(dst_dir, name)
    if os.path.exists(src_path):
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
            print(f"[目录复制] {name} -> {dst_dir}")
        else:
            shutil.copy2(src_path, dst_path)
            print(f"[文件复制] {name} -> {dst_dir}")
    else:
        print(f"[警告] 文件/目录不存在: {src_path}")

# -----------------------------
# 开始复制
# -----------------------------
for f in BIN_FILES:
    copy_file(f, SOURCE_DIR, BIN_DIR)

for f in LIB_FILES:
    copy_file(f, SOURCE_DIR, LIB_DIR)

for f in SHARE_FILES:
    copy_file(f, SOURCE_DIR, SHARE_DIR)

for f in TOOLS_FILES:
    copy_file(f, SOURCE_DIR, TOOLS_DIR)

print("\n分类完成！")
print(f"打包目录: {PKG_DIR}")
