# Issues Encountered with Dockerized Freeling

## Case Description

The project located at the remote repository https://github.com/PlanTL-SANIDAD/SPACCC_POS-TAGGER was build to be run from a Linux terminal, taking the standard input (STDIN) and returning the results to the standard output (STDOUT).

This way of handling data is not usable if we want to convert this project to an API that handles HTTP requests to be consumed by a frontend in a demos webpage.

The "ENTRYPOINT" (or "CMD") in the last line of the Dockerfile calls the Freeling "analyze" executable, which is the one that works with the STDIN and STDOUT.

## Workaround

Install a simple web server such as Flask and let to him the action of executing the Freeling "analyze". The HTTP response will be the same data returned in the STDOUT but in a JSON format, which can be consumed by a frontend or another API that listens to HTTP responses.

So, let's change that Dockerfile (mainly the ENTRYPOINT line) to try this to work as an API.
