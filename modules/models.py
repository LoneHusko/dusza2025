import datetime
import os
import shutil
from typing import List


class ProcessConfig:
    name: str
    count: int
    processor: int
    memory: int

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.count = kwargs.get("count")
        self.processor = kwargs.get("processor")
        self.memory = kwargs.get("memory")


class ProcessState:
    name: str
    uid: str
    started_at: datetime.datetime
    active: bool
    processor_usage: int
    memory_usage: int

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.uid = kwargs.get("uid")
        self.started_at = kwargs.get("started_at")
        self.active = kwargs.get("active")
        self.processor_usage = kwargs.get("processor_usage")
        self.memory_usage = kwargs.get("memory_usage")

    def filename(self) -> str:
        return f"{self.name}-{self.uid}"


class Computer:
    name: str
    processor_capacity: int
    memory_capacity: int
    processes: List[ProcessState]

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.processor_capacity = kwargs.get("processor_capacity")
        self.memory_capacity = kwargs.get("memory_capacity")
        self.processes = kwargs.get("processes", [])


class State:
    # .klaszter contents
    cluster_processes: List[ProcessConfig] = []
    computers: List[Computer] = []

    def read_from_path(self, path: str):
        cluster_file = []
        with open(os.path.join(path, ".klaszter"), encoding="utf8") as f:
            cluster_file = f.read().strip().splitlines()

        self.cluster_processes = []
        for i in range(0, len(cluster_file), 4):
            self.cluster_processes.append(ProcessConfig(
                name=cluster_file[i],
                count=int(cluster_file[i + 1]),
                processor=int(cluster_file[i + 2]),
                memory=int(cluster_file[i + 3]),
            ))

        dirlist = [s for s in os.listdir(path) if s != ".klaszter"]
        self.computers = []
        for computer_name in dirlist:
            current_computer = Computer()
            file_list = os.listdir(os.path.join(path, computer_name))
            for file_name in file_list:
                file_content = []
                with open(os.path.join(path, computer_name, file_name), encoding="utf8") as f:
                    file_content = f.read().strip().splitlines()

                if file_name == ".szamitogep_konfig":
                    current_computer.name = computer_name
                    current_computer.processor_capacity = int(file_content[0])
                    current_computer.memory_capacity = int(file_content[1])
                    continue

                current_computer.processes.append(ProcessState(
                    name=file_name.split("-")[0],
                    uid=file_name.split("-")[1],
                    started_at=datetime.datetime.fromisoformat(file_content[0].replace(" ", "T")),
                    active=file_content[1] == "AKTÍV",
                    processor_usage=int(file_content[2]),
                    memory_usage=int(file_content[3]),
                ))

            self.computers.append(current_computer)
        return self

    def write_to_path(self, path: str):
        dirlist = [s for s in os.listdir(path) if s != ".klaszter"]
        for item in dirlist:
            shutil.rmtree(os.path.join(path, item))

        with open(os.path.join(path, ".klaszter"), mode="wt", encoding="utf8") as f:
            process_lines = [str.join("\n", [
                process.name,
                str(process.count),
                str(process.processor),
                str(process.memory),
            ]) for process in self.cluster_processes]
            f.write(
                str.join("\n", process_lines)
            )

        for computer in self.computers:
            os.makedirs(os.path.join(path, computer.name))
            with open(os.path.join(path, computer.name, ".szamitogep_konfig"), mode="wt", encoding="utf8") as f:
                f.write(str.join("\n", [
                    str(computer.processor_capacity),
                    str(computer.memory_capacity),
                ]))
            for process in computer.processes:
                with open(os.path.join(path, computer.name, process.filename()), mode="wt", encoding="utf8") as f:
                    f.write(str.join("\n", [
                        process.started_at.isoformat(" ").split("Z")[0],
                        "AKTÍV" if process else "INAKTÍV",
                        str(process.processor_usage),
                        str(process.memory_usage)
                    ]))
