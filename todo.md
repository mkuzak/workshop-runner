Spreadsheet solution is unreliable. The advantage of this solustion is that it is infrastructure independent.
As long as created VM runs the shell script it will work. Unfortunately google spreadsheets don't deal well with multiple machines
trying to edit it at the same time. They will try to edit same cells.

The solution would be to run lightweight server that:
- starts VMs
- collects their ip addresses
- allows workshop users to register
- provides users with ip adress of the machine
- configures VMs to allow users to login to their dedicated machines

Unfortunatelly this solution would be infrastructure dependent (at least I don't see a beeter way).For example on OpenNebula cloud
it would use OpenNebula API to start up and configure machines. This could have plugin/adapeter design, with adapter for each cloud.
