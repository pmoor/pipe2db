pipe2db
=======

External Postfix delivery script that feeds incoming email into Google's Cloud Storage Service (GCS).

To play well with SELinux/postfix change the context of the script and .boto configuration with

  chcon -u system_u -r object_r -t postfix_pipe_exec_t ...
