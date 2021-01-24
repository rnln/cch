# Everyday Commit

**Everyday Commit** is a Python package that generates a random number of commits following the gamma distribution:
<figure style="margin-left: 0">
	<img alt="PDF plot" title="PDF plot" src="./plot.png"><br>
	<figcaption style="font-size: smaller">Visualisation of the gamma distribution's <abbr title="Probability density function">PDF</abbr> with the shape parameter α = 0.3.</figcaption>
</figure>

Distribution type and parametrization based on my humble GitHub activity stats
research.

I did it for the lulz. I know that it's dumb, and that people don't like old
memes. Just don't bug me and yourself.

## Setup

Create a fork and run the setup script:
```sh
git clone git@github.com:rnln/everyday_commit.git
cd everyday_commit
python3 setup.py
```

Setup module creates a virtual environment in `/path/to/everyday_commit/venv/` and a cron
job to run `everyday_commit.py` daily. Job sample:
```
* * 0 0 0 /home/user/everyday_commit/venv/bin/python /home/user/everyday_commit/everyday_commit.py # Everyday Commit
```

## License

Copyright © 2020 Roman Ilin ([contacts][contacts]).

This work is free. You can redistribute and modify it under the terms of the
Do What The Fuck You Want To Public License, Version 2, as published by Sam
Hocevar. See the [COPYING file](./COPYING) for more details.

[![WTFPL 2.0][wtfpl-badge]][wtfpl-website]

[wtfpl-website]: http://wtfpl.net
[wtfpl-badge]: http://wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-2.png
[contacts]: https://rilin.me/contacts
