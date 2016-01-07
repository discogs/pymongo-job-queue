# How to contribute

This project operates with the open contributor model where anyone is welcome to contribute towards development in the form of code review, testing and submitting fixes/patches. If you have a new feature you would like to propose, please create an issue first so we can discuss it together.

## Submitting a Change

To submit a change, please do the following:

* Fork this repo
* Create a new branch on your fork
* Push commits to yr branch
* Submit new Pull Request

Please write clear/coherent messages for your commits:

* For small changes you can do `$ git commit -m "yr brief summary"`
* For larger changes please use the subject, body, footer style. A great resource for writing good commit messages can be found [here](http://chris.beams.io/posts/git-commit/).

### Testing

Anyone submitting code to the project is strongly encouraged to also include tests. We currently have written unit tests in `test.py`. If you have a better idea, please feel free to open an issue and discuss.

## Coding Conventions

We use [EditorConfig](http://editorconfig.org/) to maintain a consistent coding style between different editors. Basically it just ensures that we use `pep8` in our Python files across the project.

If you don't want to use EditorConfig, just make sure to:

* Indent using four spaces for Python
* Indent using two spaces for YAML


