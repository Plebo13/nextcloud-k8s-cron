# nextcloud-k8s-cron
Nextcloud requires a periodic execution of its internal cron script (cron.php) to handle background jobs such as file cleanup, preview generation, and notification dispatch.
In traditional setups, this is handled by the system cron. In Kubernetes, this repository provides an equivalent approach using:

- A simple Python script that triggers the Nextcloud cron endpoint.

- A Kubernetes CronJob resource configured to run this script on schedule.