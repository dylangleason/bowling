# bowling

Program for calculating 10-pin bowling scores.

Score each frame at the interactive prompt, for up to 10 frames. A valid frame is defined as one of the following inputs:

    X     - Strike ("x" is also accepted as input)
    n,/   - Spare
    n,m   - Open Frame, where n and m are numbers
    X,n,m - Strike plus two bonus rolls (Final Frame only)
    n,/,m - Spare plus two bonus rolls (Final Frame only

## Running the Program

The program can be run via Python 3, or via Docker after building an image with the supplied `Dockerfile`.

### Python

To run the program via Python 3:

```
python3 main.py
```

### Docker

Docker commands have been wrapped via `make`. To build the Docker image and execute the program via a one-shot container, run the following:

```
make
```

The program can be run again without rebuilding the image:

```
make run
```

## Running the Tests

Unit tests have also been provided and can be run via `make`:

```
make test
```
