# Backbone

Backbone is a dirt-simple server-side app container
Backbone simply updates and runs a git repository
To use backbone, simple issue `./backbone [git-rep-url]`
The only requirement is that the repository have a `install.sh` and `run.sh` for installing and running respectively.
Backbone will take it from there.

As of current writing, neither the app nor its supporting scripts should require superuser priveleges (And, generally, you shouldn't need superuser priveleges to install apps anyway..).
