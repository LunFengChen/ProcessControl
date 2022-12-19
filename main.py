from ProcessUtils import ProcessControl


if __name__ == '__main__':
    processControl = ProcessControl()
    # 1. 创建进程
    processControl.create_process("nginx")
    processControl.create_process("sshd")
    processControl.create_process("mysql")
    processControl.create_process("redis")
    processControl.run_process(pname='mysql')
    processControl.create_process("mariadb")
    processControl.create_process("mongodb")
    # processControl.current_info()

    # 2. 删除进程
    # processControl.delete_process(pname="nginx")
    # # processControl.delete_process(pid=1505)
    # processControl.current_info()
    #
    # # 3. 阻塞进程
    # processControl.block_process(pname="mysql")
    # processControl.block_process(pname="redis")
    # processControl.current_info()
    #
    # # 4. 唤醒进程
    # processControl.wake_process(pname="mysql")
    # processControl.current_info()
    # 5. 等待操作
    processControl.run()
