import psutil
import time
import datetime

"""
获取系统基本信息
"""

EXPAND = 1024 * 1024


def get_memory_info():
    """
    获取系统内存使用情况
    :return:
    """
    mem = psutil.virtual_memory()

    return f"""内存状态如下:
系统的内存容量为: {int(mem.total / EXPAND)} MB
系统的内存已使用容量为: {int(mem.used / EXPAND)} MB
系统可用的内存容量为: {int((mem.total - mem.used) / EXPAND)} MB
"""


def get_disks_info():
    disk_str = "硬盘信息如下:\n"
    disk_status = psutil.disk_partitions()

    for item in disk_status:
        p = item.device
        disk = psutil.disk_usage(p)

        disk_str += f"""{item}
{p}盘容量为: {int(disk.total / EXPAND)} MB
{p}盘已使用容量为: {int(disk.used / EXPAND)} MB
{p}盘可用的内存容量为: {int(disk.free / EXPAND)} MB

"""
    return disk_str


def get_users_info():
    from datetime import datetime
    user_status = psutil.users()

    user_str_set = set()
    for item in user_status:
        user_str_set.add(f"""用户名：{item.name}
登录主机: {item.host}
登录时间: {datetime.fromtimestamp(item.started)}

""")

    return f"""登录用户信息如下:
{''.join(user_str_set)}    
"""


if __name__ == '__main__':
    print(get_memory_info())
    print(get_disks_info())
    print(get_users_info())
