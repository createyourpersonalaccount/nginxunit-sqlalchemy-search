# -*- mode: org -*-

* NGINX-Unit with litestar using SQLAlchemy and PostgreSQL

To run this project, use

#+begin_src sh
  podman-compose build
  podman-compose up -d
#+end_src

then redirect your browser to http://localhost:48572/. There's two endpoints, the index and ~/search~ with a single variable ~/search?s=search_term~.

Brind down the containers and clean up with:

#+begin_src sh
  podman-compose down -t0
#+end_src

** Hacking

You may make changes to the source code under ~webserver/~ in your host OS and have them take immediate effect to your web server without having to rebuild the container images. To do so, use:

#+begin_src sh
  podman exec -t unit ./reload.sh
#+end_src

after you're done editing the Python files of the webserver. Note that this will only pick up changes in the Python files, not other configurations lying in ~unit.d/~.

** Note on psycopg driver

Note that we're using the pure-Python implementation of psycopg instead of the more efficient ~psycopg[c]~ one. See [[https://www.psycopg.org/psycopg3/docs/basic/install.html][these instructions]] for ~psycopg[c]~.

** Note on the NGINX public key

This is only for the paranoid who care about security.

There is a file ~unit.d/nginx-keyring.gpg~ that we have committed in this git repository for convenience, but properly, you should obtain this file via some other means, e.g. see the installation instructions of [[https://unit.nginx.org/installation/][NGINX Unit]]. (Unless you trust me to give you their public key; it may also expire eventually.)
