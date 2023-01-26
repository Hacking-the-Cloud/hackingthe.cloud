FROM squidfunk/mkdocs-material
RUN pip install mkdocs-awesome-pages-plugin
RUN pip install mkdocs-redirects
RUN pip install mkdocs-rss-plugin
RUN pip install mkdocs-glightbox
