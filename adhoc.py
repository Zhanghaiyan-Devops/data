import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
import ansible.constants as C


def adhoc(sources=None, hosts=None, module=None, args=None):
    # since API is constructed for CLI it expects certain options to always be set, named tuple 'fakes' the args parsing options object
    # namedtuple是命名元组(为元组的下标取名就是命名元组)
    # 配置ansible执行过程中所用到的参数
    # connection是连接类型, 有三种选项:
    # local 表示本地执行, ssh  表示用ssh连接后执行, smart  表示自动选择
    Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
    options = Options(connection='local', module_path=['/to/mymodules'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)

    # initialize needed objects
    # ansible会用到各种各样的格式, 如json, yaml, ini等
    # 这些文件的内容需要转成python的数据类型, Dateloader会自动进行转换
    loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
    # 各种密码
    passwords = dict(vault_pass='secret')

    # Instantiate our ResultCallback for handling results as they come in. Ansible expects this to be one of its main display outlets

    # create inventory, use path to host config file as source or hosts in a comma separated string
    # inventory是主机清单, 可以采用两种形式:
    # 1. 用逗号将所有被管理的主机列出
    # 2. 用文件路径列表指定主机清单文件的位置
    # inventory = InventoryManager(loader=loader, sources='localhost,')
    inventory = InventoryManager(loader=loader, sources=sources)

    # variable manager takes care of merging all the different sources to give you a unifed view of variables available in each context
    # 变量管理器
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # create datastructure that represents our play, including tasks, this is basically what our YAML loader does internally.

    play_source =  dict(
            name = "Ansible Play",
            hosts = hosts,
            gather_facts = 'no',
            tasks = [
                dict(action=dict(module=module, args=args), register='shell_out'),
                dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
             ]
        )

    # Create play object, playbook objects use .load instead of init or new methods,
    # this will also automatically create the task objects from the info provided in play_source
    # 创建play的实例
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # Run it - instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host list and tasks
    # 创建任务列表管理器
    tqm = None
    try:
        tqm = TaskQueueManager(
                  inventory=inventory,
                  variable_manager=variable_manager,
                  loader=loader,
                  options=options,
                  passwords=passwords,
              )
        result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
    finally:
        # we always need to cleanup child procs and the structres we use to communicate with them
        if tqm is not None:
            tqm.cleanup()

        # Remove ansible tmpdir
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

if __name__ == '__main__':
    adhoc(['myansible/hosts'], 'dbservers', 'shell', 'id root')