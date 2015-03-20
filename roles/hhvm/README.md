# HHVM

Using HHVM and WordPress together can lead to memory leaks.

See https://github.com/facebook/hhvm/issues/4398 and https://github.com/facebook/hhvm/issues/4250 for more details.

The best solution right now is to restart the HHVM service every so often. By default this role will restart the service every day at 2am (local time of server).

## Options

This role can be customized with two variables:

* `hhvm_daily_restart`: whether or not to restart HHVM daily via a cron job (default: `True`)
* `hhvm_daily_restart_hour`: the hour the cron job runs at (default: `2`)
