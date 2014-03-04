这个脚本帮助你快速把多个数据库导出并备份到七牛
> pip install qiniu

将config.example.py改名为config.py，填入你的七牛、MySQL数据库配置，并将你要备份的数据库名依次写入DB_NAME

例：
> DB_NAME = ['database1', 'database2', 'database3']

最后运行
> python main.py

也可以写成cron来实现每天自动备份
> 0 0 * * * python /yourpath/main.py

**注意，此脚本每次执行都会覆盖之前的备份文件，如果想保留每次的备份文件请自行修改代码**