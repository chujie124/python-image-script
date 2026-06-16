import cv2
import numpy as np
import os

def create_blue_curve_lut(intensity):
    """
    生成蓝色通道的映射曲线 (Lookup Table)
    """
    x = np.arange(0, 256, dtype=np.float32)
    y = x + intensity * np.sin(x * np.pi / 255.0)
    lut = np.clip(y, 0, 255).astype(np.uint8)
    return lut

def apply_blue_curve_to_image(image, intensity):
    """
    对单张图像应用蓝色曲线
    """
    b, g, r = cv2.split(image)
    lut = create_blue_curve_lut(intensity)
    b_enhanced = cv2.LUT(b, lut)
    enhanced_image = cv2.merge((b_enhanced, g, r))
    return enhanced_image

# ======== 新增：支持中文路径的读取和保存函数 ========
def cv_imread(file_path):
    """支持中文路径的读取"""
    # 先用 numpy 把文件读成一维数组，再用 imdecode 解码
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return cv_img

def cv_imwrite(file_path, img):
    """支持中文路径的保存"""
    # 获取图片的后缀名（例如 .jpg）
    ext = os.path.splitext(file_path)[1]
    # 先编码，再用 numpy 写入文件
    cv2.imencode(ext, img)[1].tofile(file_path)
# ====================================================

def batch_process_images(input_dir, output_dir, intensity):
    """
    批量处理文件夹中的图片
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 已创建输出文件夹: {output_dir}")

    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    count = 0

    print(f"🚀 开始批量处理，当前设置的蓝色拉升强度为: {intensity}")
    
    for filename in os.listdir(input_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in valid_extensions:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"blue_{filename}")
            
            # 【修改点】使用自己写的支持中文的读取函数
            img = cv_imread(input_path)
            if img is None:
                print(f"⚠️ 无法读取文件: {filename}")
                continue
            
            # 处理图片
            enhanced_img = apply_blue_curve_to_image(img, intensity)
            
            # 【修改点】使用自己写的支持中文的保存函数
            cv_imwrite(output_path, enhanced_img)
            print(f"✅ 成功处理并保存: {output_path}")
            count += 1
            
    print(f"🎉 批量处理完成！共处理了 {count} 张图片。")

if __name__ == "__main__":
    # ================= 配置区域 =================
    
    # 请继续使用你之前的路径即可，现在它已经支持中文了
    INPUT_FOLDER = r"D:\PythonProjects\照片\处理前"  # 请替换为你的实际待处理路径
    OUTPUT_FOLDER = r"D:\PythonProjects\照片\处理后" # 请替换为你的实际输出路径
    
    BLUE_INTENSITY = 40  
    
    # ===========================================
    
    batch_process_images(INPUT_FOLDER, OUTPUT_FOLDER, BLUE_INTENSITY)