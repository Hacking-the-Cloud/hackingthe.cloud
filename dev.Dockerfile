# This Dockerfile is intended for local testing and requires a subscription to 
# Material for MkDocs to work. If you'd like to contribute to Hacking the Cloud
# and need to setup a local env, you can use the normal "Dockerfile" in this repo.
# Thank you!
FROM ubuntu

ARG GH_TOKEN

WORKDIR /docs

RUN apt update -y
RUN apt install -y libcairo2-dev libfreetype6-dev libffi-dev libjpeg-dev libpng-dev libz-dev python3-pip python3 git
RUN pip install tzdata
RUN pip install pillow cairosvg
RUN pip install mkdocs-minify-plugin
RUN pip install mkdocs-awesome-pages-plugin
RUN pip install mkdocs-redirects
RUN pip install mkdocs-git-revision-date-localized-plugin
RUN pip install mkdocs-git-committers-plugin-2
RUN pip install mkdocs-rss-plugin
RUN pip install --use-pep517 mkdocs-glightbox
RUN pip install git+https://${GH_TOKEN}@github.com/squidfunk/mkdocs-material-insiders.git

RUN git config --global --add safe.directory /docs &&\
    git config --global --add safe.directory /site

EXPOSE 8000

ENTRYPOINT ["mkdocs"]
CMD ["serve", "--dev-addr=0.0.0.0:8000"]