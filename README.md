Sudoku Solver API & Site
============

A sudoku puzzle solver website and API. This is based off my [sudoku-solver](https://github.com/adamsp/sudoku-solver) script, with a few tweaks. It's running on Google App Engine because it's free and easy to get up and running.

## Usage

Usage is very simple.

To solve a Sudoku puzzle, just send a GET to `/solve/{puzzle}`, where `{puzzle}` is the 81 digits (for the 9x9 grid) that make up the puzzle, using 0s as placeholders. This will return to you an 81 character string of digits representing the solved puzzle, or HTTP code 400 (and an error message) for invalid input. If it is impossible to solve your input, the result will be solved as far as possible, with 0s in the remaining cells.

For example:

```
http://localhost:8080/solve/097080600000000700008012530001540298900307006642098300039670800004000000006030940
```

## License

    Copyright 2014 Adam Speakman

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
