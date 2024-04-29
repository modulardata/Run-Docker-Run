from pathlib import Path

import docker
from hstest import StageTest, dynamic_test, CheckResult
import os
docker_file = "Dockerfile"
stage = Path(__file__).parent.parent

project_images = ["python:3.11-slim"]


def get_dockerfile_content():
    file = f"{stage}/{docker_file}"
    if not os.path.isfile(docker_file):
        return
    with open(file=file, mode="r", encoding="utf-8") as file:
        rows = file.read().lower()
    return rows


class DockerTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None
        self.client = docker.from_env()

    @dynamic_test()
    def test1(self):
        """Tests if image exists in the system"""
        images_text = " ".join([str(image) for image in self.client.images.list()])
        for image in project_images:
            if image not in images_text:
                return CheckResult.wrong(f"'{image}' not found in the system images!")

        return CheckResult.correct()

    @dynamic_test()
    def test2(self):
        """Tests docker file length, and content"""
        content = get_dockerfile_content()

        if content is None:
            return CheckResult.wrong("Dockerfile not found!")

        content_list = [line for line in content.split("\n") if line]

        if len(content_list) < 6:
            return CheckResult.wrong("The Dockerfile should contain at least 6 lines!")

        for instruction in ["FROM ", "EXPOSE ", "WORKDIR ", "ADD ", "RUN ", "ENTRYPOINT "]:
            if instruction.lower() not in "".join(content_list).lower():
                return CheckResult.wrong(f"Dockerfile should have `{instruction}` instruction!")

        return CheckResult.correct()


if __name__ == '__main__':
    DockerTest().run_tests()
