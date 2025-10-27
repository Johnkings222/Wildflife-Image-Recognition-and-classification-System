# Windows安装指南

本指南将帮助您在Windows系统上安装和运行野生动物图像识别系统。

---

## 系统要求

### 最低要求
- **操作系统**: Windows 10 或 Windows 11
- **CPU**: 双核处理器 2.0GHz
- **内存**: 4GB RAM
- **存储**: 2GB可用磁盘空间
- **Python**: Python 3.8 - 3.11

### 推荐配置
- **操作系统**: Windows 11
- **CPU**: 四核处理器 3.0GHz+
- **内存**: 8GB+ RAM
- **存储**: 5GB+ SSD空间
- **GPU**: NVIDIA显卡（可选，用于加速）

---

## 步骤1: 安装Python

### 1.1 下载Python

1. 访问Python官方网站: https://www.python.org/downloads/
2. 下载Python 3.10或3.11（推荐）
3. 下载Windows安装程序（64位）

### 1.2 安装Python

1. 运行下载的安装程序
2. **重要**: 勾选 "Add Python to PATH"
3. 选择 "Install Now" 或 "Customize installation"
4. 等待安装完成

### 1.3 验证安装

打开命令提示符（CMD）并输入：

```cmd
python --version
```

应显示类似：`Python 3.10.x`

---

## 步骤2: 下载项目文件

### 方法1: 直接下载ZIP

1. 从项目仓库下载ZIP文件
2. 解压到合适的位置，例如：`C:\Users\YourName\Wildlife Recognition`

### 方法2: 使用Git（如已安装）

```cmd
git clone <repository-url>
cd "Wildlife Image Recognition and Classification System"
```

---

## 步骤3: 安装依赖

### 3.1 打开命令提示符

1. 按 `Win + R` 打开运行对话框
2. 输入 `cmd` 并按回车

### 3.2 导航到项目目录

```cmd
cd "C:\Users\YourName\Wildlife Image Recognition and Classification System"
```

### 3.3 创建虚拟环境（推荐）

```cmd
python -m venv venv
```

### 3.4 激活虚拟环境

```cmd
venv\Scripts\activate
```

激活后，命令提示符前面会显示 `(venv)`

### 3.5 安装依赖包

```cmd
pip install -r requirements.txt
```

**可能需要几分钟时间**，请耐心等待。

### 3.6 使用国内镜像加速（可选）

如果下载速度很慢，可以使用清华镜像源：

```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 步骤4: 运行程序

### 4.1 启动应用

在项目目录下（确保虚拟环境已激活），运行：

```cmd
python wildlife_recognition_app.py
```

### 4.2 首次运行

首次运行时，程序会自动下载预训练模型（约45MB）：

```
正在下载: resnet18-f37072fd.pth
大小: 44.7MB
保存位置: C:\Users\YourName\.cache\torch\hub\checkpoints\
```

**下载完成后，应用程序窗口将自动打开。**

---

## 步骤5: 使用程序

### 5.1 上传图像

1. 点击 "📁 上传图像" 按钮
2. 选择一张野生动物图片（支持JPG、PNG、BMP等格式）
3. 程序会自动识别并显示结果

### 5.2 查看结果

- **左侧**: 显示上传的图像
- **右侧**: 显示前5个预测结果及置信度
- **底部**: 显示当前状态

### 5.3 清除数据

点击 "🗑 清除" 按钮重置界面，可以上传新的图像。

---

## 常见问题解决

### 问题1: "python不是内部或外部命令"

**原因**: Python未添加到系统PATH

**解决方案**:
1. 重新安装Python，勾选 "Add Python to PATH"
2. 或手动添加Python到环境变量

### 问题2: "pip install失败"

**原因**: 网络问题或权限问题

**解决方案**:

方法1 - 使用国内镜像：
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

方法2 - 以管理员身份运行CMD：
1. 搜索 "命令提示符"
2. 右键 → "以管理员身份运行"
3. 重新执行安装命令

### 问题3: "ModuleNotFoundError: No module named 'tkinter'"

**原因**: Python安装时未包含Tkinter

**解决方案**:
1. 重新安装Python
2. 在自定义安装中勾选 "tcl/tk and IDLE"

### 问题4: 中文显示为方框

**原因**: 系统缺少中文字体

**解决方案**:
程序使用 "Microsoft YaHei" 字体，Windows 10/11默认包含。如仍有问题：
1. 检查系统字体设置
2. 确保中文语言包已安装

### 问题5: 程序运行缓慢

**优化建议**:

1. **使用GPU加速**（如有NVIDIA显卡）:
   ```cmd
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

2. **关闭其他程序**: 释放内存

3. **使用较小的图像**: 推荐分辨率1024x1024以下

### 问题6: "torch下载失败"

**原因**: PyTorch包较大（~700MB）

**解决方案**:

方法1 - 使用清华镜像：
```cmd
pip install torch torchvision -i https://pypi.tuna.tsinghua.edu.cn/simple
```

方法2 - 手动下载：
1. 访问: https://download.pytorch.org/whl/torch_stable.html
2. 下载对应版本的.whl文件
3. 本地安装:
   ```cmd
   pip install path\to\downloaded\torch.whl
   ```

---

## 创建桌面快捷方式

### 方法1: 手动创建批处理文件

1. 在项目目录创建 `启动程序.bat` 文件
2. 内容如下：

```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python wildlife_recognition_app.py
pause
```

3. 双击运行即可启动程序

### 方法2: 创建快捷方式

1. 右键桌面 → 新建 → 快捷方式
2. 位置输入：
   ```
   C:\Users\YourName\Wildlife Recognition\venv\Scripts\python.exe "C:\Users\YourName\Wildlife Recognition\wildlife_recognition_app.py"
   ```
3. 命名为 "野生动物识别系统"

---

## 卸载指南

### 1. 删除虚拟环境

```cmd
rmdir /s venv
```

### 2. 删除项目文件

直接删除项目文件夹即可

### 3. 卸载Python（可选）

通过 "设置" → "应用" → "Python" → "卸载"

---

## 性能优化

### GPU加速（NVIDIA显卡）

1. **安装CUDA Toolkit**:
   - 下载: https://developer.nvidia.com/cuda-downloads
   - 选择Windows版本安装

2. **安装GPU版PyTorch**:
   ```cmd
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

3. **验证GPU**:
   ```cmd
   python -c "import torch; print(torch.cuda.is_available())"
   ```
   应输出: `True`

### 设置CPU线程数

在 `siamese_network.py` 中添加：

```python
import torch
torch.set_num_threads(4)  # 根据CPU核心数调整
```

---

## 技术支持

### 系统信息收集

如遇问题，请提供以下信息：

1. **Windows版本**:
   ```cmd
   winver
   ```

2. **Python版本**:
   ```cmd
   python --version
   ```

3. **已安装包**:
   ```cmd
   pip list
   ```

4. **错误信息**: 完整的错误堆栈跟踪

---

## 附录: 目录结构

```
Wildlife Image Recognition and Classification System/
│
├── wildlife_recognition_app.py    # 主程序（GUI）
├── siamese_network.py             # 模型文件
├── requirements.txt               # 依赖列表
├── README.md                      # 项目说明
├── 技术文档.md                    # 技术文档
├── Windows安装指南.md             # 本文档
│
├── venv/                          # 虚拟环境（安装后创建）
│   ├── Scripts/
│   │   ├── activate.bat
│   │   └── python.exe
│   └── Lib/
│
└── .gitignore                     # Git忽略文件
```

---

## 下一步

安装完成后，建议：

1. **阅读技术文档.md** 了解系统原理
2. **准备测试图像** 进行识别测试
3. **查看支持的物种列表** （在技术文档中）

---

**祝您使用愉快！**

如有任何问题，请参考常见问题部分或联系技术支持。
