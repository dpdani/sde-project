# SDE Final Project

Final project for Service Design and Engineering.
Daniele Parmeggiani (229317), a.y. 2022/23.

## Running the project

In order to build and use this project, from the root folder of the project,
please run:

```shell
docker compose -p kappa-sde up -d --build
docker run --network=kappa-sde_default -it kappa-sde-kappa-cli sh
```

A shell should be presented, with the `kappa-cli` command available. This
command provides the CLI client of the kappa service.
To learn about the available commands and options, run `kappa-cli --help`.

In order to stop the services, close the shell and run:

```shell
docker compose down
```

## Original Proposal

The proposed service, named κ, is similar in spirit to AWS Lambda.

It will be able to let users log in and register functions (i.e. Python code
snippets) that can be invoked through REST endpoints. For instance, like this:

```
POST http://kappa/functions
{
"name": "my-function",
"code": "def main(a):\n\tprint(a)"
}

GET http://kappa/functions/my-function?a=ciao

DELETE http://kappa/functions/my-function
```

The service will keep track of the number of times a function is invoked in
order to present a monthly bill to each user.

Note that no isolation or security will be provided to the functions,
differently from AWS Lambda. A user, though, will only be able to “see” (i.e.
create / invoke / delete) his own functions.

A command line interface will be provided as a client that is able to request
function creation / invocation / deletion, as well as current billing status and
the handling of authentication. It will also be possible to run simple queries
to the logging system.

## The Process

The user will be able to perform the following workflow:

1. Authenticate user
2. Upload function
3. Check function (does it respect the requirements for being run? I.e. does the
   code have a main function?)
4. Start function
5. Ensure function is available
6. However many times:
    1. User executes the function
    2. User can monitor the function
7. Stop function
8. Ensure function is removed

## Logical Layers

With regards to the four logical layers described in the assignment, the
services that are going to be developed are:

- Process layer:
    - function creation and termination (`kappa`)
- Business logic layer:
    - function runtime, endpoints, and billing logic (`kappa-runner`)
- Adapter layer:
    - unified logs (`kappa-logs`)
- Data layer:
    - user data and logs emitted by the system (`kappa-data`)
    - logs emitted by functions (`kappa-fn-logs`)
    - stored functions code (`kappa-fn-code`)

Overall, six services and one command line client will be developed.
