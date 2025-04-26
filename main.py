# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



import functools
import time
import uuid

from collections import defaultdict, deque


class Node:
    def __init__(self, data):
        self.data = data.strip().lower()
        self.parent = None
        self.child = []
        self.task_status = ['Not Started']
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return f"Node({self.data})"




def time_calculator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"⏳ Start time: {start}")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"✅ End time: {end}, Duration: {end - start:.4f}s\n")
        return result

    return wrapper


class Goal:
    def __init__(self, goal):
        self.root = Node(goal)

        self.tree_dict = {self.root.data: [self.root]}
        self.name_index = defaultdict(list)
        self.name_index[self.root.data].append(self.root)
        self.by_uudi = {self.root.id: self.root}

    def ask_for_correct_parent(self, nodes_with_same_name):
        x = 0
        for i in nodes_with_same_name:
            if i.parent:
                print(i.parent.data, "    ", x)
            else:
                print("root node", x)
            x = x + 1
        return nodes_with_same_name[int(input("tell which parent: "))]

    @time_calculator
    def add_subtask(self, data, parent):
        data = data.strip().lower()
        parent = parent.strip().lower()

        # if data in self.tree_dict:
        #     print(f"⚠️ Subtask '{data}' already exists. Skipping.")
        #     return
        subtask_node = Node(data)
        if parent in self.name_index:
            correct_parent_node = self.ask_for_correct_parent(self.name_index[parent])
            correct_parent_node.child.append(subtask_node)
            subtask_node.parent = correct_parent_node
            self.name_index[subtask_node.data].append(subtask_node)
            self.by_uudi[subtask_node.id] = subtask_node
            return

        parent_node = self.find_parent(parent, self.root)
        if not parent_node:
            print(f"❌ Parent '{parent}' not found.")
            return

        parent_node.child.append(subtask_node)
        subtask_node.parent = parent_node
        self.name_index[subtask_node.data].append(subtask_node)
        self.by_uudi[subtask_node.id] = subtask_node
        print(f"✅ Added '{data}' under '{parent}'")
        print(f"📘 Tree Dict: {self.tree_dict}")

    def find_parent(self, parent, root_node):
        if root_node.data == parent:
            return root_node

        for child in root_node.child:
            found = self.find_parent(parent, child)
            if found:
                return found
        return None

    def print_goals_subtask(self, root, slash_count):
        indent = "    " * slash_count
        print(indent + "- " + root.data)

        for child in root.child:
            self.print_goals_subtask(child, slash_count + 1)

    def update_task_status(self, status, task_node_name):
        self.tree_dict[task_node_name].task_status = status
        return

    def bfs_print(self,root):
        queue = deque([root])
        result = []
        while queue:
            current = queue.popleft()
            result.append(current.data)
            for child in current.child:
                queue.append(child)

        print(result)


# def run_dummy_data():
#     main_goal = Goal("Build a personal website")
#
#     tasks = [
#         ("Design UI", "Build a personal website"),
#         ("Write content", "Build a personal website"),
#         ("Design UI", "Write content"),  # duplicate name, different parent
#         ("Choose font", "Design UI"),    # will ask which "Design UI"
#         ("Deploy site", "Build a personal website"),
#     ]
#
#     for subtask, parent in tasks:
#         main_goal.add_subtask(subtask, parent)
#
#     print("\n📌 Final Goal Tree:")
#     main_goal.print_goals_subtask(main_goal.root, 0)
#
#     print("\n🧠 All tasks by UUID:")
#     for uid, node in main_goal.by_uuid.items():
#         print(f"{uid}: {node.data} (status: {node.task_status[0]})")

from unittest.mock import patch


from itertools import cycle

def run_dummy_data_with_input_mock():
    main_goal = Goal("Build a personal website")

    tasks = [
        ("Design UI", "Build a personal website"),
        ("Write content", "Build a personal website"),
        ("Design UI", "Write content"),  # duplicate name, different parent
        ("Choose font", "Design UI"),    # Will trigger ask_for_correct_parent
        ("Deploy site", "Build a personal website"),
    ]

    # Use cycle to repeat input values infinitely
    simulated_inputs = cycle(["0"])

    with patch("builtins.input", side_effect=simulated_inputs):
        for subtask, parent in tasks:
            main_goal.add_subtask(subtask, parent)

    print("\n📌 Final Goal Tree:")
    main_goal.print_goals_subtask(main_goal.root, 0)

    print("\n🧠 All tasks by UUID:")
    for uid, node in main_goal.by_uudi.items():
        print(f"{uid}: {node.data} (status: {node.task_status[0]})")
    print(f"fdfdfdfdfdfddf------------------")
    print(main_goal.bfs_print(main_goal.root))



if __name__ == '__main__':
    run_dummy_data_with_input_mock()
    # goal = input("🎯 Main Goal: ")
    # main_goal = Goal(goal)
    #
    # while True:
    #     subtask = input("\n➕ Subtask: ")
    #     parent = input("🔗 Parent task: ")
    #     main_goal.add_subtask(subtask, parent)
    #
    #     cont = input("➕ Add more? (y/n): ").strip().lower()
    #     if cont != 'y':
    #         print("\n📌 Final Goal Tree:")
    #         main_goal.print_goals_subtask(main_goal.root, 0)
    #         break


# Press the green button in the gutter to run the script.
