# edu-question-generator

[English](README.md) | [简体中文](README_zh.md)

`edu-question-generator` 是一个开源 Python 项目，帮助家教、教师和培训机构从结构化模板生成初中数学和物理练习题，并导出为 DOCX 文档。

当前版本：`v0.1.0`。

项目会为每份练习生成两个文件：

- 学生版：只有题目，不含答案
- 教师版：包含题目和详细解答

所有内容都在本地生成，不需要付费 API。

## 功能

- 内置初中数学和物理题目模板
- 支持选择科目、主题、难度和题目数量
- 支持使用随机种子生成可复现的练习卷
- 使用 `python-docx` 导出 DOCX
- 使用简单的 dataclass 数据模型
- 使用容易修改的 JSON 模板
- 提供简单命令行工具
- 包含生成器、模板加载、公式计算和 DOCX 导出的测试

## 安装

克隆仓库：

```bash
git clone https://github.com/gaopu1/edu-question-generator.git
cd edu-question-generator
```

创建并启用虚拟环境。

Windows：

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS 或 Linux：

```bash
python -m venv .venv
source .venv/bin/activate
```

安装依赖：

```bash
python -m pip install -r requirements.txt
```

如果要以开发模式安装项目，也可以运行：

```bash
python -m pip install -e ".[dev]"
```

## 快速开始

查看可用模板：

```bash
python -m edu_question_generator.cli --list-options
```

生成 5 道代数练习题：

```bash
python -m edu_question_generator.cli --subject math --topic algebra --difficulty easy --count 5 --seed 42
```

## 示例命令

生成一份物理运动主题练习卷，并保存到自定义目录：

```bash
python -m edu_question_generator.cli --subject physics --topic motion --difficulty easy --count 10 --output-dir worksheets
```

## 输出说明

默认输出目录是 `examples/output/`。

运行：

```bash
python -m edu_question_generator.cli --subject math --topic algebra --difficulty easy --count 5 --seed 42
```

会生成：

```text
examples/output/math_algebra_easy_student.docx
examples/output/math_algebra_easy_teacher.docx
```

学生版包含编号题目和答题空白。教师版包含相同题目，并在每题下方给出简短解题过程。

## 修改题目模板

模板位于 `edu_question_generator/templates/`，格式为 JSON。

每个模板包含：

- `prompt`：学生看到的题目
- `answer`：教师版中的解答
- `variables`：随机生成的变量
- `formulas`：根据变量计算出的结果

示例：

```json
{
  "id": "math-geometry-rectangle-easy",
  "subject": "math",
  "topic": "geometry",
  "difficulty": "easy",
  "prompt": "A rectangle has length {length} cm and width {width} cm. Find its area.",
  "answer": "Area = length x width = {length} x {width} = {area} square cm.",
  "variables": [
    {"name": "length", "min": 4, "max": 18},
    {"name": "width", "min": 2, "max": 12}
  ],
  "formulas": {
    "area": "length * width"
  }
}
```

公式只支持简单算术表达式，方便初学者理解和维护。

## 运行测试

```bash
python -m pytest
```

## 路线图

- 增加更多初中数学和物理主题
- 支持班级、日期、学生姓名等练习卷信息
- 增加 YAML 模板支持
- 增加仅答案版复习资料
- 增加模板校验报告
- 将命令行工具打包为可安装的 Python 包

## 参与贡献

欢迎贡献模板、文档和测试。提交 Pull Request 前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

MIT。详情见 [LICENSE](LICENSE)。
