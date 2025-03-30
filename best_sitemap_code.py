import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import time
import re

# 初始URL和基本URL
base_url = "https://www.klayout.de/"
sitemap_urls = [
    "https://www.klayout.de/doc.html",
    "https://www.klayout.de/doc/index.html",
    "https://www.klayout.de/doc-qt5/index.html",
    "https://www.klayout.de/doc-qt5/manual/index.html",
    "https://www.klayout.de/doc-qt5/about/index.html",
    "https://www.klayout.de/doc-qt5/code/index.html"
]

# 存储所有找到的URL
all_urls = set()

def extract_patterns(base_url):
    """从基本URL提取可能的规律性URL模式"""
    patterns = []
    
    # 针对KLayout文档的常见路径模式
    common_paths = [
        "/doc/",
        "/doc-qt5/",
        "/doc-qt5/manual/",
        "/doc-qt5/about/",
        "/doc-qt5/code/",
        "/doc/manual/",
        "/doc/about/",
        "/doc/code/"
    ]
    
    # 常见的文件命名模式
    file_patterns = [
        "class_*.html",
        "module_*.html",
        "namespace_*.html",
        "index.html",
        "*.html"
    ]
    
    # 组合生成可能的URL模式
    for path in common_paths:
        for pattern in file_patterns:
            patterns.append(base_url + path + pattern)
    
    return patterns

def save_patterns_to_file(patterns, filename="url_patterns.txt"):
    """将URL模式保存到文件中，便于手动编辑"""
    with open(filename, 'w', encoding='utf-8') as f:
        for pattern in patterns:
            f.write(pattern + '\n')
    print(f"URL模式已保存到 {filename}")

def read_patterns_from_file(filename="url_patterns.txt"):
    """从文件读取URL模式"""
    patterns = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    patterns.append(line)
        print(f"从 {filename} 读取了 {len(patterns)} 个URL模式")
    except FileNotFoundError:
        print(f"文件 {filename} 不存在，将使用默认模式")
        patterns = extract_patterns(base_url)
    return patterns

def fetch_page_with_retry(url, max_retries=3, delay=1):
    """带重试机制的页面获取函数"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                print(f"获取 {url} 失败: HTTP {response.status_code}")
        except Exception as e:
            print(f"获取 {url} 时出错 (尝试 {attempt+1}/{max_retries}): {e}")
        
        if attempt < max_retries - 1:
            time.sleep(delay)
    
    return None

def find_links_in_sitemap(url):
    """从站点地图页面提取所有链接"""
    content = fetch_page_with_retry(url)
    if not content:
        print(f"无法获取站点地图: {url}")
        return []
    
    soup = BeautifulSoup(content, 'html.parser')
    links = []
    
    # 查找所有链接
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        full_url = urljoin(url, href)
        
        # 只保留klayout.de域名的链接
        if "klayout.de" in full_url and not full_url.endswith(('.zip', '.tar.gz', '.exe')):
            # 规范化URL
            parsed = urlparse(full_url)
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                normalized_url += f"?{parsed.query}"
            
            links.append(normalized_url)
    
    return links

def expand_patterns(patterns):
    """展开URL模式生成具体URL列表"""
    expanded_urls = set()
    
    for pattern in patterns:
        if '*' in pattern:
            # 这里我们需要手动展开通配符，转为正则表达式
            pattern_regex = pattern.replace('.', '\\.').replace('*', '.*')
            # 如果有通配符，需要手动确认或者提供可能的值
            print(f"发现通配符模式: {pattern}")
            print("请注意这需要手动处理或提供可能的替换值")
            
            # 添加一些常见的类名和模块名作为示例
            # 实际使用时可能需要手动编辑或从其他来源获取
            common_names = ["QWidget", "QApplication", "QString", "tl", "db", "rdb", "lay"]
            for name in common_names:
                expanded_url = pattern.replace('*', name)
                expanded_urls.add(expanded_url)
        else:
            expanded_urls.add(pattern)
    
    return expanded_urls

def process_sitemap():
    """处理所有站点地图页面"""
    for sitemap_url in sitemap_urls:
        print(f"处理站点地图: {sitemap_url}")
        links = find_links_in_sitemap(sitemap_url)
        for link in links:
            all_urls.add(link)
        print(f"从 {sitemap_url} 找到 {len(links)} 个链接")
        time.sleep(2)  # 添加延迟，避免请求过于频繁

def save_urls_to_csv(urls, filename="best_klayout_urls.csv"):
    """将URL列表保存到CSV文件"""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["URL"])
        for url in sorted(urls):
            writer.writerow([url])
    print(f"已将 {len(urls)} 个URL保存到 {filename}")

def main():
    """主函数"""
    print("开始从KLayout文档站点提取URL...")
    
    # 首先从站点地图提取链接
    process_sitemap()
    print(f"从站点地图中提取了 {len(all_urls)} 个链接")
    
    # 然后基于模式生成更多链接
    patterns = extract_patterns(base_url)
    save_patterns_to_file(patterns)
    
    # 可以在这里手动编辑url_patterns.txt文件，添加或修改模式
    input("已生成URL模式文件。如果需要，请编辑 url_patterns.txt 文件，然后按Enter继续...")
    
    # 读取可能已编辑的模式
    patterns = read_patterns_from_file()
    
    # 展开模式生成具体URL
    pattern_urls = expand_patterns(patterns)
    print(f"从模式生成了 {len(pattern_urls)} 个可能的URL")
    
    # 合并所有URL
    all_urls.update(pattern_urls)
    print(f"总共生成了 {len(all_urls)} 个唯一URL")
    
    # 保存结果
    save_urls_to_csv(all_urls)
    print("URL提取完成!")

if __name__ == "__main__":
    main()