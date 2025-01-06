# NUS Hack&Roll25 data engineering workshop

## git clone this repo: https://github.com/yijiachen525/Hack-Roll25Workshop
```bash
git clone https://github.com/yijiachen525/HacknRoll2025Workshop.git
```

## Pre-requisites

### 1. Download necessary applications
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed. **If you're on Windows, skip to the Troubleshooting section at the bottom of this page for more detailed instructions**
- [Python](https://www.python.org/downloads/) installed, recommended version 3.10 or 3.11
- Python development environment: recommended [PyCharm Community](https://www.jetbrains.com/products/compare/?product=pycharm&product=pycharm-ce); or [VSCode](https://code.visualstudio.com/)

### 2. Setup development environment

#### Configure the environment via virtualenv from Pycharm
After cloning this repository, open it as a project in PyCharm. If PyCharm prompts you to create a new virtualenv using the `requirements.txt`, do that.

If not, you might need to setup the Python interpreter in PyCharm by clicking "Add Interpreter" > "Add Local Interpreter" and "Virtualenv > New". Select the Python executable which has been installed if it not already selected. Then, in a terminal, run: `pip install -r requirements.txt` to install the Python dependencies manually.

#### Alternatively, if you have Conda installed 
_or install it here: https://www.anaconda.com/download. You will need to provide your email address_

Navigate to the project root directory, you can create an environment via:

```bash
conda env create -f environment.yaml
```

The above will create a new environment called `mw-data-workshop`. Activate the environment using the following command:

```bash
conda activate mw-data-workshop
```

In Pycharm, follow [this guide](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html#view_list) to select the interpreter `mw-data-workshop` you just installed.

If you are using VScode, you can open up the command palette > search "Python: Select interpreter" > then select the `mw-data-workshop` you just installed.

### 3. Spin up docker images

Mark the `src` directory as sources root (right click > Mark directory as > Sources root).

Spin up the dependencies by running the following in the terminal at the root of the project:

```bash
docker compose up -d
```

If this is your first time running the command, it may take a few minutes to pull the images.

This will spin up:
- A kafka broker at http://localhost:9093
- Kafka UI: http://localhost:8083
- SQLite UI: http://localhost:8082
- Mystery Picture API: http://localhost:9999

You can check the images running with this command:

```bash
docker compose ps
```

After the workshop, you can use this to tear down your docker instance:
```commandline
docker-compose down
```

---
## End of setup!! See you at the workshop :)
---

# Troubleshooting

#### Installing Docker Desktop for Windows
Enable Hyper-V by going to the "Turn Windows features on or off" panel and ticking Hyper-V. You will need to restart your computer after this.

Download Docker for Desktop on [this page](https://www.docker.com/products/docker-desktop/). If you get the error `We've detected that you have an incompatible version of Windows. Docker Desktop requires Windows 10 Pro/Enterprise/Home version 19044 or above.` when running the installer, install an older version of Docker Desktop for Windows than the latest one. You might have more luck installing version 4.20.0 from [this page](https://docs.docker.com/desktop/release-notes/#4200).

Run the installer and **untick "Use WSL instead of Hyper-V"** then proceed with the installation.

#### I get `the docker daemon is not running` when running `docker compose up -d`

Is Docker Desktop up and running?

#### I get `ModuleNotFoundError: No module named 'common'`
Did you mark `src` as sources root in PyCharm?

#### I get "cannot connect to kafka" when running the scrape
Was `docker compose up -d` successful? Check that the container is running with `docker ps` on the terminal, or in the Docker Desktop app. 

#### I get `ModuleNotFoundError: No module named 'scrapy'`
Did you install the python packages with `pip install -r requirements.txt`?
