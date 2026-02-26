# Paper CN Agent Network (MVP)

一个可运行的“英文论文 -> 中文论文”多 Agent 流水线示例。

## 功能
- 结构/文本抽取（支持 `.txt` / `.md` / `.pdf`）
- 分段切分（按段落）
- 术语标准化（自定义术语表）
- 翻译 Agent（支持 `mock` 和 OpenAI）
- 学术风格统一 Agent
- QA Agent（数字/术语/长度异常检查）
- 结果导出（中英对照 + 中文稿 + 中文 PDF）
- 可视化界面（Streamlit 上传并下载结果）

## 目录
- `main.py`: 入口 CLI
- `pipeline.py`: Agent 网络编排
- `agents/`: 各 Agent 实现
- `config/terms.csv`: 术语库
- `data/input/`: 输入文档
- `data/output/`: 输出结果

## 快速开始
```bash
cd paper_cn_agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

1) 准备输入文件（推荐先用 txt）
```bash
cp /path/to/your_english_paper.txt data/input/paper.txt
```

2) 运行（离线 mock 翻译）
```bash
python main.py --input data/input/paper.txt --translator mock
```

3) 使用 OpenAI 翻译（可选）
```bash
export OPENAI_API_KEY=your_key
python main.py --input data/input/paper.txt --translator openai --model gpt-4.1-mini
```

4) 直接处理 PDF
```bash
python main.py --input data/input/paper.pdf --translator mock
```

5) 启动可视化界面
```bash
streamlit run app.py
```

## 输出
- `data/output/<name>.zh.md`: 中文稿
- `data/output/<name>.bilingual.md`: 中英对照
- `data/output/<name>.qa.json`: 质量检查结果
- `data/output/<name>.zh.pdf`: 中文 PDF

## 术语库格式
`config/terms.csv`

```csv
en,zh
building envelope,建筑围护结构
heat pump,热泵
net zero,净零
```

## 下一步建议
- 增加引用编号与图表锚点保真
- 增加人工审校界面（streamlit）
