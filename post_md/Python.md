### 打包程序为 exe

pip install pyinstaller
pyinstaller --onefile --noconsole your_script.py

PyInstaller 将会开始打包你的项目，并在打包完成后生成一个 dist 文件夹，其中包含了打包好的 .exe 文件以及项目的依赖项。