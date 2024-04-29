import docker
import requests
from hstest import StageTest, dynamic_test, CheckResult

ancestor = "hyper-web-app"
url = "http://localhost:8000"
server_response = {
    "first_name": "Hyper",
    "id": "90", "last_name": "Skill"
}


class DockerTest(StageTest):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output = None
        self.client = docker.from_env()

    @dynamic_test()
    def test1(self):
        """Tests image of container, state and exposed port"""
        all_containers = self.client.containers.list(all=True)
        for container in all_containers:
            if container.attrs.get("Config").get("Image") == ancestor:
                if container.attrs.get("State").get("Running"):
                    if "8000" in str(container.attrs.get("Config").get("ExposedPorts").keys()):
                        return CheckResult.correct()
                    else:
                        return CheckResult.wrong("The exposed port should be 8000!")
                else:
                    return CheckResult.wrong("The container should be running!")

        return CheckResult.wrong(f"Couldn't find a container from the '{ancestor}' ancestor!")

    @dynamic_test()
    def test2(self):
        """Tests if the webserver is running as expected"""
        try:
            response = requests.get(url)
        except requests.exceptions.ConnectionError:
            return CheckResult.wrong("Connection error!")
        except requests.exceptions.InvalidURL:
            return CheckResult.wrong("Couldn't connect to the server. Check if hyper-web-app is running as expected!")
        except requests.exceptions.Timeout:
            return CheckResult.wrong("Connection timed out, while trying to connect hyper-web-app!")
        else:
            if response.status_code != 200:
                return CheckResult.wrong("Wrong status code returned from the hyper-web-app!")
            try:
                json_response = response.json()
            except requests.exceptions.JSONDecodeError:
                return CheckResult.wrong("Couldn't convert server response to dictionary!")
            if json_response != server_response:
                return CheckResult.wrong("Wrong content returned from the hyper-web-app!")
        return CheckResult.correct()


if __name__ == '__main__':
    DockerTest().run_tests()
