# KLayout Manual Crawler 📊
# KLayout手册爬虫工具 📊

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/Python-3.6+-green.svg)

> **Transform the KLayout manual index (https://www.klayout.de/doc.html) into a knowledge base for large language models**
> 
> **将KLayout手册索引 (https://www.klayout.de/doc.html) 转化为大语言模型可用的知识库**

## 🔍 Project Overview | 项目概述

KLayout Manual Crawler is a specialized web crawler designed specifically for the KLayout documentation website (https://www.klayout.de/doc.html). It intelligently crawls all relevant pages of the KLayout documentation and generates a structured sitemap. This tool is built for chip designers and semiconductor researchers to significantly improve retrieval efficiency of KLayout professional knowledge when using large language models like ChatGPT or Claude.

KLayout Manual Crawler是一个专门为KLayout文档网站 (https://www.klayout.de/doc.html) 设计的爬虫工具，它能够智能抓取KLayout文档网站的所有相关页面，并生成结构化的站点地图（sitemap）。这个工具专为芯片设计师和半导体研究人员打造，可显著提升在使用大型语言模型（如ChatGPT、Claude）等时对KLayout专业知识的检索效率。

## 🌟 Core Features | 核心功能

- **Intelligent Crawling** - Automatically identifies and crawls all relevant pages from the KLayout documentation website
- **Parallel Processing** - Utilizes multi-threading technology to significantly increase crawling speed
- **Precise Filtering** - Intelligently filters irrelevant content, focusing on documentation and manual pages
- **Structured Output** - Generates a sitemap in CSV format, facilitating subsequent processing and import

---

- **智能抓取** - 自动识别并抓取KLayout文档网站的所有相关页面
- **并行处理** - 采用多线程技术，大幅提升爬取速度
- **精准过滤** - 智能过滤无关内容，专注于文档和手册页面
- **结构化输出** - 生成CSV格式的站点地图，方便后续处理和导入

## 🚀 Why Do We Need This Tool? | 为什么需要这个工具？

The KLayout manual at https://www.klayout.de/doc.html is a comprehensive resource for this powerful layout design and GDS viewer tool. However, these valuable documents are scattered across numerous subpages, making it difficult to directly import them into large language models. This tool addresses this challenge by:

1. **Simplifying Knowledge Base Construction** - One-click crawling of all relevant documentation pages from the main KLayout manual
2. **Enhancing Retrieval Precision** - Structured sitemap improves search quality
3. **Making AI Assistants Smarter** - Providing your AI assistant with comprehensive KLayout professional knowledge

---

KLayout官方手册网站 (https://www.klayout.de/doc.html) 作为一款强大的布图设计和GDS查看工具的参考资源，拥有庞大而复杂的文档体系。然而，这些宝贵的文档分散在众多子网页中，使得直接将其导入大语言模型变得困难。本工具解决了这一挑战，使得：

1. **知识库构建更简单** - 一键抓取KLayout官方手册的所有相关文档页面
2. **检索更精准** - 结构化的站点地图提升检索质量
3. **AI助手更智能** - 为你的AI助手提供完整的KLayout专业知识

## 💻 How to Use | 使用方法

### 1. Install Dependencies | 安装依赖

```bash
pip install requests beautifulsoup4
```

### 2. Run the Crawler | 运行爬虫

```bash
python klayout_crawler.py
```

### 3. Get the Sitemap | 获取站点地图

After the script finishes execution, a `klayout_urls.csv` file will be generated in the current directory, containing all the crawled URLs from the KLayout documentation site.

脚本执行完成后，将在当前目录生成`klayout_urls.csv`文件，包含从KLayout文档网站抓取的所有URL。

## 🔧 Code Analysis | 代码解析

```python
# Core functionality highlights
# 核心功能亮点

# Starting URL - The main KLayout documentation page
# 起始URL - KLayout文档主页
start_url = "https://www.klayout.de/doc.html"
base_url = "https://www.klayout.de/"

# 1. Intelligent URL filtering - Ensuring only relevant documentation pages are crawled
# 1. 智能URL过滤 - 确保只抓取相关文档页面
def is_valid_url(url):
    # Precise function to determine if a URL should be crawled
    # 判断URL是否应该被爬取的精确函数
    parsed = urlparse(url)
    
    # Must be klayout.de domain
    # 必须是klayout.de域名
    if "klayout.de" not in parsed.netloc:
        return False
    
    # Exclude unwanted file types
    # 排除不需要的文件类型
    exclude_extensions = ['.zip', '.tar', '.gz', '.exe', '.bin', '.jpg', '.png', '.gif']
    if any(url.lower().endswith(ext) for ext in exclude_extensions):
        return False
    
    # Must be documentation-related URL
    # 必须是文档相关的URL
    doc_indicators = ['/doc', 'manual', 'reference', 'about', 'index']
    return any(indicator in url.lower() for indicator in doc_indicators)

# 2. Efficient parallel processing - Significantly increases crawling speed
# 2. 高效并行处理 - 显著提升抓取速度
crawler_manager(max_workers=30)  # Number of threads can be adjusted as needed
                                # 可根据需要调整线程数
```

## 📊 Use Cases | 使用场景

- **Building Knowledge Bases for Custom AI Assistants** - Using the generated sitemap of KLayout's documentation to train specialized KLayout assistants
- **Improving LLM Responses to Chip Design Questions** - Providing large language models with professional KLayout reference materials
- **Creating Personal Knowledge Management Systems** - Integrating KLayout documentation into personal knowledge bases
- **Facilitating Team Collaboration** - Providing unified KLayout documentation indexes for semiconductor design teams

---

- **为定制AI助手构建知识库** - 将生成的KLayout文档站点地图用于训练专门的KLayout助手
- **提升LLM对芯片设计问题的回答质量** - 为大语言模型提供专业的KLayout参考资料
- **创建个人知识管理系统** - 将KLayout文档整合到个人知识库
- **辅助团队协作** - 为半导体设计团队提供统一的KLayout文档索引

## 🔄 Post-Processing Suggestions | 后续处理建议

After generating the sitemap from https://www.klayout.de/doc.html, you can:

1. Use a crawler to further capture the specific content of each URL
2. Structurally process the content (e.g., segmentation, extraction of key information)
3. Import the processed content into a large language model's knowledge base
4. Build a specialized KLayout query system or custom AI assistant

---

生成KLayout文档网站 (https://www.klayout.de/doc.html) 的站点地图后，您可以：

1. 使用爬虫进一步抓取每个URL的具体内容
2. 将内容进行结构化处理（如分段、提取关键信息）
3. 将处理后的内容导入大语言模型的知识库
4. 构建专门的KLayout查询系统或自定义AI助手

## 📝 Notes | 注意事项

- Please respect the KLayout website's robots.txt rules
- Control crawling frequency to avoid excessive burden on the server
- The crawled content is for personal learning and research use only

---

- 请尊重KLayout网站的robots.txt规则
- 控制爬取频率，避免对服务器造成过大负担
- 抓取的内容仅供个人学习和研究使用

## 📄 License | 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

本项目采用MIT许可证 - 详见[LICENSE](LICENSE)文件

## 🤝 Contribution | 贡献

Contributions and feedback through Issues or Pull Requests are welcome!

欢迎通过Issues或Pull Requests进行贡献和反馈！

---

> 💡 **Tip | 提示**：This tool can significantly improve the efficiency of chip designers and researchers in using large language models to solve KLayout-related problems. Whether it's layout design, DRC rules, or KLayout script programming, your AI assistant will be able to provide more accurate guidance by having access to the complete KLayout documentation.
>
> 💡 **提示**：这个工具能够显著提升芯片设计师和研究人员使用大语言模型解决KLayout相关问题的效率。无论是对布图设计、DRC规则还是KLayout脚本编程，通过获取完整的KLayout文档，您的AI助手都将能够提供更精确的指导。
