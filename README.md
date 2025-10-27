# 野生动物图像识别系统

基于深度学习的野生动物物种自动识别系统

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-orange)

---

## 📋 项目简介

野生动物图像识别系统是一个基于PyTorch深度学习框架的计算机视觉应用程序。系统采用预训练的ResNet18卷积神经网络，通过迁移学习技术，能够准确识别150多种野生动物。

### 主要特点

- ✅ **高精度识别**: 基于ImageNet预训练模型，识别准确率高
- ✅ **中文界面**: 完整的中文图形用户界面
- ✅ **实时处理**: 快速图像预测（0.1-0.5秒）
- ✅ **易于使用**: 简洁直观的操作界面
- ✅ **跨平台支持**: 支持Windows、Linux和macOS
- ✅ **离线运行**: 首次下载模型后可离线使用

---

## 🎯 功能特性

### 核心功能

1. **图像上传**
   - 支持多种格式：JPG、PNG、BMP、GIF、WEBP等
   - 自动图像预处理和缩放

2. **物种识别**
   - 识别150+种野生动物
   - 提供Top-5预测结果
   - 显示置信度百分比

3. **结果展示**
   - 可视化置信度条
   - 排名显示（金银铜牌）
   - 详细的预测信息

4. **用户界面**
   - 现代化设计
   - 中文本地化
   - 实时状态更新

---

## 🖥️ 系统要求

### 硬件要求

| 组件 | 最低配置 | 推荐配置 |
|------|----------|----------|
| CPU | 双核 2.0GHz | 四核 3.0GHz+ |
| 内存 | 4GB | 8GB+ |
| 存储 | 2GB | 5GB+ |
| GPU | 无（可选） | NVIDIA CUDA支持 |

### 软件要求

- **操作系统**:
  - Windows 10/11
  - Ubuntu 20.04+ / Linux
  - macOS 10.15+
- **Python**: 3.8 - 3.11（推荐3.10）
- **显示**: 最小分辨率1024x768

---

## 📦 安装指南

### 快速开始（所有平台）

1. **克隆仓库**
   ```bash
   git clone <repository-url>
   cd "Wildlife Image Recognition and Classification System"
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行程序**
   ```bash
   python wildlife_recognition_app.py
   ```

### Windows系统

详细的Windows安装步骤请参阅 [**Windows安装指南.md**](Windows安装指南.md)

关键步骤：
```cmd
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行程序
python wildlife_recognition_app.py
```

### Linux/Mac系统

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行程序
python3 wildlife_recognition_app.py
```

---

## 📖 使用说明

### 基本操作流程

1. **启动程序**
   - 运行 `python wildlife_recognition_app.py`
   - 等待界面加载完成

2. **上传图像**
   - 点击 "📁 上传图像" 按钮
   - 从文件对话框选择野生动物图片
   - 支持的格式：JPG、JPEG、PNG、BMP等

3. **查看结果**
   - 左侧显示上传的图像
   - 右侧显示前5个预测结果
   - 每个结果包含物种名称和置信度

4. **重新识别**
   - 点击 "🗑 清除" 按钮
   - 上传新的图像进行识别

### 界面说明

```
┌─────────────────────────────────────────────┐
│       野生动物图像识别系统（标题栏）         │
├──────────────┬────────────────────────────┤
│ 📁 上传图像  │ 🗑 清除                    │
├──────────────┴────────────────────────────┤
│                │                           │
│   已上传图像    │     前五预测结果          │
│   （左侧）     │     （右侧）              │
│                │                           │
│                │   🥇 物种1  85.32%        │
│                │   🥈 物种2  8.47%         │
│                │   🥉 物种3  3.21%         │
│                │   4️⃣ 物种4  2.15%         │
│                │   5️⃣ 物种5  0.85%         │
│                │                           │
├────────────────────────────────────────────┤
│ 状态栏: 就绪 / 正在预测... / 预测完成！    │
└────────────────────────────────────────────┘
```

---

## 🔬 技术架构

### 模型架构

**ResNet18 卷积神经网络**

```
输入图像 (224×224×3)
    ↓
卷积层 + 残差块
    ↓
特征提取 (512维)
    ↓
全连接层
    ↓
Softmax分类 (1000类)
    ↓
过滤野生动物类别 (150+种)
    ↓
Top-5输出
```

### 核心技术

- **迁移学习**: 利用ImageNet预训练权重
- **残差网络**: ResNet18架构
- **图像预处理**: 标准化和归一化
- **多线程**: 后台预测，界面不卡顿

详细技术说明请参阅 [**技术文档.md**](技术文档.md)

---

## 📊 支持的物种

系统基于ImageNet数据集，支持识别以下类别的野生动物：

### 大型猫科动物
- 豹 (Leopard)
- 雪豹 (Snow Leopard)
- 美洲豹 (Jaguar)
- 狮子 (Lion)
- 老虎 (Tiger)
- 猎豹 (Cheetah)

### 鸟类（40+种）
- 白头鹰 (Bald Eagle)
- 秃鹫 (Vulture)
- 猫头鹰 (Owl)
- 孔雀 (Peacock)
- 火烈鸟 (Flamingo)
- 鹈鹕 (Pelican)
- 企鹅 (Penguin)
- 鹦鹉 (Macaw)

### 大型哺乳动物
- 非洲象 (African Elephant)
- 印度象 (Indian Elephant)
- 长颈鹿 (Giraffe)
- 犀牛 (Rhinoceros)
- 河马 (Hippopotamus)
- 斑马 (Zebra)

### 灵长类（12+种）
- 大猩猩 (Gorilla)
- 黑猩猩 (Chimpanzee)
- 猩猩 (Orangutan)
- 狒狒 (Baboon)

### 其他
- 熊类（棕熊、黑熊、北极熊）
- 爬行动物（鳄鱼、蜥蜴、海龟）
- 海洋哺乳动物（海豹、海狮）

**完整物种列表请参见技术文档**

---

## 📁 项目结构

```
Wildlife Image Recognition and Classification System/
│
├── wildlife_recognition_app.py    # 主程序（GUI）
├── siamese_network.py             # 深度学习模型
├── requirements.txt               # Python依赖包
├── README.md                      # 项目说明（本文件）
├── 技术文档.md                    # 详细技术文档
├── Windows安装指南.md             # Windows专用安装指南
├── TUTORIAL.txt                   # 学习教程
├── .gitignore                     # Git忽略规则
│
└── test_images/                   # 测试图像（可选）
    ├── lion.jpg
    ├── eagle.jpg
    └── ...
```

---

## 🚀 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 推理速度（CPU） | 0.1-0.5秒 | 单张图像 |
| 推理速度（GPU） | 0.01-0.05秒 | 单张图像 |
| 模型大小 | 44.7MB | ResNet18权重 |
| 内存占用 | 500MB-1GB | 运行时 |
| 准确率 | 70-85% | ImageNet验证集 |
| 支持格式 | 10+ | JPG/PNG/BMP等 |

---

## ❓ 常见问题

### Q1: 为什么首次运行需要下载模型？

**A**: 系统使用预训练的ResNet18模型（44.7MB），首次运行时会自动从PyTorch官方服务器下载。下载后会缓存到本地，之后可离线使用。

### Q2: 识别结果不准确怎么办？

**A**: 可能原因和解决方案：
- **图像质量差**: 使用清晰、高分辨率的图像
- **动物不在中心**: 确保动物占据画面主要部分
- **物种不支持**: 检查是否为系统支持的150+物种
- **背景复杂**: 尽量使用背景简洁的图像

### Q3: Windows上中文显示异常？

**A**: 程序使用 "Microsoft YaHei" 字体，Windows 10/11默认包含。如有问题，请确保：
- 系统已安装中文语言包
- 字体文件完整

### Q4: 如何使用GPU加速？

**A**:
```bash
# 安装GPU版本的PyTorch（NVIDIA显卡）
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Q5: 程序运行缓慢？

**A**: 优化建议：
1. 使用GPU（如可用）
2. 减小输入图像尺寸
3. 关闭其他占用资源的程序
4. 增加系统内存

---

## 🛠️ 开发与扩展

### 添加新物种

1. 修改 `siamese_network.py` 中的 `IMAGENET_WILDLIFE_CLASSES`
2. 添加ImageNet类别ID和中文名称
3. 重新运行程序

### 使用更强大的模型

```python
# 在 siamese_network.py 中替换模型
# ResNet18 → ResNet50
self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
```

---

## 📄 依赖项

```
torch>=2.0.0          # PyTorch深度学习框架
torchvision>=0.15.0   # 计算机视觉工具
Pillow>=10.0.0        # 图像处理库
numpy>=1.24.0         # 数值计算库
```

Python内置库：
- tkinter（图形界面）
- threading（多线程）
- os（文件操作）

---

## 📝 许可证

本项目仅供学习和研究使用。

---

## 👥 贡献者

感谢所有为本项目做出贡献的开发者。

---

## 📞 技术支持

如有问题或建议，请：

1. 查阅 [技术文档.md](技术文档.md)
2. 查看 [Windows安装指南.md](Windows安装指南.md)
3. 阅读常见问题部分
4. 提交Issue到项目仓库

---

## 🔗 参考资料

- [PyTorch官方文档](https://pytorch.org/docs/)
- [ResNet论文](https://arxiv.org/abs/1512.03385)
- [ImageNet数据集](https://www.image-net.org/)
- [Python Tkinter教程](https://docs.python.org/3/library/tkinter.html)

---

**感谢使用野生动物图像识别系统！**

如果本项目对您有帮助，欢迎⭐Star支持！
