import os
import shutil
import zipfile

def copy_and_zip_apk(src_dir, apk_name, dest_dir, new_name=None):
    """
    复制 APK 并生成 ZIP 版本

    :param src_dir: 原 APK 文件所在目录
    :param apk_name: 原 APK 文件名（带 .apk）
    :param dest_dir: 目标目录
    :param new_name: 新文件名（不带扩展名），如果为 None 则使用原名
    """
    # 检查源文件
    src_apk_path = os.path.join(src_dir, apk_name)
    if not os.path.isfile(src_apk_path):
        raise FileNotFoundError(f"APK 文件不存在: {src_apk_path}")

    # 创建目标目录
    os.makedirs(dest_dir, exist_ok=True)

    # 设置新 APK 名称
    base_name = new_name if new_name else os.path.splitext(apk_name)[0]
    apk_dest_path = os.path.join(dest_dir, f"{base_name}.apk")
    zip_dest_path = os.path.join(dest_dir, f"{base_name}.zip")

    # 复制 APK
    shutil.copy2(src_apk_path, apk_dest_path)
    print(f"已复制 APK: {apk_dest_path}")

    # 压缩为 ZIP
    with zipfile.ZipFile(zip_dest_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 将 APK 文件添加到 ZIP，存储为原文件名
        zipf.write(apk_dest_path, arcname=os.path.basename(apk_dest_path))
    print(f"已生成 ZIP: {zip_dest_path}")


if __name__ == "__main__":
    source_folder = "/home/f/myproject/Brave/src/out/android_Component_arm/apks"
    apk_filename = "ChromePublic.apk"
    output_folder = "./apks"
    new_file_base_name = "kilo"

    copy_and_zip_apk(source_folder, apk_filename, output_folder, new_file_base_name)
