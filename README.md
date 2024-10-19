# strange
strange is a static site generator

## Install

```
git clone https://github.com/knutel/strange.git
cd strange
pip install .
```

## Usage

Run `strange -h` to get basic help:

```
$ strange --help
Usage: strange [OPTIONS]

Options:
  -s, --serve
  -p, --port INTEGER
  --publish
  --help              Show this message and exit.
  ```

Running `strange` once without parameters will create the necessary folders:

* `content`: This is where you put your blog posts, written in Markdown.
* `theme`: Put your stylesheets here.
* `templates`: Put your Jinja2 templates here.
* `output`: This is where the generated site is put when serving locally.
* `publish`: This is where the published site is put. Drafts are not generated here.

See the `example` folder for a full site.

Running `strange -s -p 8000` will continuously re-generate your site into the `output` folder when any input files change. Go to `http://localhost:8000` to view site.

Running `strange --publish` will generate your site into the `publish` folder, which can then be copied to your hosting platform of choice.

## Final words

strange is extremely basic and a work in progress that is only meant to cover my own needs. Others may at best learn something from it.