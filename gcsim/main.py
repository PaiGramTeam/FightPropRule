import asyncio
import json
import platform
from pathlib import Path

import aiofiles
import re
import gcsim_pypi

data_path = Path("gcsim.json")
gcsim_path = Path("gcsim")
scripts_path = gcsim_path / "scripts"
temp_path = gcsim_path / "temp"
temp_path.mkdir(exist_ok=True)


def _get_gcsim_bin_name() -> str:
    if platform.system() == "Windows":
        return "gcsim.exe"
    bin_name = "gcsim"
    if platform.system() == "Darwin":
        bin_name += ".darwin"
    if platform.machine() == "arm64":
        bin_name += ".arm64"
    return bin_name


gcsim_pypi_path = Path(gcsim_pypi.__file__).parent
bin_path = gcsim_pypi_path.joinpath("bin").joinpath(_get_gcsim_bin_name())


async def run_gcsim(path: Path) -> bool:
    try:
        process = await asyncio.create_subprocess_exec(
            bin_path,
            "-c",
            path.absolute().as_posix(),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()
        err = stderr.decode()
        if err:
            print(f"{path.name} 解析失败 {err}")
            return False
        return True
    except Exception:
        return False


async def modify_script(path: Path):
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        content = await f.read()
    content = re.sub(r"iteration=\d+", "iteration=1", content)
    new_path = temp_path / path.name
    async with aiofiles.open(new_path, "w", encoding="utf-8") as f:
        await f.write(content)


async def main():
    for path in scripts_path.iterdir():
        if path.is_file() and path.suffix == ".txt":
            await modify_script(path)
    allow = []
    for path in temp_path.iterdir():
        if await run_gcsim(temp_path / path.name):
            allow.append(path)
    data = {}
    for path in allow:
        async with aiofiles.open(path, "r", encoding="utf-8") as f:
            data[path.stem] = await f.read()
    async with aiofiles.open(data_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=4))


if __name__ == "__main__":
    asyncio.run(main())
