## Introduction

A Vesuvius Challenge tool to view a small 3D region of high resolution volume with flexibility.

## Setup

Virtual environment

```
python -m venv env
source env/bin/activate
```

Install dependency

```
pip install -r requirements.txt
```

## Select the location

Let's say you have a labeled image of a segment, but some local areas have some interesting behaviors that make you want to take a closer look. Take the following spot in segment `20230702185753` as an example, the uv coordinate of that spot is around `(0.521, 0.492)` (lower left and upper right corner are (0, 0) and (1, 1) respectively).

<!-- need an image here -->

## Run App

```
python app.py
```
