# Readeck

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<a rel="me" href="https://mastodon.online/@readeck"><img src="https://img.shields.io/badge/%40readeck-blue?logo=mastodon&logoColor=%23fff&color=%236364ff" alt="Follow on Mastodon" /></a>

Readeck is a simple web application that lets you save the
precious readable content of web pages you like and want to keep
forever. \
See it as a bookmark manager and a read later tool.

![Readeck Bookmark List](https://codeberg.org/readeck/readeck/media/branch/main/screenshots/bookmark-list.webp)

## Contents

- [Features](#features)
- [Installation](#how-to-test-or-install)
- [FAQ](#faq)
- [Under the hood](#under-the-hood)
- [License](#license)

## Features

### 🔖 Bookmarks

Like a page you're reading? Paste the link in Readeck and you're done!

### 📸 Articles, pictures and videos

Readeck saves the readable content of web pages for you to read later. It also detects when a page is an image or a video and adapts its process accordingly.

### ⭐ Labels, favorites, archives

Move bookmarks to archives or favorites and add as many labels as you want.

### 🖍️ Highlights

Highlight the important content of your bookmarks to easily find it later.

### 🗃️ Collections

If you need a dedicated section with all your bookmarks from the past 2 weeks labeled with "cat", Readeck lets you save this search query into a collection so you can access it later.

### 🧩 Browser Extension

Want to keep something for later while browsing? No need to copy and paste a link. Install the browser extension and save bookmarks in one click!

- [For Mozilla Firefox](https://addons.mozilla.org/en-US/firefox/addon/readeck/)
- [For Google Chrome](https://chromewebstore.google.com/detail/readeck/jnmcpmfimecibicbojhopfkcbmkafhee)
- [More Information and Source Code](https://codeberg.org/readeck/browser-extension)

### 📖 E-Book export

What's best than reading your collected articles on your e-reader? You can export any article to an e-book file (EPUB). You can even export a collection to a single book!

On top of that, you can directly access Readeck's catalog and collections from your e-reader if it supports OPDS.

### 🔎 Full text search

Whether you need to find a vague piece of text from an article, or all the articles with a specific label or from a specific website, we've got you covered!

### 🚀 Fast!

Readeck is a modern take on so called boring, but proven, technology pieces. It guaranties very quick response times and a smooth user experience.

### 🔒 Built for your privacy and long term archival

Will this article you like be online next year? In 10 year? Maybe not; maybe it's all gone, text and images. For this reason, and for your privacy, text and images are all stored in your Readeck instance the moment you save a link.

With the exception of videos, not a single request is made from your browser to an external website.

## How to test or install

Done reading this promotional content? Good! Want to try Readeck on your laptop or a server? Even better!

### Container

To install or test Readeck with Docker or Podman, simply run the image:

```shell
docker run --rm -ti -p 8000:8000 -v readeck-data:/readeck codeberg.org/readeck/readeck:latest
```

You'll find all the container images there: \
[https://codeberg.org/readeck/-/packages/container/readeck/latest](https://codeberg.org/readeck/-/packages/container/readeck/latest)

### Binary file installation

Readeck is distributed as a single binary file. Using it is almost as easy as a container.

- Create a new directory
  ```shell
  mkdir -p readeck-install
  cd readeck-install
  ```
- Download the file matching your system from the [last release](https://codeberg.org/readeck/readeck/releases)

- Make this file executable
- Launch Readeck with the `serve` argument, for example:
  ```shell
  ./readeck-0.9.1-linux-amd64 serve
  ```

### First time launch

Once Readeck has started, it is accessible on: \
**[http://localhost:8000/](http://localhost:8000/)**

### Installation for production

More documentation is coming but if you already know how deploy containers or new services on a server (ie. with systemd), it should be quite straightforward.

## FAQ

### I can't save a link or it's incomplete

Readeck usually can save the vast majority of news or blog articles but it sometimes fails to do so. The most common reasons are:

- The page is behind a paywall,
- The page needs JavaScript to render its content,
- Your server is blocked,
- The content extractor fails.

The most common solution to these problems is to install and use the [Browser Extension](https://readeck.org/en/download/). The extension sends the page's full content to Readeck, so anything can be saved. Moreover, it lets you select the exact content you want to save.

If a page really doesn't work at all, please [open an issue](https://codeberg.org/readeck/readeck/issues/new?template=.gitea%2fissue_template%2fextraction_error.yaml).

### Can I share a saved bookmark with a public link?

Yes you can, for a limited time. On each article you can generate a link that'll be valid for 24 hours. You can generate a new link as many times as you want but it will always expire. You can also export or print an article to a PDF file.

### Is there a system to store my (paywall) website credentials?

There isn't, for several reasons:

- To safely store credentials without giving access to anyone but the user is next to impossible,
- Such a system relies on web scrapping and is prone to break too often,
- It might go against websites TOS.

Again, the [Browser Extension](https://readeck.org/en/download/) will let you save any content you can access from your web browser.

### Is there a smartphone application?

Not yet but it might come at some point. Meanwhile, you can use Readeck on any mobile browser and even install as a mobile application.

If you'd like to save links using the "share" feature of your phone, you can use the following:

- iOS: [iOS shortcut](https://www.icloud.com/shortcuts/226bafabbbfd47708f3bea69dbf24ef0),
- Android: Use [HTTP Shortcuts](https://http-shortcuts.rmy.ch/) and create a new shortcut as described on [this issue](https://codeberg.org/readeck/readeck/issues/112#issuecomment-2082710).

### Is there a roadmap?

There are [milestones](https://codeberg.org/readeck/readeck/milestones), where you can see what's planned for the future releases.

For longer term goals, there are [projects](https://codeberg.org/readeck/readeck/projects)

### Is there a Readeck twitter account?

There isn't but you can follow [@readeck@mastodon.online](https://mastodon.online/@readeck) on Mastodon.

### Is the a Readeck Discord server?

There isn't but you can join [#readeck:matrix.org](https://matrix.to/#/#readeck:matrix.org) on Matrix.

### How can I report a security issue?

If you think you found a security issue in Readeck, **please DO NOT create an issue**; they're public and it could potentially put all users at risk.

Send an email to security@readeck.com and you'll receive a follow-up as soon as possible.

## Under the hood

Readeck was born out of frustration (and COVID lock-downs) from the tools that don't save everything related to the saved content, primarily images.
This key principle guided every step of Readeck development.

### The ZIP file

Every bookmark is stored in a single, immutable, ZIP file. Parts of this file (HTML content, images, etc.) are directly served by the application or converted to a web page or an e-book when needed.

### A simple database

Readeck has a very simple database schema with a few tables (and a bit of clever JSON fields here and there). The recommended database engine is SQLite for most installations.

### A simple stack

Unlike many modern web applications, Readeck is not a single page application built on top of an API with impossible to install dependencies and a mess of background processes.

Readeck is written in [Go](https://go.dev/) and all its content is rendered server side with some interactivity brought by [Stimulus](https://stimulus.hotwired.dev/) and [Turbo](https://turbo.hotwired.dev/).

This has proven to be a great combination when performance really matters.

## License

Readeck is distributed under the terms of the [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html). Here's a short summary of the license conditions:

- Permissions
  - **Commercial use** \
     The licensed material and derivatives may be used for commercial purposes.
  - **Distribution** \
     The licensed material may be distributed.
  - **Modification** \
     The licensed material may be modified.
  - **Patent use** \
     This license provides an express grant of patent rights from contributors.
  - **Private use** \
     The licensed material may be used and modified in private.
- Conditions
  - **Disclose source** \
    Source code must be made available when the licensed material is distributed.
  - **License and copyright notice** \
    A copy of the license and copyright notice must be included with the licensed material.
  - **Network use is distribution** \
    Users who interact with the licensed material via network are given the right to receive a copy of the source code.
  - **Same license** \
    Modifications must be released under the same license when distributing the licensed material. In some cases a similar or related license may be used.
  - **State changes** \
    Changes made to the licensed material must be documented.
- Limitations
  - **Liability** \
    This license includes a limitation of liability.
  - **Warranty** \
    This license explicitly states that it does NOT provide any warranty.
