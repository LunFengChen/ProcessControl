import datetime

import random


class PCB:
    """
    进程控制块 PCB: process control block
    """

    def __init__(self, pid, pname):
        self.pid = pid
        self.pname = pname
        self.state = "ready"  # "done" "blocked"
        self.instruction = []
        self.wait_time = 0

        self.current_queue = None  # type: Queue

        self.create_time = datetime.datetime.now().time()

    @property
    def queue_index(self):
        return self.current_queue.index(self) + 1

class Queue(list):
    @property
    def size(self):
        return len(self)

    @property
    def _name(self, name):
        self._name = name

    @_name.setter
    def _name(self, value):
        self.name = value


class ProcessControl:
    def __init__(self):
        # 创建, 运行队列、就绪队列、阻塞队列
        self.init_queue()

        self.pid_list = []
        self.pname_list = []

    def init_queue(self):
        self.ready_queue = Queue()
        self.ready_queue._name = "ready_queue"

        self.running_queue = Queue()
        self.running_queue._name = "running_queue"

        self.block_queue = Queue()
        self.block_queue._name = "block_queue"

    def random_pid(self):
        while True:
            pid = random.randint(1000, 65536)
            if pid not in self.pid_list:
                break
        return pid

    def create_process(self, pname=None):
        pid = self.random_pid()
        if pname in self.pname_list:
            raise "输入的pname所对应的进程已经在队列中"

        process_object = PCB(pid, pname)

        self.pid_list.append(pid)
        self.pname_list.append(pname)

        self.ready_queue.append(process_object)
        process_object.current_queue = self.ready_queue
        # process_object.queue_index = process_object.current_queue.size

        print(f"创建进程 -> pname: {pname}, pid: {pid}, status: {process_object.state}")

    def get_process_by_pname(self, pname) -> PCB:
        for item in self.ready_queue:
            if item.pname == pname:
                return item

        for item in self.block_queue:
            if item.pname == pname:
                return item

        for item in self.running_queue:
            if item.pname == pname:
                return item

    def get_process_by_pid(self, pid) -> PCB:
        for item in self.ready_queue:
            if item.pid == pid:
                return item

        for item in self.block_queue:
            if item.pid == pid:
                return item

        for item in self.running_queue:
            if item.pid == pid:
                return item

    def delete_process(self, pid=None, pname=None):
        # 1. 找到对应进程
        if not (pid or pname):
            raise SyntaxError("请输入pname或者pid")

        process = self.get_process_by_pname(pname) or self.get_process_by_pid(pid)

        # 2. 取进程现在所在队列中删除它
        queue = process.current_queue
        queue.remove(process)
        print(f"删除成功 -> pid:{process.pid}, pname= {process.pname}")

    def block_process(self, pid=None, pname=None):
        """
        找到进程, 把他移到阻塞队列, 并把状态改成阻塞
        """
        # 1. 找到对应进程
        if not (pid or pname):
            raise SyntaxError("请输入pname或者pid")

        process = self.get_process_by_pname(pname) or self.get_process_by_pid(pid)

        # 2. 移到阻塞队列
        process.current_queue.remove(process)  # 当前队列删除

        self.block_queue.append(process)  # 加到新队列, 把当前队列置为新队列
        process.current_queue = self.block_queue
        # process.queue_index = process.current_queue.size

        process.state = "blocked"
        print(f"进程调度, 阻塞进程 -> pid:{process.pid}, pname= {process.pname}")

    def run_process(self, pid=None, pname=None):
        # 1. 找到对应进程
        if not (pid or pname):
            raise SyntaxError("请输入pname或者pid")

        process = self.get_process_by_pname(pname) or self.get_process_by_pid(pid)

        # 2. 移到就绪队列
        if process.state == "ready":
            self.ready_queue.remove(process)
            self.running_queue.append(process)
            process.current_queue = self.running_queue
            # process.queue_index = process.current_queue.size

            process.state = "running"
            print(f"进程调度, 执行进程 -> pid:{process.pid}, pname= {process.pname}")
        else:
            print("只有ready的进程才能开始运行")

    def wake_process(self, pid=None, pname=None):
        """
        找到进程, 把他移到就绪队列, 并把状态改成就绪
        """
        # 1. 找到对应进程
        if not (pid or pname):
            raise SyntaxError("请输入pname或者pid")

        process = self.get_process_by_pname(pname) or self.get_process_by_pid(pid)

        # 2. 移到就绪队列
        self.block_queue.remove(process)

        self.ready_queue.append(process)
        process.current_queue = self.ready_queue
        # process.queue_index = process.current_queue.size

        process.state = "ready"
        print(f"进程调度, 唤醒进程 -> pid:{process.pid}, pname= {process.pname}")

    def current_info(self):
        print("".center(80, "-"))
        print("{:^10s}\t{:^10s}\t{:^10s}\t{:^15s}\t{:^15s}\t{:^5s}"
              .format("pid", 'pname', 'state', 'create_time', 'queue_name', 'queue_index'))
        print("".center(80, "-"))
        for item in self.ready_queue + self.block_queue + self.running_queue:
            print("{:^10d}\t{:^10s}\t{:^10s}\t{:^15s}\t{:^15s}\t{:^5d}"
                  .format(item.pid, item.pname, item.state, str(item.create_time), item.current_queue.name,
                          item.queue_index))
        print("".center(80, "-"))
        print("\n")

    def cmd_help(self):
        print("help manual".center(60, "-"))
        print("杀掉进程:\t\tkill -pname mysql 或 kill -pid 3306")
        print("创建进程:\t\tadd -pname mysql")
        print("阻塞进程:\t\tblock -pname mysql 或 block -pid 3306")
        print("唤醒进程:\t\twake -pname mysql 或 wake -pid 3306")
        print("查看进程信息:\t\tps")
        print("查看手册:\t\thelp")
        print("end manual".center(60, "-"))


    def run(self):
        self.cmd_help()
        while True:
            try:
                cmd = input("请输入命令>> ")
                # 删除
                cmd = cmd.strip().split(" ")
                if cmd[0] == "kill":
                    # kill -pid 3306
                    # kill -pname mysql
                    if cmd[1] == "-pid":
                        self.delete_process(pid=int(cmd[2]))
                    elif cmd[1] == "-pname":
                        self.delete_process(pname=cmd[2])
                    else:
                        print("请输入正确指令! 如 kill -pname mysql")
                elif cmd[0] == "add":
                    # add -pname redis
                    if cmd[1] == "-pname":
                        self.create_process(pname=cmd[2])
                    else:
                        print("请输入正确指令! 如 add -pname redis")
                elif cmd[0] == "block":
                    # block -pid 3306
                    # block -pname mysql
                    if cmd[1] == "-pid":
                        self.block_process(pid=int(cmd[2]))
                    elif cmd[1] == "-pname":
                        self.block_process(pname=cmd[2])
                    else:
                        print("请输入正确指令! 如 block -pname mysql")
                elif cmd[0] == "wake":
                    # wake -pid 3306
                    # wake -pname mysql
                    if cmd[1] == "-pid":
                        self.wake_process(pid=int(cmd[2]))
                    elif cmd[1] == "-pname":
                        self.wake_process(pname=cmd[2])
                    else:
                        print("请输入正确指令! 如 wake -pname mysql")
                elif cmd[0] == "run":
                    # wake -pid 3306
                    # wake -pname mysql
                    if cmd[1] == "-pid":
                        self.run_process(pid=int(cmd[2]))
                    elif cmd[1] == "-pname":
                        self.run_process(pname=cmd[2])
                    else:
                        print("请输入正确指令! 如 run -pname mysql")

                elif cmd[0] == "ps":
                    self.current_info()
                elif cmd[0] == "exit":
                    # exit
                    break
                elif cmd[0] == "help":
                    self.cmd_help()
            except:
                print("请检查指令有无错误")

