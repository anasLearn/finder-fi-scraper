# Finder.fi scraper

This a simple scraper to collect data about companies from [finder.fi](https://www.finder.fi/).

## Prerequisites
* Python 3.9

In a terminal, install dependencies with:
```
python -m venv venv

# In linux
source venv/bin/activate

# In Windows
.\venv\Scripts\activate

pip install -r requirements.txt
```

## Usage
* In the file [`input.txt`](./input.txt), write `finder.fi` urls of the page of the companies you wish to scrap. One link per line.
* In a terminal:
* ```
  python main.py
  ```
* A file named `output.csv` will be generated. You can open it in excel.
