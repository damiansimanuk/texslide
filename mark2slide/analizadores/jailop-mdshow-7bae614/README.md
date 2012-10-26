# A markdown-based presentations generator

By Jaime Lopez, <jailop@gmail.com>

September, 2012

!

## The necessity

I like plain text.
[Markdown](http://daringfireball.net/projects/markdown/syntax)
is a format definition to write documents in plain text.
So, why not use plain text to generate presentations.

The idea is not original. There are great tools to generate
presentations from a Markdown text file. But I need something
very simple, minimalist in extreme.

!

## The pathway

The process to generate presentations that I prefer:

- Write a plain text in Markdown format
- Separate each slide with "!"
- Generate one webpage for each slide
- Manage formats with a style page in CSS
- Add navigation support (no & yes Javascript)
- Open in a browser, full screen mode
- Enjoy it!


!

## The solution

- A [text plain file](README.md) with your content.

- [mdshow.pl](mdshow.pl) - a Perl script to generate webpages for slides

    `$ ./mdshow.pl README.md`  

- [mdshow.js](mdshow.js) - a Javascript code to add keyboard & mouse driven support

- [style.css](style.css) - a CSS stylesheet

And that's all. Here is it, in less than 100 code lines.

!

## How to move

Mouse:

- `Click` on left side: previous slide
- `Click` on right side: next slide

Keyboard:

- `Right`, `PgDn`, `Space`, `j`: next slide
- `Left`, `PgUp`, `k`: previous slide
- `Home`: First slide
- `End`: Last slide

!

## Warnings

- You need to have installed Perl and Markdown module in your computer to generate files. After that, just distribute your files.
- By the moment, I just had tested Javascript file in Firefox and Chrome.
- If you prefer something with more options or fancy, you are in the wrong place.
