import asyncio
import logging
import os
from configparser import ConfigParser

from pyppeteer import launch

config = ConfigParser()

# 加载config.ini配置文件
config_file = 'config.ini'
config.read(config_file, encoding='utf-8')

apps = {app_name: config['apps'][app_name] for app_name in config['apps']}
button_selector = config.get('selectors', 'button_selector')
version_selector = config.get('selectors', 'version_selector')
versions_file_path = config.get('paths', 'versions_file')
# 检查是否正确加载了配置文件的'selectors'部分
# if 'selectors' in config:
#     for selector in config['selectors']:
#         print(selector, "=", config['selectors'][selector])
# else:
#     print("Unable to find 'selectors' section in the config file.")
# for app, url in apps.items():
#     print(app, "URL:", url)

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config_file = 'config.ini'
config = ConfigParser()

def ensure_config_file(file_path):
    """确保配置文件存在，并读取配置"""
    if not os.path.exists(file_path):
        logging.error(f"Config file '{file_path}' not found.")
        raise FileNotFoundError(f"Config file '{file_path}' not found.")
    else:
        config.read(file_path, encoding='utf-8')
        logging.info(f"Config file '{file_path}' loaded.")

ensure_config_file(config_file)

# 获取配置参数

button_selector = config.get('selectors', 'button_selector', fallback=None)
version_selector = config.get('selectors', 'version_selector', fallback=None)
versions_file_path = config.get('paths', 'versions_file', fallback='versions.txt')

if not button_selector or not version_selector:
    logging.error("Selector configuration is missing in the config file.")
    raise ValueError("Selector configuration is missing in the config file.")

class VersionCheckError(Exception):
    pass

async def get_app_version(url: str, button_selector: str, version_selector: str) -> str:
    """获取指定应用在Google Play商店的版本号"""
    browser = await launch({'headless': True})
    page = await browser.newPage()
    try:
        await page.goto(url)
        await page.waitForSelector(button_selector, options={'timeout': 5000})
        await page.click(button_selector)
        await page.waitForSelector(version_selector, options={'timeout': 5000})
        version = await page.evaluate(f'document.querySelector("{version_selector}").textContent')
    except Exception as e:
        logging.error(f"Failed to get version for {url}: {e}")
        raise VersionCheckError(f"Failed to get version for {url}: {e}")
    finally:
        await browser.close()
    return version.strip()

# async def check_for_updates():
#     """检查应用程序版本更新"""
#     local_versions = {}  # 应该从本地文件读取已记录的版本号
#     # 示例应用和URL，应从配置文件读取
#     apps = {
#         'ExampleApp': 'https://play.google.com/store/apps/details?id=com.example'
#     }
#     updates = {}
#     for name, url in apps.items():
#         try:
#             version = await get_app_version(url, button_selector, version_selector)
#             if name in local_versions and version != local_versions[name]:
#                 updates[name] = version
#                 logging.info(f"{name} has an update: {version}")
#             else:
#                 logging.info(f"No updates found for {name}.")
#         except VersionCheckError:
#             continue
#     # 将获取的新版本号写入本地文件

def read_versions_file(file_path):
    """从给定的文件路径读取应用的版本信息。

    Args:
        file_path (str): 包含版本信息的文件路径。

    Returns:
        dict: 包含应用名称作为键和版本号作为值的字典。
    """
    versions = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # 假设文件中每行的格式为'app_name=version'
                app_name, version = line.strip().split('=')
                versions[app_name] = version
    except FileNotFoundError:
        print(f"文件'{file_path}'未找到，将以空字典继续。")
    except Exception as e:
        print(f"读取文件'{file_path}'时出现错误: {e}")
    return versions


def write_versions_file(file_path, versions):
    """将应用的版本信息写入到给定的文件路径。

    Args:
        file_path (str): 要写入版本信息的文件路径。
        versions (dict): 包含应用名称作为键和版本号作为值的字典。
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for app_name, version in versions.items():
                file.write(f'{app_name}={version}\n')
    except Exception as e:
        print(f"写入文件'{file_path}'时出现错误: {e}")

async def check_for_updates(apps, button_selector, version_selector, versions_file):
    """检查应用程序版本更新"""
    local_versions = read_versions_file(versions_file)  # 从本地文件读取已记录的版本号
    updates = {}
    for name, url in apps.items():
        try:
            version = await get_app_version(url, button_selector, version_selector)
            if name in local_versions and version != local_versions[name]:
                updates[name] = version
                logging.info(f"{name} has an update: {version}")
            else:
                logging.info(f"No updates found for {name}.")
        except VersionCheckError as e:
            logging.error(f"Error checking update for {name}: {e}")
            continue
    # 将获取的新版本号写入本地文件
    write_versions_file(versions_file, {**local_versions, **updates})


# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(check_for_updates())
if __name__ == "__main__":
    config = ConfigParser()
    config.read('config.ini', encoding='utf-8')

    # 从config.ini中读取apps及其他配置
    apps = {app: config['apps'][app] for app in config['apps']}
    button_selector = config.get('selectors', 'button_selector')
    version_selector = config.get('selectors', 'version_selector')
    versions_file_path = config.get('paths', 'versions_file')

    # 使用读取的配置作为参数调用check_for_updates()
    asyncio.run(check_for_updates(apps, button_selector, version_selector, versions_file_path))
