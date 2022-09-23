import asyncio
import subprocess


async def invoke_simple_cmd(cmd: str) -> str:
    proc = await asyncio.create_subprocess_shell(
        cmd=cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    proc.stdin.writelines(['systemctl status kite2.service'.encode()])
    out = await proc.stdout.read()
    return out.decode()
