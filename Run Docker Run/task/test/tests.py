import docker
from hstest import StageTest, dynamic_test, CheckResult

project_images = ["python:3.11-slim"]


class DockerTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None
        self.client = docker.from_env()

    @dynamic_test()
    def test1(self):
        """Tests if the base image exists in the system"""
        images_text = " ".join([str(image) for image in self.client.images.list()])
        for image in project_images:
            if image not in images_text:
                return CheckResult.wrong(f"'{image}' not found in the system images!")

        return CheckResult.correct()


if __name__ == '__main__':
    DockerTest().run_tests()
