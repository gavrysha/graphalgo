# graphbuilder

Simple pygame application for graphs building.

## Installation

Clone this repo. Also, it's possible to use graphbuilder as module. To do this, you should place [graphbuilder](https://github.com/shevelidze/graphbuilder/tree/main/graphbuilder) folder to place from you want import it.

## Usage
For basic usage just install requirements:

```
pip install -r requirements.txt
```
And run:

```
python __main__.py
```

From parent directory:

```
python graphbuilder
```

### Controls

`V` - create vertex.

`E` - create edge. Before edge creating, you should activate vertex. Then click to second vertex.

`Click to vertex` - activate vertex.

`Esc` - cancel vertex and edge creating, deactivate vertex.

`Delete` - delete active vertex.

To delete edge create it one more time.

`O` - open file.

`S` - save to file.