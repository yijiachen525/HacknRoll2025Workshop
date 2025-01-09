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

#### If you have Conda installed
Alternatively, navigate to the project root directory, you can create an environment via:

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


---
### End of setup!! See you at the workshop :)

---

## Introduction

In this repository, we will be spinning up a few different components for a simple data application. There will be:
1. 2 webscraping pipelines (code in `./src/pipeline/`). We are using the [Scrapy](https://scrapy.org/) python framework for the webscrapes.  
Each pipeline is made up of a **scrape** file, whose only goal is to send the
*raw* data to a Kafka topic, and a **consume** file, which parses the messages in Kafka
and writes the structured data to SQLite.
2. Some visualisations/dashboards made using Plotly Dash (code in `./src/hockey_app.py` & `./src/mystery_picture_app.py`)

## Instructions

### Hockey scrape and dashboard

This is a scrape of the Hockey teams data located at: https://www.scrapethissite.com/pages/forms/  
This scrape is already written for you and should work out of the box.  
Make yourself familiar with the code:
- the `scrape/hockey_spider.py` file starts a bunch of scrapy Requests to scrape all pages of the link above. It inserts a `HockeyResultsItem` into the Kafka topic - which is the raw, unprocessed HTML of the table present in the page.
The reason why we store this raw unprocessed data in Kafka is because it enables us to decouple the raw data from the processing logic. Also, it allows us to easily replay history if the website ever changes and the parsing logic breaks.
- the `consume/hockey_kafka_to_sqlite.py` file actually parses the table into structured data, and inserts it into a SQLite table.

Run the `src/run.py` file with the IDE. You should see some Scrapy logs in the Run window.  
Navigate to the Kafka UI at http://localhost:8083 and explore the messages in the `hockey-teams-results` topic. Notice how messages contain the raw HTML.  
Then, navigate to the SQLite UI at http://localhost:8082. Open up the `HockeyTeamResults` table and browse for the inserted content.  
If you're familiar with SQL, you can try to run queries to explore the data.

Then, start the plotly dash app by running the file `./src/hockey_app.py` and navigating to http://localhost:8080.

1) Which team had the most losses in 2011?
2) Which team had the most wins in a given year?
3) Display a table showing the stats of the team with the highest win percentage for each year. If some teams have the same value, pick the first alphabetically.

### Mystery picture API

The goal is to scrape an API located at http://localhost:9999/.  
There are 500 pages we want to scrape: from http://localhost:9999/rows/0 up to http://localhost:9999/rows/499.  
The `GET /rows/{row_id}` endpoint returns a JSON value that has the following structure:
```json
{"row_id": <row id from the input>,
"columns": <array of integers from 0 to 255>}
```
Each page actually represents a single "row" in a 500*500 picture. The `columns` array represents the grayscale values
of each pixel in the given row. 
For example, let's look at: http://localhost:9999/rows/3. This returns:
```json
{
  "row_id": 3,
  "columns": [
    242, 241, 240, 238, 238, 236, 235, 234, ... (500 values)
  ]
}
```
This means that the 3rd (well, 4th since we count from 0) row of the picture has the pixel grayscale values `[242, 241, 240, ...]`.  

1) Edit the `./src/pipeline/scrape/mystery_picture_spider.py` file to write the scrape of these 500 API pages, and send the **raw** result from the API to Kafka, and run it. To run it, keep using the `./src/run.py` entrypoint, just comment the block from the previous task. 
2) After the messages are in Kafka (which you can see via the Kafka UI), edit the `./src/pipeline/consume/mystery_picture_to_sqlite.py` file to parse the raw messages and insert 
   into the MysteryPicture table. That table has the columns `(X, Y, Value)` where X is the row number, Y is the column number, and Value is the grayscale value from 0-255.  
   This means that each raw message from Kafka should insert 500 rows in the table, and that the table should have exactly 500*500 = 250000 entries once the scrape has run.

   In `run.py`, you can comment the lines before `print("Start inserting")` to only run the `consume` part of the pipeline. If you had already ran the pipeline, you will have to reset the consumer offsets so that the
   consumer replays the historical raw data that was already scraped with Scrapy. If you don't, it will consider that there are no new messages to process and do nothing, since it will be reading the end of the Kafka topic.
   To reset the consumer offsets, go to the Kafka UI and click on Consumers > sqlite > `...` on the top right > Reset offset > chose the topic, reset type=EARLIEST, partitions=all.
3) Once the `consume` file has run, on the SQLite UI, run a few sanity checks on the `MysteryPicture` table:
```sql
-- The picture contains 500*500 = 250,000 pixels:
SELECT COUNT(*)
FROM "MysteryPicture"
-- This should return 250000
```
```sql
-- The mystery picture's X and Y coordinates all span from 0 to 499:
SELECT MIN(X), MAX(X), MIN(Y), MAX(Y)
FROM "MysteryPicture"
-- This should return (0, 499, 0, 499)
```
```sql
-- There are no duplicate rows with the same (X, Y):
SELECT X, Y
FROM "MysteryPicture"
GROUP BY X, Y
HAVING COUNT(*) >= 2
-- This should be empty
```
```sql
-- The grayscale values are always between 0 and 255:
SELECT MIN(Value), MAX(Value)
FROM "MysteryPicture"
-- This should return (0, 255)
```
4) Edit and run the `./src/mystery_picture_app.py` to format the results from the SQL table accordingly in order to display them on a [plotly Heatmap](https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.Heatmap.html).
5) Who's in the picture?

## Extra questions
If you have some time left:
1) In the HockeyTeamResults table, we can expect an obvious relationship between the
`GoalsFor`, `GoalsAgainst`, `GoalsDifference` columns. Can you run a SQL query to check that this is indeed the case?
2) Similarly, we can expect a relationship between `Wins`, `Losses` and `WinPct`. Can you run a SQL query to verify that this is the case? What could explain the discrepancies?
3) Following the question above, can you write a SQL query to derive an additional piece of information about each team's yearly score?

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
