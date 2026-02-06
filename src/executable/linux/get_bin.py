import os
import shutil
import sys

SOURCE_DIR = r"/home/f/myproject/Brave/src/out/Release"
TARGET_DIR = r"/home/f/myproject/web3DomainProject/kilo/executable/linux/pgk/kilo/opt/kilo"

REQUIRED_ITEMS = [
    "angledata",
    "locales",
    "MEIPreload",
    "PrivacySandboxAttestationsPreloaded",
    "brave_100_percent.pak",
    "brave_200_percent.pak",
    "brave_resources.pak",
    "chrome_100_percent.pak",
    "chrome_200_percent.pak",
    "chrome_crashpad_handler",
    "chrome_sandbox",
    "headless_command_resources.pak",
    "icudtl.dat",
    "kilo",
    "libEGL.so",
    "libGLESv2.so",
    "libqt5_shim.so",
    "libqt6_shim.so",
    "libvk_swiftshader.so",
    "libVkICD_mock_icd.so",
    "libVkLayer_khronos_validation.so",
    "libvulkan.so.1",
    "resources.pak",
    "v8_context_snapshot.bin",
    "vk_swiftshader_icd.json",
    "xdg-mime",
    "xdg-settings",
]

def fail(msg):
    print(f"[ERROR] {msg}")
    sys.exit(1)

def copy_item(src, dst):
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=True)
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

def main():
    if not os.path.isdir(SOURCE_DIR):
        fail(f"源目录不存在: {SOURCE_DIR}")

    os.makedirs(TARGET_DIR, exist_ok=True)

    print("开始验证并复制文件...\n")

    for item in REQUIRED_ITEMS:
        src_path = os.path.join(SOURCE_DIR, item)
        dst_path = os.path.join(TARGET_DIR, item)

        if not os.path.exists(src_path):
            fail(f"缺少必需项: {item}")

        print(f"复制: {item}")
        copy_item(src_path, dst_path)

    print("\n全部文件验证通过并复制完成。")

if __name__ == "__main__":
    main()
