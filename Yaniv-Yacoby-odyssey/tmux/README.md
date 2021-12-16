### TMUX (Terminal Multiplexer) 

`tmux` is useful for several reasons:
1. If you lose connection / close your terminal when logged into a remote server, it will keep alive any interactive shells you have.
2. It allows you to split your screen into parts (have multiple terminals on Odyssey) without having to log in multiple times.

To use `tmux`, you do have to:
1. make sure you alway log into the same login node, since your `tmux` session will be stored there (e.g. `ssh USERNAME@boslogin01.rc.fas.harvard.edu`).
2. Copy the `.tmux.conf` script into your home directory on Odyssey. While this script is not necessary, it is makes `tmux` **significantly** more convenient to use.

Once on Odyssey, type `tmux` to start a new session. Now if you close your terminal / lose connection, after logging back into Odyssey (into the same login node), type `tmux attach`, and your session will re-appear just as you left it. Sometimes the nodes are restarted for maintenance, and in these cases you may lose the session. 

In addition to keeping your session alive, `tmux` also has a number of other handy features:
* `Control-b \` will open up a vertical split.
* `Control-b -` will open up a horizontal split.
* `Control-b o` will switch between the splits
* `Control-b c` will create a new pane (pane number listed in the bottom right).
* `Control-b n` and `Control-b p` will go between the different panes (forwards and backwards, respectively)
* `Control-b [` will go into scroll mode inside a split:
  - Use the arrow keys to scroll.
  - Use `Control-r` to search up (keep hitting `Control-r` for more results)
  - Use `Control-s` to seeearch down 

There are more things you can do with `tmux`, but hopefully this is enough to get you started. 


